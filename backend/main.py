import json

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import create_tables, get_db
from models import Opportunity, SavedOpportunity, Student
from recommendation import calculate_match, parse_student_year, recommend_opportunities
from ai_service import generate_opportunity_explanation
from schemas import (
    AIExplanationRequest,
    MatchRequest,
    MatchResult,
    MessageResponse,
    OpportunityResponse,
    RecommendationResponse,
    SavedOpportunityDetail,
    StudentCreate,
    StudentResponse,
)
from seed_data import seed_opportunities


app = FastAPI(
    title="OpporTune AI API",
    description="Backend API for the Student Opportunity Discovery Platform",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    create_tables()
    db = next(get_db())
    try:
        seed_opportunities(db)
    finally:
        db.close()


def serialize_opportunity(opportunity: Opportunity):
    required_skills = json.loads(opportunity.required_skills or "[]")
    preferred_skills = json.loads(opportunity.preferred_skills or "[]")

    return OpportunityResponse(
        id=opportunity.id,
        title=opportunity.title,
        organization=opportunity.organization,
        category=opportunity.category,
        description=opportunity.description,
        required_skills=required_skills,
        preferred_skills=preferred_skills,
        eligibility=opportunity.eligibility,
        eligible_branches=[],
        min_year=None,
        max_year=None,
        location=opportunity.location,
        deadline=opportunity.deadline,
        application_url=opportunity.application_url,
        is_demo=opportunity.is_demo,
        created_at=opportunity.created_at,
    )


def serialize_student(student: Student):
    return StudentResponse(
        id=student.id,
        name=student.name,
        education=student.education,
        year=parse_student_year(student.year),
        branch=student.branch,
        skills=json.loads(student.skills or "[]"),
        interests=json.loads(student.interests or "[]"),
        preferred_categories=json.loads(student.preferred_categories or "[]"),
        preferred_location=student.preferred_location,
        created_at=student.created_at,
    )


@app.get("/")
def root():
    return {
        "message": "Welcome to OpporTune AI API",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "OpporTune AI backend",
    }


@app.post("/api/profile", response_model=StudentResponse, status_code=201)
def create_profile(student_data: StudentCreate, db: Session = Depends(get_db)):
    student = Student(
        name=student_data.name,
        education=student_data.education,
        year=str(student_data.year),
        branch=student_data.branch,
        skills=json.dumps(student_data.skills),
        interests=json.dumps(student_data.interests),
        preferred_categories=json.dumps(student_data.preferred_categories),
        preferred_location=student_data.preferred_location,
    )

    db.add(student)
    db.commit()
    db.refresh(student)

    return serialize_student(student)


@app.get("/api/profile/{student_id}", response_model=StudentResponse)
def get_profile(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()

    if student is None:
        raise HTTPException(status_code=404, detail="Student profile not found")

    return serialize_student(student)


@app.get("/api/opportunities", response_model=list[OpportunityResponse])
def get_opportunities(
    category: str | None = Query(default=None, description="Filter by opportunity category"),
    location: str | None = Query(default=None, description="Filter by location"),
    search: str | None = Query(default=None, description="Search opportunity title, organization or description"),
    db: Session = Depends(get_db),
):
    query = db.query(Opportunity)

    if category:
        query = query.filter(Opportunity.category.ilike(f"%{category}%"))

    if location:
        query = query.filter(Opportunity.location.ilike(f"%{location}%"))

    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            (Opportunity.title.ilike(search_pattern))
            | (Opportunity.organization.ilike(search_pattern))
            | (Opportunity.description.ilike(search_pattern))
        )

    opportunities = query.order_by(Opportunity.deadline.asc()).all()
    return [serialize_opportunity(opportunity) for opportunity in opportunities]


@app.get("/api/opportunities/{opportunity_id}", response_model=OpportunityResponse)
def get_opportunity(opportunity_id: int, db: Session = Depends(get_db)):
    opportunity = db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()

    if opportunity is None:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    return serialize_opportunity(opportunity)


@app.get("/api/recommendations/{student_id}", response_model=list[RecommendationResponse])
def get_recommendations(
    student_id: int,
    limit: int = Query(default=10, ge=1, le=50, description="Maximum number of recommendations"),
    db: Session = Depends(get_db),
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student profile not found")

    opportunities = db.query(Opportunity).order_by(Opportunity.deadline.asc()).all()
    recommendations = recommend_opportunities(student, opportunities)[:limit]
    return [
        {
            **recommendation,
            "opportunity": serialize_opportunity(recommendation["opportunity"]),
        }
        for recommendation in recommendations
    ]


@app.post("/api/match", response_model=MatchResult)
def match_student_to_opportunity(match_request: MatchRequest, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == match_request.student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student profile not found")

    opportunity = db.query(Opportunity).filter(Opportunity.id == match_request.opportunity_id).first()
    if opportunity is None:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    return calculate_match(student, opportunity)


@app.post("/api/ai/explanation")
def get_ai_explanation(request: AIExplanationRequest, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == request.student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student profile not found")

    opportunity = db.query(Opportunity).filter(Opportunity.id == request.opportunity_id).first()
    if opportunity is None:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    match_result = calculate_match(student, opportunity)
    explanation = generate_opportunity_explanation(student, opportunity, match_result)

    return {
        "available": explanation is not None,
        "explanation": explanation or match_result["explanation"],
    }


@app.post("/api/opportunities/{opportunity_id}/save", response_model=MessageResponse)
def save_opportunity(
    opportunity_id: int,
    student_id: int = Query(..., description="ID of the student saving the opportunity"),
    db: Session = Depends(get_db),
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student profile not found")

    opportunity = db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
    if opportunity is None:
        raise HTTPException(status_code=404, detail="Opportunity not found")

    existing_save = (
        db.query(SavedOpportunity)
        .filter(
            SavedOpportunity.student_id == student_id,
            SavedOpportunity.opportunity_id == opportunity_id,
        )
        .first()
    )

    if existing_save:
        return MessageResponse(message="Opportunity is already saved")

    saved_opportunity = SavedOpportunity(student_id=student_id, opportunity_id=opportunity_id)
    db.add(saved_opportunity)
    db.commit()

    return MessageResponse(message="Opportunity saved successfully")


@app.delete("/api/opportunities/{opportunity_id}/save", response_model=MessageResponse)
def remove_saved_opportunity(
    opportunity_id: int,
    student_id: int = Query(..., description="ID of the student removing the saved opportunity"),
    db: Session = Depends(get_db),
):
    saved_opportunity = (
        db.query(SavedOpportunity)
        .filter(
            SavedOpportunity.student_id == student_id,
            SavedOpportunity.opportunity_id == opportunity_id,
        )
        .first()
    )

    if saved_opportunity is None:
        raise HTTPException(status_code=404, detail="Saved opportunity not found")

    db.delete(saved_opportunity)
    db.commit()

    return MessageResponse(message="Opportunity removed from saved list")


@app.get("/api/saved/{student_id}", response_model=list[SavedOpportunityDetail])
def get_saved_opportunities(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student profile not found")

    saved_items = (
        db.query(SavedOpportunity)
        .filter(SavedOpportunity.student_id == student_id)
        .order_by(SavedOpportunity.created_at.desc())
        .all()
    )

    results = []
    for saved_item in saved_items:
        opportunity = db.query(Opportunity).filter(Opportunity.id == saved_item.opportunity_id).first()
        if opportunity is not None:
            results.append(
                {
                    "saved_id": saved_item.id,
                    "opportunity": serialize_opportunity(opportunity),
                    "saved_at": saved_item.created_at,
                }
            )

    return results

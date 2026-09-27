from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class StudentCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    education: str = Field(..., min_length=1, max_length=150)
    year: int = Field(..., ge=1, le=4)
    branch: str = Field(..., min_length=1, max_length=100)
    skills: list[str] = Field(default_factory=list)
    interests: list[str] = Field(default_factory=list)
    preferred_categories: list[str] = Field(default_factory=list)
    preferred_location: str = Field(default="Any", max_length=100)


class StudentResponse(StudentCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class OpportunityResponse(BaseModel):
    id: int
    title: str
    organization: str
    category: str
    description: str
    required_skills: list[str]
    preferred_skills: list[str]
    eligibility: str
    eligible_branches: list[str] = Field(default_factory=list)
    min_year: int | None = None
    max_year: int | None = None
    location: str
    deadline: date
    application_url: str
    is_demo: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SavedOpportunityResponse(BaseModel):
    id: int
    student_id: int
    opportunity_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SavedOpportunityDetail(BaseModel):
    saved_id: int
    opportunity: OpportunityResponse
    saved_at: datetime


class MessageResponse(BaseModel):
    message: str


class ScoreBreakdown(BaseModel):
    skills: float
    interests: float
    eligibility: float
    location: float
    category: float


class EligibilityDetails(BaseModel):
    eligible: bool
    year_eligible: bool
    branch_eligible: bool


class MatchResult(BaseModel):
    match_percentage: float
    matching_skills: list[str]
    skill_gaps: list[str]
    preferred_skill_gaps: list[str]
    matching_interests: list[str]
    eligible: bool
    score_breakdown: ScoreBreakdown
    eligibility_details: EligibilityDetails
    explanation: str


class RecommendationResponse(MatchResult):
    opportunity: OpportunityResponse


class MatchRequest(BaseModel):
    student_id: int
    opportunity_id: int


class AIExplanationRequest(BaseModel):
    student_id: int
    opportunity_id: int

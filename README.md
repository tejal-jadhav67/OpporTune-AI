# OpporTune AI

> Personalized opportunities. Smarter decisions.

OpporTune AI is an AI-powered student opportunity discovery platform designed to help students discover internships, hackathons, competitions, courses, certifications, workshops and scholarships that match their profile.

## Problem
Students often miss valuable opportunities because information is scattered across different websites, social media platforms, college groups and other sources.

## Solution
OpporTune AI creates a centralized opportunity discovery platform where students can create a profile and receive personalized, explainable recommendations.

The system evaluates:

- Skills
- Interests
- Eligibility
- Location
- Opportunity category

It then calculates a transparent match score and identifies relevant skill gaps.

## Planned Features

- Student profile
- Opportunity explorer
- Search and filtering
- Personalized recommendations
- Explainable match scores
- Skill-gap analysis
- Opportunity details
- Save/bookmark opportunities
- Student dashboard
- AI-generated recommendation explanations

## Technology Stack

### Frontend

- React
- Vite
- Tailwind CSS
- React Router
- Lucide React

### Backend

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- SQLite

### AI

- Deterministic recommendation engine
- Optional LLM-based explanation layer

### Deployment

- Docker
- Google Cloud Run

## Development Phases
1. Project setup and application skeleton.
2. Database and seed data
3. Backend APIs
4. Recommendation engine
5. Frontend functionality
6. AI integration
7. Testing
8. Netlify/Vercel Deployment
9. Final polish

## Running Locally

### Backend

```bash
cd backend
python -m venv venv
```

Activate the virtual environment and install dependencies:

```bash
pip install -r requirements.txt
```

Start FastAPI:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend:

```text
http://localhost:8000
```

API documentation:

```text
http://localhost:8000/docs
```

### Frontend

In another terminal:

```bash
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:5173
```

## Project Architecture

```text
React + Vite
      |
      | REST API
      v
FastAPI
      |
      +---- SQLite
      |
      +---- Recommendation Engine
      |
      +---- AI Explanation Layer
```

## Future Scope
The MVP can later be extended with:

- Automated opportunity ingestion
- Semantic opportunity matching
- Resume-to-profile extraction
- Natural-language search
- Opportunity freshness detection
- Notifications
- Managed PostgreSQL database
- Authentication
- Admin tools

## Contributors
Tejal Jadhav

from datetime import datetime

from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    education: Mapped[str] = mapped_column(String(100), nullable=False)
    year: Mapped[str] = mapped_column(String(50), nullable=False)
    branch: Mapped[str] = mapped_column(String(100), nullable=False)
    skills: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    interests: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    preferred_categories: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    preferred_location: Mapped[str] = mapped_column(String(100), nullable=False, default="Any")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    saved_opportunities: Mapped[list["SavedOpportunity"]] = relationship(
        "SavedOpportunity",
        back_populates="student",
        cascade="all, delete-orphan",
    )


class Opportunity(Base):
    __tablename__ = "opportunities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    organization: Mapped[str] = mapped_column(String(200), nullable=False)
    category: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    required_skills: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    preferred_skills: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    eligibility: Mapped[str] = mapped_column(Text, nullable=False)
    eligible_branches: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    min_year: Mapped[int | None] = mapped_column(Integer, nullable=True, default=None)
    max_year: Mapped[int | None] = mapped_column(Integer, nullable=True, default=None)
    location: Mapped[str] = mapped_column(String(100), nullable=False)
    deadline: Mapped[str] = mapped_column(Date, nullable=False)
    application_url: Mapped[str] = mapped_column(String(500), nullable=False)
    is_demo: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    saved_by_students: Mapped[list["SavedOpportunity"]] = relationship(
        "SavedOpportunity",
        back_populates="opportunity",
        cascade="all, delete-orphan",
    )


class SavedOpportunity(Base):
    __tablename__ = "saved_opportunities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False)
    opportunity_id: Mapped[int] = mapped_column(ForeignKey("opportunities.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    student: Mapped["Student"] = relationship("Student", back_populates="saved_opportunities")
    opportunity: Mapped["Opportunity"] = relationship("Opportunity", back_populates="saved_by_students")

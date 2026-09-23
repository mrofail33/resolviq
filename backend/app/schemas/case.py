from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.case import CaseCategory, CaseStatus


class CaseCreate(BaseModel):
    user_email: str = Field(default="demo@resolviq.local")
    user_full_name: str = Field(default="Demo User")
    title: str = Field(min_length=3, max_length=160)
    category: CaseCategory


class CaseStatusUpdate(BaseModel):
    status: CaseStatus


class DeadlineCreate(BaseModel):
    label: str = Field(min_length=3, max_length=160)
    due_date: date


class DeadlineRead(BaseModel):
    id: int
    label: str
    due_date: date
    completed: bool

    model_config = ConfigDict(from_attributes=True)


class DocumentRead(BaseModel):
    id: int
    filename: str
    content_type: str
    extracted_text: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class StructuredDate(BaseModel):
    label: str = Field(min_length=2, max_length=120)
    date: date


class StructuredCaseAnalysis(BaseModel):
    summary: str = Field(min_length=20)
    company: str = Field(min_length=2, max_length=160)
    disputed_amount: Decimal | None = Field(default=None, ge=0)
    important_dates: list[StructuredDate] = Field(default_factory=list)
    dispute_reason: str = Field(min_length=10)
    evidence: list[str] = Field(default_factory=list)
    missing_information: list[str] = Field(default_factory=list)

    @field_validator("evidence", "missing_information")
    @classmethod
    def strip_empty_items(cls, value: list[str]) -> list[str]:
        return [item.strip() for item in value if item.strip()]


class CaseRead(BaseModel):
    id: int
    title: str
    category: CaseCategory
    status: CaseStatus
    company: str | None
    disputed_amount: Decimal | None
    summary: str | None
    dispute_reason: str | None
    generated_draft: str | None
    created_at: datetime
    documents: list[DocumentRead] = []
    deadlines: list[DeadlineRead] = []
    evidence: list[str] = []
    missing_information: list[str] = []
    important_dates: list[StructuredDate] = []

    model_config = ConfigDict(from_attributes=True)

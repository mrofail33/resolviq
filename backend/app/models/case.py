from datetime import date, datetime
from enum import Enum
from sqlalchemy import Date, DateTime, Enum as SQLEnum, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class CaseCategory(str, Enum):
    refund = "refund"
    warranty = "warranty"
    travel = "travel"


class CaseStatus(str, Enum):
    draft = "draft"
    waiting_on_company = "waiting_on_company"
    follow_up_needed = "follow_up_needed"
    resolved = "resolved"
    closed = "closed"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(120))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    cases: Mapped[list["Case"]] = relationship(back_populates="user")


class Case(Base):
    __tablename__ = "cases"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(String(160))
    category: Mapped[CaseCategory] = mapped_column(SQLEnum(CaseCategory, name="case_category"))
    status: Mapped[CaseStatus] = mapped_column(
        SQLEnum(CaseStatus, name="case_status"), default=CaseStatus.draft
    )
    company: Mapped[str | None] = mapped_column(String(160), nullable=True)
    disputed_amount: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    dispute_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    generated_draft: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    user: Mapped[User] = relationship(back_populates="cases")
    documents: Mapped[list["Document"]] = relationship(
        back_populates="case", cascade="all, delete-orphan"
    )
    deadlines: Mapped[list["Deadline"]] = relationship(
        back_populates="case", cascade="all, delete-orphan"
    )


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    case_id: Mapped[int] = mapped_column(ForeignKey("cases.id"))
    filename: Mapped[str] = mapped_column(String(255))
    content_type: Mapped[str] = mapped_column(String(120))
    extracted_text: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    case: Mapped[Case] = relationship(back_populates="documents")


class EvidenceItem(Base):
    __tablename__ = "evidence_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    case_id: Mapped[int] = mapped_column(ForeignKey("cases.id"), index=True)
    label: Mapped[str] = mapped_column(String(255))


class MissingInformation(Base):
    __tablename__ = "missing_information"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    case_id: Mapped[int] = mapped_column(ForeignKey("cases.id"), index=True)
    label: Mapped[str] = mapped_column(String(255))


class ImportantDate(Base):
    __tablename__ = "important_dates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    case_id: Mapped[int] = mapped_column(ForeignKey("cases.id"), index=True)
    label: Mapped[str] = mapped_column(String(120))
    date_value: Mapped[date] = mapped_column(Date)


class Deadline(Base):
    __tablename__ = "deadlines"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    case_id: Mapped[int] = mapped_column(ForeignKey("cases.id"))
    label: Mapped[str] = mapped_column(String(160))
    due_date: Mapped[date] = mapped_column(Date)
    completed: Mapped[bool] = mapped_column(default=False)

    case: Mapped[Case] = relationship(back_populates="deadlines")

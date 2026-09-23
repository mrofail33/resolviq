from datetime import date, timedelta

from app.db.session import Base, SessionLocal, engine
from app.models.case import Case, CaseCategory, Deadline, User


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(User).first():
            return
        user = User(email="demo@resolviq.local", full_name="Demo User")
        db.add(user)
        db.flush()
        case = Case(
            user_id=user.id,
            title="Laptop warranty denied",
            category=CaseCategory.warranty,
            company="Northstar Laptops",
            disputed_amount=849.00,
            summary="The user has a denied laptop warranty claim with proof of purchase.",
            dispute_reason="The manufacturer denied coverage even though the issue occurred during the warranty period.",
            generated_draft="Subject: Request to review denied warranty claim\n\nPlease review my warranty claim and the attached evidence.",
        )
        db.add(case)
        db.flush()
        db.add(
            Deadline(
                case_id=case.id,
                label="Send warranty appeal",
                due_date=date.today() + timedelta(days=7),
            )
        )
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()

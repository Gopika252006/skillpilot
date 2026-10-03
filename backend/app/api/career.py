from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import User
from app.schemas.schemas import CareerProfileOut
from app.services.career_service import career_service
from app.api.deps import get_current_user

router = APIRouter(prefix="/career", tags=["Career & Skill Gap"])

@router.get("/path", response_model=CareerProfileOut)
def get_career_path(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Career Path Intelligence: Compares user's proven knowledge vs target role,
    computes skill gaps, and recommends high-value projects & certifications.
    """
    profile = career_service.get_or_calculate_career_profile(db, current_user.id)
    return CareerProfileOut(
        target_role=profile.target_role,
        readiness_score=profile.readiness_score,
        strong_skills=profile.strong_skills,
        gap_skills=profile.gap_skills,
        recommended_actions=profile.recommended_actions,
        recommended_projects=profile.recommended_projects,
        recommended_certifications=profile.recommended_certifications
    )

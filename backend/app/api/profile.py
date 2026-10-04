from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import User, UserProfile
from app.schemas.schemas import UserProfileUpdate, UserProfileOut
from app.api.deps import get_current_user

router = APIRouter(prefix="/profile", tags=["User Profile"])

@router.get("", response_model=UserProfileOut)
def get_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = current_user.profile
    if not profile:
        profile = UserProfile(
            user_id=current_user.id,
            target_role="Backend Software Engineer",
            experience_level="Intermediate",
            learning_goals="Build mastery over complex DSA and distributed systems.",
            weekly_hours=7,
            onboarding_completed=False
        )
        profile.current_technologies = ["Python", "Java", "SQL"]
        profile.interests = ["DSA", "System Design", "Backend"]
        db.add(profile)
        db.commit()
        db.refresh(profile)
    return profile

@router.put("", response_model=UserProfileOut)
def update_profile(
    profile_in: UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    profile = current_user.profile
    if not profile:
        profile = UserProfile(user_id=current_user.id)
        db.add(profile)

    if profile_in.target_role is not None:
        profile.target_role = profile_in.target_role
    if profile_in.experience_level is not None:
        profile.experience_level = profile_in.experience_level
    if profile_in.learning_goals is not None:
        profile.learning_goals = profile_in.learning_goals
    if profile_in.weekly_hours is not None:
        profile.weekly_hours = profile_in.weekly_hours
    if profile_in.current_technologies is not None:
        profile.current_technologies = profile_in.current_technologies
    if profile_in.interests is not None:
        profile.interests = profile_in.interests
    if profile_in.onboarding_completed is not None:
        profile.onboarding_completed = profile_in.onboarding_completed

    db.commit()
    db.refresh(profile)
    return profile

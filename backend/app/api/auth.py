from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_password_hash, verify_password, create_access_token
from app.models.models import User, UserProfile
from app.schemas.schemas import UserRegister, UserLogin, TokenResponse, UserOut
from app.api.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=TokenResponse)
def register(user_in: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_in.email.lower()).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email address already exists."
        )

    # First user can optionally be made admin if role is ADMIN
    user = User(
        email=user_in.email.lower(),
        hashed_password=get_password_hash(user_in.password),
        full_name=user_in.full_name,
        role=user_in.role if user_in.role in ["USER", "ADMIN"] else "USER",
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Initialize default profile
    profile = UserProfile(
        user_id=user.id,
        target_role="Backend Software Engineer",
        experience_level="Intermediate",
        learning_goals="Build mastery over complex DSA, system design, and distributed architectures.",
        weekly_hours=7,
        onboarding_completed=False
    )
    profile.current_technologies = ["Python", "Java", "SQL", "Git"]
    profile.interests = ["DSA", "System Design", "Backend", "AI/ML"]
    db.add(profile)
    db.commit()

    token = create_access_token(subject=user.id, role=user.role)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "onboarding_completed": False
        }
    }

@router.post("/login", response_model=TokenResponse)
def login(login_in: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_in.email.lower()).first()
    if not user or not verify_password(login_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password."
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive."
        )

    token = create_access_token(subject=user.id, role=user.role)
    onboarding_done = user.profile.onboarding_completed if user.profile else False

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "onboarding_completed": onboarding_done
        }
    }

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    profile = current_user.profile
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "role": current_user.role,
        "onboarding_completed": profile.onboarding_completed if profile else False,
        "profile": {
            "target_role": profile.target_role if profile else "Software Engineer",
            "experience_level": profile.experience_level if profile else "Intermediate",
            "learning_goals": profile.learning_goals if profile else "",
            "weekly_hours": profile.weekly_hours if profile else 5,
            "current_technologies": profile.current_technologies if profile else [],
            "interests": profile.interests if profile else []
        }
    }

@router.post("/logout")
def logout(current_user: User = Depends(get_current_user)):
    return {"message": "Logged out successfully."}

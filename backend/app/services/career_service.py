from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.models.models import CareerProfile, UserProfile, KnowledgeConcept
from app.schemas.schemas import CareerProfileOut
from app.ai.context_builder import build_user_technical_context
from app.ai.orchestrator import ai_orchestrator

class CareerService:
    """Calculates skill gap analysis, high-value project and certification recommendations."""

    @staticmethod
    def get_or_calculate_career_profile(db: Session, user_id: int) -> CareerProfile:
        career = db.query(CareerProfile).filter(CareerProfile.user_id == user_id).first()
        
        user_context = build_user_technical_context(db, user_id)
        analysis = ai_orchestrator.generate_career_analysis(user_context)

        if not career:
            career = CareerProfile(
                user_id=user_id,
                target_role=user_context.get("target_role", "Backend Software Engineer"),
                readiness_score=analysis.get("readiness_score", 72.0)
            )
            career.strong_skills = analysis.get("strong_skills", [])
            career.gap_skills = analysis.get("gap_skills", [])
            career.recommended_actions = analysis.get("recommended_actions", [])
            career.recommended_projects = analysis.get("recommended_projects", [])
            career.recommended_certifications = analysis.get("recommended_certifications", [])
            db.add(career)
        else:
            career.target_role = user_context.get("target_role", "Backend Software Engineer")
            career.readiness_score = analysis.get("readiness_score", 72.0)
            career.strong_skills = analysis.get("strong_skills", [])
            career.gap_skills = analysis.get("gap_skills", [])
            career.recommended_actions = analysis.get("recommended_actions", [])
            career.recommended_projects = analysis.get("recommended_projects", [])
            career.recommended_certifications = analysis.get("recommended_certifications", [])

        db.commit()
        db.refresh(career)
        return career

career_service = CareerService()

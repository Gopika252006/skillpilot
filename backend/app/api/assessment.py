from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import User
from app.schemas.schemas import AssessmentOut, AssessmentSubmitRequest
from app.services.assessment_service import assessment_service
from app.api.deps import get_current_user

router = APIRouter(prefix="/assessment", tags=["Weekend Assessment"])

@router.get("/current", response_model=AssessmentOut)
def get_current_assessment(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve or generate the active weekly adaptive assessment."""
    return assessment_service.get_or_create_weekly_assessment(db, current_user.id)

@router.post("/generate", response_model=AssessmentOut)
def generate_assessment(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Generate or retrieve the active weekend assessment."""
    return assessment_service.get_or_create_weekly_assessment(db, current_user.id)

@router.get("/history")
def get_assessment_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve all past completed assessments with scores and feedback."""
    from app.models.models import Assessment
    assessments = db.query(Assessment).filter(
        Assessment.user_id == current_user.id
    ).order_by(Assessment.created_at.desc()).all()
    return [
        {
            "id": a.id,
            "title": a.title,
            "status": a.status,
            "score": a.score,
            "total_score": a.total_score,
            "feedback_summary": a.feedback_summary,
            "strong_areas": a.strong_areas,
            "weak_areas": a.weak_areas,
            "completed_at": a.completed_at,
            "created_at": a.created_at
        }
        for a in assessments
    ]

@router.post("/{assessment_id}/submit", response_model=AssessmentOut)
def submit_assessment(
    assessment_id: int,
    req: AssessmentSubmitRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Submit answers, trigger AI evaluation, identify weak areas, and feed verified
    test performance into Personal Technical Memory.
    """
    try:
        return assessment_service.submit_assessment(db, current_user.id, assessment_id, req.answers)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

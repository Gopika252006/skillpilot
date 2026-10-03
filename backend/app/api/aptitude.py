from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import User
from app.schemas.schemas import AptitudeSubmitRequest
from app.services.aptitude_service import aptitude_service
from app.api.deps import get_current_user

router = APIRouter(prefix="/aptitude", tags=["Aptitude Sprint"])

@router.get("/sprint")
def get_daily_sprint():
    """Retrieve the daily 5-question aptitude sprint."""
    return aptitude_service.get_daily_sprint()

@router.post("/attempt")
def submit_aptitude_attempt(
    req: AptitudeSubmitRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Submit answer to an aptitude question and get immediate explanation."""
    try:
        return aptitude_service.record_attempt(
            db=db,
            user_id=current_user.id,
            question_idx=req.question_index,
            selected_option=req.selected_option,
            time_taken_seconds=req.time_taken_seconds
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/stats")
def get_aptitude_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve accuracy and attempt statistics."""
    return aptitude_service.get_stats(db, current_user.id)

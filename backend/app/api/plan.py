from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import User
from app.schemas.schemas import WeeklyPlanOut
from app.services.plan_service import plan_service
from app.api.deps import get_current_user

router = APIRouter(prefix="/plan", tags=["Weekly Learning Plan"])

@router.get("/current", response_model=WeeklyPlanOut)
def get_current_plan(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve the active adaptive weekly learning plan."""
    return plan_service.get_or_create_active_plan(db, current_user.id)

@router.post("/generate", response_model=WeeklyPlanOut)
def generate_new_plan(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Regenerate a 15-20 min/day weekly plan based on the latest knowledge memory state."""
    return plan_service.generate_adaptive_plan(db, current_user.id)

@router.post("/tasks/{task_id}/toggle")
def toggle_task_completion(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Toggle a daily task between completed and pending."""
    task = plan_service.toggle_task(db, current_user.id, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found.")
    return {
        "id": task.id,
        "is_completed": task.is_completed,
        "completed_at": task.completed_at
    }

from datetime import datetime
from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.models import WeeklyPlan, WeeklyTask
from app.schemas.schemas import WeeklyPlanOut
from app.ai.context_builder import build_user_technical_context
from app.ai.orchestrator import ai_orchestrator

class PlanService:
    """Manages adaptive 15-20 min/day weekly learning plans."""

    @staticmethod
    def get_or_create_active_plan(db: Session, user_id: int) -> WeeklyPlan:
        plan = db.query(WeeklyPlan).filter(
            WeeklyPlan.user_id == user_id,
            WeeklyPlan.is_active == True
        ).first()

        if not plan:
            plan = PlanService.generate_adaptive_plan(db, user_id)

        return plan

    @staticmethod
    def generate_adaptive_plan(db: Session, user_id: int) -> WeeklyPlan:
        # Mark previous plans inactive
        db.query(WeeklyPlan).filter(
            WeeklyPlan.user_id == user_id,
            WeeklyPlan.is_active == True
        ).update({"is_active": False})
        db.commit()

        # Build context
        user_context = build_user_technical_context(db, user_id)
        plan_data = ai_orchestrator.generate_weekly_plan(user_context)

        plan = WeeklyPlan(
            user_id=user_id,
            week_title=plan_data.get("week_title", "Weekly Mastery Sprint"),
            focus_area=plan_data.get("focus_area", "Algorithms & System Design"),
            rationale=plan_data.get("rationale", "Tailored to your current knowledge gaps and target career goals."),
            is_active=True
        )
        db.add(plan)
        db.commit()
        db.refresh(plan)

        tasks_data = plan_data.get("tasks", [])
        for t in tasks_data:
            task = WeeklyTask(
                plan_id=plan.id,
                day_of_week=t.get("day_of_week", "Monday"),
                title=t.get("title", "Practice Task"),
                description=t.get("description", ""),
                target_concept=t.get("target_concept", "Core DSA"),
                estimated_minutes=t.get("estimated_minutes", 15),
                is_completed=False
            )
            db.add(task)
        
        db.commit()
        db.refresh(plan)
        return plan

    @staticmethod
    def toggle_task(db: Session, user_id: int, task_id: int) -> Optional[WeeklyTask]:
        task = db.query(WeeklyTask).join(WeeklyPlan).filter(
            WeeklyTask.id == task_id,
            WeeklyPlan.user_id == user_id
        ).first()

        if not task:
            return None

        task.is_completed = not task.is_completed
        task.completed_at = datetime.utcnow() if task.is_completed else None
        db.commit()
        db.refresh(task)
        return task

plan_service = PlanService()

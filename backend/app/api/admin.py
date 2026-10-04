from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import User, CodeAnalysis, KnowledgeVaultItem, LearningLog
from app.schemas.schemas import AdminStatsOut
from app.ai.orchestrator import ai_orchestrator
from app.api.deps import get_current_admin

router = APIRouter(prefix="/admin", tags=["Admin Portal"])

@router.get("/stats", response_model=AdminStatsOut)
def get_admin_stats(
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin)
):
    """
    Admin-only portal statistics:
    View user counts, code analysis counts, vault volume, and local AI health.
    Never exposes another user's personal knowledge or private code.
    """
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    total_analyses = db.query(CodeAnalysis).count()
    total_vault = db.query(KnowledgeVaultItem).count()
    total_logs = db.query(LearningLog).count()

    ai_info = ai_orchestrator.get_status()

    return AdminStatsOut(
        total_users=total_users,
        active_users=active_users,
        total_code_analyses=total_analyses,
        total_vault_items=total_vault,
        total_learning_logs=total_logs,
        system_health="Operational (Green)",
        ai_status=ai_info.get("status", "operational"),
        active_model=ai_info.get("active_runtime", "Open-Weight Local")
    )

@router.get("/overview")
def get_admin_overview(
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin)
):
    total_users = db.query(User).count()
    active_users = db.query(User).filter(User.is_active == True).count()
    total_analyses = db.query(CodeAnalysis).count()
    total_vault = db.query(KnowledgeVaultItem).count()
    ai_info = ai_orchestrator.get_status()

    return {
        "total_users": total_users,
        "active_users": active_users,
        "total_submissions": total_analyses,
        "total_vault_items": total_vault,
        "system_health": "Operational (Green)",
        "ai_status": ai_info.get("status", "operational"),
        "active_model": ai_info.get("active_runtime", "Open-Weight Local")
    }

@router.get("/users")
def get_admin_users(
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin)
):
    users = db.query(User).all()
    return [
        {
            "id": u.id,
            "email": u.email,
            "full_name": u.full_name,
            "role": u.role,
            "is_active": u.is_active,
            "created_at": u.created_at
        }
        for u in users
    ]

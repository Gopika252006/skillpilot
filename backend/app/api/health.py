from fastapi import APIRouter
from app.ai.orchestrator import ai_orchestrator

router = APIRouter(tags=["Health & Open AI Status"])

@router.get("/health")
def health_check():
    """Application health and runtime status."""
    ai_status = ai_orchestrator.get_status()
    return {
        "status": "healthy",
        "service": "CodePilot API",
        "version": "1.0.0",
        "ai": ai_status
    }

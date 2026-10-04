from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import User
from app.schemas.schemas import CodeAnalyzeRequest, CodeAnalyzeResponse
from app.services.code_service import code_service
from app.api.deps import get_current_user

router = APIRouter(prefix="/code", tags=["Code Analyzer"])

@router.post("/analyze", response_model=CodeAnalyzeResponse)
def analyze_code(
    req: CodeAnalyzeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Hero Feature: Analyzes user's code, calculates complexity, extracts concepts,
    detects potential boundary bugs, provides progressive hints, and updates
    Personal Technical Knowledge profile with verified practice evidence.
    """
    return code_service.analyze_and_record(db, current_user.id, req)

@router.get("/history")
@router.get("/submissions")
def get_analysis_history(
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get history of past code submissions analyzed by CodePilot."""
    analyses = code_service.get_user_history(db, current_user.id, limit=limit)
    return [
        {
            "id": a.id,
            "problem_title": a.problem_title,
            "language": a.language,
            "approach_detected": a.approach_detected,
            "time_complexity": a.time_complexity,
            "space_complexity": a.space_complexity,
            "code_quality_score": a.code_quality_score,
            "concepts_detected": a.concepts_detected,
            "created_at": a.created_at
        }
        for a in analyses
    ]

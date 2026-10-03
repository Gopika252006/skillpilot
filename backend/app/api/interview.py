from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import User
from app.schemas.schemas import InterviewStartRequest, InterviewAnswerRequest
from app.services.interview_service import interview_service
from app.api.deps import get_current_user

router = APIRouter(prefix="/interview", tags=["Adaptive Interview"])

@router.post("/start")
def start_interview(
    req: InterviewStartRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Start an adaptive verbal/technical interview based on target role and weak areas."""
    session = interview_service.start_session(db, current_user.id, req.topic or "DSA & Backend Architecture")
    first_exchange = session.exchanges[0] if session.exchanges else None
    return {
        "session_id": session.id,
        "target_role": session.target_role,
        "topic": session.topic,
        "status": session.status,
        "first_question": {
            "question_number": first_exchange.question_number if first_exchange else 1,
            "question": first_exchange.question if first_exchange else "Explain your technical background."
        }
    }

@router.post("/answer")
def submit_interview_answer(
    req: InterviewAnswerRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Submit answer, evaluate technical depth, and receive follow-up question."""
    try:
        return interview_service.submit_answer(
            db=db,
            user_id=current_user.id,
            session_id=req.session_id,
            question_number=req.question_number,
            user_answer=req.user_answer
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/sessions/{session_id}")
def get_interview_session(
    session_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    session = interview_service.get_session(db, current_user.id, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Interview session not found.")
    return {
        "id": session.id,
        "target_role": session.target_role,
        "topic": session.topic,
        "status": session.status,
        "overall_score": session.overall_score,
        "clarity_feedback": session.clarity_feedback,
        "technical_depth_feedback": session.technical_depth_feedback,
        "exchanges": [
            {
                "question_number": e.question_number,
                "question": e.question,
                "user_answer": e.user_answer,
                "ai_feedback": e.ai_feedback,
                "score": e.score,
                "follow_up_question": e.follow_up_question
            }
            for e in session.exchanges
        ]
    }

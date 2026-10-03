from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.models import User
from app.schemas.schemas import ChatRequest, ChatResponse
from app.services.chat_service import chat_service
from app.api.deps import get_current_user

router = APIRouter(prefix="/chat", tags=["Ask My AI"])

@router.post("/message", response_model=ChatResponse)
def send_chat_message(
    req: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Ask My AI: Context-aware personal technical companion that grounds its answers
    in the user's specific learning memory, weak concepts, recent code analyses,
    and target career role.
    """
    return chat_service.send_message(db, current_user.id, req)

@router.get("/history")
def get_chat_history(
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    messages = chat_service.get_history(db, current_user.id, limit=limit)
    return [
        {
            "id": m.id,
            "role": m.role,
            "content": m.content,
            "context_used": m.context_used,
            "created_at": m.created_at
        }
        for m in messages
    ]

from typing import Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.models import ChatMessage
from app.schemas.schemas import ChatRequest, ChatResponse
from app.ai.context_builder import build_user_technical_context
from app.ai.orchestrator import ai_orchestrator

class ChatService:
    """Manages Ask My AI technical companion conversations."""

    @staticmethod
    def send_message(db: Session, user_id: int, req: ChatRequest) -> ChatResponse:
        # 1. Build comprehensive user technical context
        user_context = build_user_technical_context(db, user_id)

        # 2. Append active code or topic to context if present
        if req.active_code:
            user_context["prompt_block"] += f"\n\n[USER CURRENTLY HAS THIS CODE OPEN IN EDITOR]:\n{req.active_code}\n"
        if req.current_topic:
            user_context["prompt_block"] += f"\n[CURRENT DISCUSSION TOPIC]: {req.current_topic}\n"

        # 3. Call AI
        ai_resp = ai_orchestrator.answer_question(message=req.message, user_context=user_context)

        context_used = ai_resp.get("context_used", [])
        if not context_used:
            context_used = user_context.get("context_badges", [])

        # 4. Save user and assistant messages
        user_msg = ChatMessage(
            user_id=user_id,
            role="user",
            content=req.message,
            context_used=[]
        )
        asst_msg = ChatMessage(
            user_id=user_id,
            role="assistant",
            content=ai_resp.get("reply", ""),
            context_used=context_used
        )
        db.add(user_msg)
        db.add(asst_msg)
        db.commit()

        return ChatResponse(
            reply=ai_resp.get("reply", ""),
            context_used=context_used,
            suggested_followups=ai_resp.get("suggested_followups", []),
            model_used=ai_resp.get("model_used", "local")
        )

    @staticmethod
    def get_history(db: Session, user_id: int, limit: int = 50) -> List[ChatMessage]:
        return db.query(ChatMessage).filter(
            ChatMessage.user_id == user_id
        ).order_by(ChatMessage.created_at.asc()).limit(limit).all()

chat_service = ChatService()

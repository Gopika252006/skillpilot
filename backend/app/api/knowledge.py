from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.core.database import get_db
from app.models.models import User, KnowledgeConcept, LearningLog
from app.schemas.schemas import ConceptOut, KnowledgeGraphResponse, LearningLogCreate, LearningLogOut
from app.services.knowledge_service import knowledge_service
from app.ai.orchestrator import ai_orchestrator
from app.api.deps import get_current_user

router = APIRouter(prefix="/knowledge", tags=["Personal Knowledge Memory"])

@router.get("/concepts", response_model=List[ConceptOut])
def get_concepts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve all structured personal technical memory concepts."""
    return knowledge_service.get_user_concepts(db, current_user.id)

@router.get("/graph", response_model=KnowledgeGraphResponse)
def get_knowledge_graph(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Visual knowledge graph nodes, prerequisites, status, and mastery stats."""
    return knowledge_service.get_knowledge_graph(db, current_user.id)

@router.post("/log", response_model=LearningLogOut)
def record_learning_log(
    log_in: LearningLogCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Record external learning ('I Learned This'). AI automatically extracts
    concepts and registers learning evidence into the knowledge graph.
    """
    extracted = ai_orchestrator.extract_concepts(f"{log_in.topic}: {log_in.notes}")

    log = LearningLog(
        user_id=current_user.id,
        topic=log_in.topic,
        notes=log_in.notes,
        source=log_in.source or "Self Study",
        time_spent_mins=log_in.time_spent_mins or 20,
        confidence_rating=log_in.confidence_rating or 3
    )
    log.extracted_concepts = extracted
    db.add(log)
    db.commit()
    db.refresh(log)

    # Register concepts in Knowledge Memory
    for c_name in extracted:
        knowledge_service.get_or_create_concept(db, current_user.id, c_name)

    return log

@router.get("/logs", response_model=List[LearningLogOut])
def get_learning_logs(
    limit: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(LearningLog).filter(
        LearningLog.user_id == current_user.id
    ).order_by(desc(LearningLog.created_at)).limit(limit).all()

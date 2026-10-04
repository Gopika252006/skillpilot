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

@router.get("/heatmap")
def get_activity_heatmap(
    days: int = 30,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Activity heatmap showing daily practice, code analyses, and learning logs over time."""
    from datetime import datetime, timedelta
    from app.models.models import CodeAnalysis, Assessment
    from collections import defaultdict

    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=days - 1)

    daily_counts = defaultdict(int)

    # 1. Analyses
    analyses = db.query(CodeAnalysis).filter(
        CodeAnalysis.user_id == current_user.id,
        CodeAnalysis.created_at >= datetime.combine(start_date, datetime.min.time())
    ).all()
    for a in analyses:
        daily_counts[a.created_at.date().isoformat()] += 1

    # 2. Logs
    logs = db.query(LearningLog).filter(
        LearningLog.user_id == current_user.id,
        LearningLog.created_at >= datetime.combine(start_date, datetime.min.time())
    ).all()
    for l in logs:
        daily_counts[l.created_at.date().isoformat()] += 1

    # Build sequence
    day_list = []
    curr = start_date
    while curr <= end_date:
        d_str = curr.isoformat()
        day_list.append({
            "date": d_str,
            "count": daily_counts.get(d_str, 0)
        })
        curr += timedelta(days=1)

    total_activities = sum(daily_counts.values())
    return {
        "days": day_list,
        "total_activities": total_activities,
        "current_streak": min(total_activities, 5)
    }

@router.get("/public")
def get_public_showcase(db: Session = Depends(get_db)):
    """Public showcase of concepts and learning structures for demo & visitors."""
    concepts = db.query(KnowledgeConcept).limit(20).all()
    return {
        "concepts": [
            {
                "name": c.name,
                "category": c.category,
                "status": c.status,
                "confidence": c.confidence,
                "practice_count": c.practice_count
            }
            for c in concepts
        ],
        "categories": ["DSA", "System Design", "Backend", "Core CS"]
    }

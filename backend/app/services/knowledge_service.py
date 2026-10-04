from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.models.models import KnowledgeConcept, User
from app.schemas.schemas import KnowledgeGraphResponse, KnowledgeGraphNode, KnowledgeGraphEdge

# Pre-defined hierarchy relationships for clean knowledge graph visualization
PREREQUISITE_MAP = {
    "Binary Search": ["Arrays", "Boundary Invariants"],
    "Sliding Window": ["Arrays", "Two Pointers"],
    "Dynamic Programming": ["Recursion", "Memoization", "Optimal Substructure"],
    "Graph BFS/DFS": ["Graphs", "Queue", "Recursion"],
    "Tree Traversal": ["Binary Trees", "Recursion"],
    "System Design": ["Caching", "Load Balancing", "Databases"],
    "Kafka": ["Distributed Systems", "Concurrency"],
    "Caching": ["System Design", "Hash Table"]
}

CATEGORY_MAP = {
    "Arrays": "DSA",
    "Binary Search": "DSA",
    "Sliding Window": "DSA",
    "Two Pointers": "DSA",
    "Dynamic Programming": "DSA",
    "Recursion": "DSA",
    "Memoization": "DSA",
    "Optimal Substructure": "DSA",
    "Graph BFS/DFS": "DSA",
    "Graphs": "DSA",
    "Tree Traversal": "DSA",
    "Binary Trees": "DSA",
    "Hash Table": "DSA",
    "Boundary Invariants": "Core CS",
    "System Design": "System Design",
    "Caching": "System Design",
    "Load Balancing": "System Design",
    "Kafka": "Backend",
    "Distributed Systems": "Backend",
    "Databases": "Backend",
    "Queue": "DSA"
}

class KnowledgeService:
    """
    Manages the Personal Technical Memory Engine.
    Knowledge states are strictly evidence-driven:
    NOT_STARTED -> LEARNING -> PRACTICED -> STRONG -> NEEDS_REVISION
    """

    @staticmethod
    def get_or_create_concept(db: Session, user_id: int, concept_name: str, category: Optional[str] = None) -> KnowledgeConcept:
        concept_name = concept_name.strip()
        concept = db.query(KnowledgeConcept).filter(
            KnowledgeConcept.user_id == user_id,
            KnowledgeConcept.name == concept_name
        ).first()

        if not concept:
            resolved_category = category or CATEGORY_MAP.get(concept_name, "General")
            concept = KnowledgeConcept(
                user_id=user_id,
                name=concept_name,
                category=resolved_category,
                status="NOT_STARTED",
                confidence=0.0,
                practice_count=0,
                success_rate=0.0,
                repeated_mistakes=[],
                related_concepts=PREREQUISITE_MAP.get(concept_name, []),
                last_practiced=None
            )
            db.add(concept)
            db.commit()
            db.refresh(concept)
        return concept

    @staticmethod
    def record_practice_evidence(
        db: Session,
        user_id: int,
        concepts_detected: List[str],
        is_successful: bool,
        mistakes_identified: Optional[List[str]] = None
    ) -> List[KnowledgeConcept]:
        """
        Updates personal technical memory with verified evidence from code analysis
        or assessment submission.
        """
        updated_concepts = []
        for name in concepts_detected:
            concept = KnowledgeService.get_or_create_concept(db, user_id, name)
            
            # Update counts strictly from verified practice
            old_count = concept.practice_count or 0
            new_count = old_count + 1
            concept.practice_count = new_count
            
            if old_count == 0:
                concept.success_rate = 1.0 if is_successful else 0.0
            else:
                weight = 1.0 / new_count
                concept.success_rate = round(concept.success_rate * (1.0 - weight) + (1.0 if is_successful else 0.0) * weight, 2)
            
            # Recalculate confidence
            base_conf = min(0.95, (concept.practice_count * 0.08) + (concept.success_rate * 0.5))
            concept.confidence = round(base_conf, 2)
            
            # Determine state transitions based on evidence
            if mistakes_identified and len(mistakes_identified) > 0:
                current_mistakes = list(concept.repeated_mistakes)
                for m in mistakes_identified:
                    if m not in current_mistakes:
                        current_mistakes.append(m)
                concept.repeated_mistakes = current_mistakes
                if not is_successful or len(current_mistakes) >= 2:
                    concept.status = "NEEDS_REVISION"
            elif concept.practice_count >= 5 and concept.success_rate >= 0.8:
                concept.status = "STRONG"
            elif concept.practice_count >= 2:
                concept.status = "PRACTICED"
            else:
                concept.status = "LEARNING"

            concept.last_practiced = datetime.utcnow()
            updated_concepts.append(concept)

        db.commit()
        return updated_concepts

    @staticmethod
    def get_knowledge_graph(db: Session, user_id: int) -> KnowledgeGraphResponse:
        """Constructs graph nodes and edges representing user's personal knowledge."""
        concepts = db.query(KnowledgeConcept).filter(KnowledgeConcept.user_id == user_id).all()
        
        nodes = []
        edges = []
        node_ids = set()

        for c in concepts:
            nodes.append(KnowledgeGraphNode(
                id=c.name,
                name=c.name,
                category=c.category,
                status=c.status,
                confidence=c.confidence,
                practice_count=c.practice_count,
                parent=c.parent_concept
            ))
            node_ids.add(c.name)

        # Generate structural edges
        for c in concepts:
            for related in (c.related_concepts or []):
                if related in node_ids:
                    edges.append(KnowledgeGraphEdge(
                        source=related,
                        target=c.name,
                        type="prerequisite"
                    ))

        # Overall stats
        strong_count = sum(1 for c in concepts if c.status == "STRONG")
        needs_revision_count = sum(1 for c in concepts if c.status == "NEEDS_REVISION")
        practiced_count = sum(1 for c in concepts if c.status == "PRACTICED")
        avg_confidence = round(sum(c.confidence for c in concepts) / max(len(concepts), 1), 2)

        stats = {
            "total_concepts": len(concepts),
            "strong": strong_count,
            "practiced": practiced_count,
            "needs_revision": needs_revision_count,
            "average_confidence": avg_confidence
        }

        return KnowledgeGraphResponse(nodes=nodes, edges=edges, links=edges, stats=stats)

    @staticmethod
    def get_user_concepts(db: Session, user_id: int) -> List[KnowledgeConcept]:
        return db.query(KnowledgeConcept).filter(KnowledgeConcept.user_id == user_id).all()

knowledge_service = KnowledgeService()

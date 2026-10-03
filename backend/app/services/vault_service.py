from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc
from app.models.models import KnowledgeVaultItem, KnowledgeConcept
from app.schemas.schemas import VaultItemCreate, VaultItemUpdate
from app.storage.file_storage import file_storage
from app.ai.orchestrator import ai_orchestrator

class VaultService:
    """Business logic for Knowledge Vault - Personal Technical Second Brain."""

    @staticmethod
    def create_item(db: Session, user_id: int, item_in: VaultItemCreate) -> KnowledgeVaultItem:
        # If AI analysis was not provided, optionally extract tags and concepts
        extracted_concepts = item_in.extracted_concepts or []
        ai_summary = item_in.ai_summary

        if not extracted_concepts or not ai_summary:
            try:
                analysis = ai_orchestrator.analyze_vault_item(
                    title=item_in.title,
                    content=item_in.content,
                    content_type=item_in.content_type
                )
                if not extracted_concepts:
                    extracted_concepts = analysis.get("extracted_concepts", [])
                if not ai_summary:
                    ai_summary = analysis.get("ai_summary", "")
                if not item_in.tags and analysis.get("tags"):
                    item_in.tags = analysis.get("tags", [])
                if item_in.topic == "General" and analysis.get("topic"):
                    item_in.topic = analysis.get("topic")
            except Exception:
                pass

        vault_item = KnowledgeVaultItem(
            user_id=user_id,
            content_type=item_in.content_type,
            title=item_in.title,
            content=item_in.content,
            file_path=item_in.file_path,
            file_name=item_in.file_name,
            file_size=item_in.file_size,
            mime_type=item_in.mime_type,
            topic=item_in.topic or "General",
            folder=item_in.folder or "Personal Reference",
            tags=item_in.tags or [],
            extracted_concepts=extracted_concepts,
            ai_summary=ai_summary,
            is_favorite=item_in.is_favorite or False
        )
        db.add(vault_item)
        db.commit()
        db.refresh(vault_item)
        return vault_item

    @staticmethod
    def get_items(
        db: Session,
        user_id: int,
        content_type: Optional[str] = None,
        folder: Optional[str] = None,
        topic: Optional[str] = None,
        is_favorite: Optional[bool] = None,
        search_query: Optional[str] = None,
        skip: int = 0,
        limit: int = 50
    ) -> List[KnowledgeVaultItem]:
        query = db.query(KnowledgeVaultItem).filter(
            KnowledgeVaultItem.user_id == user_id,
            KnowledgeVaultItem.is_archived == False
        )

        if content_type:
            query = query.filter(KnowledgeVaultItem.content_type == content_type)
        if folder:
            query = query.filter(KnowledgeVaultItem.folder == folder)
        if topic:
            query = query.filter(KnowledgeVaultItem.topic == topic)
        if is_favorite is not None:
            query = query.filter(KnowledgeVaultItem.is_favorite == is_favorite)

        if search_query:
            term = f"%{search_query.lower()}%"
            query = query.filter(
                or_(
                    KnowledgeVaultItem.title.ilike(term),
                    KnowledgeVaultItem.content.ilike(term),
                    KnowledgeVaultItem.topic.ilike(term),
                    KnowledgeVaultItem._tags.ilike(term),
                    KnowledgeVaultItem._extracted_concepts.ilike(term)
                )
            )

        return query.order_by(desc(KnowledgeVaultItem.created_at)).offset(skip).limit(limit).all()

    @staticmethod
    def get_item_by_id(db: Session, user_id: int, item_id: int) -> Optional[KnowledgeVaultItem]:
        return db.query(KnowledgeVaultItem).filter(
            KnowledgeVaultItem.id == item_id,
            KnowledgeVaultItem.user_id == user_id
        ).first()

    @staticmethod
    def update_item(db: Session, user_id: int, item_id: int, update_in: VaultItemUpdate) -> Optional[KnowledgeVaultItem]:
        item = VaultService.get_item_by_id(db, user_id, item_id)
        if not item:
            return None

        if update_in.title is not None:
            item.title = update_in.title
        if update_in.content is not None:
            item.content = update_in.content
        if update_in.topic is not None:
            item.topic = update_in.topic
        if update_in.folder is not None:
            item.folder = update_in.folder
        if update_in.tags is not None:
            item.tags = update_in.tags
        if update_in.is_favorite is not None:
            item.is_favorite = update_in.is_favorite
        if update_in.is_archived is not None:
            item.is_archived = update_in.is_archived

        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def delete_item(db: Session, user_id: int, item_id: int) -> bool:
        item = VaultService.get_item_by_id(db, user_id, item_id)
        if not item:
            return False

        if item.file_path:
            file_storage.delete_file(item.file_path)

        db.delete(item)
        db.commit()
        return True

    @staticmethod
    def ask_item(db: Session, user_id: int, item_id: int, question: str) -> Dict[str, Any]:
        item = VaultService.get_item_by_id(db, user_id, item_id)
        if not item:
            raise ValueError("Knowledge item not found.")

        return ai_orchestrator.ask_vault_document(document_content=item.content, question=question)

    @staticmethod
    def perform_ai_action(item_content: str, item_title: str, action: str) -> Dict[str, Any]:
        """Perform ad-hoc AI study action on saved material."""
        if action == "summarize":
            summary = ai_orchestrator.analyze_vault_item(title=item_title, content=item_content, content_type="note")
            return {"result": summary.get("ai_summary", item_content[:300])}
        elif action == "explain":
            reply = ai_orchestrator.answer_question(f"Explain this saved technical material clearly with an example: {item_content[:1500]}", {})
            return {"result": reply.get("reply", "")}
        elif action == "flashcards":
            return {
                "result": [
                    {"front": f"Core concept in {item_title}?", "back": "Focuses on state isolation, complexity optimization, and invariant preservation."},
                    {"front": "Where is this applied?", "back": "High-throughput backend architectures and competitive algorithmic problem-solving."}
                ]
            }
        return {"result": "Action completed successfully."}

    @staticmethod
    def get_revision_recommendations(db: Session, user_id: int) -> List[Dict[str, Any]]:
        """
        Smart Revision: Finds saved Vault items that directly assist with concepts
        marked as NEEDS_REVISION in Personal Knowledge Memory.
        """
        weak_concepts = db.query(KnowledgeConcept).filter(
            KnowledgeConcept.user_id == user_id,
            KnowledgeConcept.status.in_(["NEEDS_REVISION", "LEARNING"])
        ).all()

        recommendations = []
        for concept in weak_concepts:
            term = f"%{concept.name.lower()}%"
            matching_items = db.query(KnowledgeVaultItem).filter(
                KnowledgeVaultItem.user_id == user_id,
                or_(
                    KnowledgeVaultItem.title.ilike(term),
                    KnowledgeVaultItem.topic.ilike(term),
                    KnowledgeVaultItem._extracted_concepts.ilike(term)
                )
            ).limit(2).all()

            if matching_items:
                recommendations.append({
                    "concept": concept.name,
                    "reason": f"Marked as {concept.status}. You have saved reference material ready to review.",
                    "vault_items": [
                        {"id": v.id, "title": v.title, "content_type": v.content_type}
                        for v in matching_items
                    ]
                })

        return recommendations

vault_service = VaultService()

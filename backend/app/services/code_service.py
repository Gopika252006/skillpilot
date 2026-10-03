from typing import Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.models import CodeAnalysis
from app.schemas.schemas import CodeAnalyzeRequest, CodeAnalyzeResponse
from app.ai.context_builder import build_user_technical_context
from app.ai.orchestrator import ai_orchestrator
from app.services.knowledge_service import knowledge_service

class CodeService:
    """Manages Code Analyzer submissions, evaluations, and memory updates."""

    @staticmethod
    def analyze_and_record(db: Session, user_id: int, req: CodeAnalyzeRequest) -> CodeAnalyzeResponse:
        # 1. Build rich personal context
        user_context = build_user_technical_context(db, user_id)

        # 2. Invoke AI engine
        analysis_result = ai_orchestrator.analyze_code(
            problem_title=req.problem_title,
            problem_statement=req.problem_statement or "",
            language=req.language,
            user_code=req.user_code,
            user_context=user_context
        )

        # 3. Persist analysis history
        record = CodeAnalysis(
            user_id=user_id,
            problem_title=req.problem_title,
            problem_statement=req.problem_statement or "",
            language=req.language,
            user_code=req.user_code,
            approach_detected=analysis_result.get("approach_detected", "Algorithmic Solution"),
            is_correct=analysis_result.get("is_correct", True),
            time_complexity=analysis_result.get("time_complexity", "O(n)"),
            space_complexity=analysis_result.get("space_complexity", "O(1)"),
            code_quality_score=analysis_result.get("code_quality_score", 8),
            code_quality_summary=analysis_result.get("code_quality_summary", ""),
            concepts_detected=analysis_result.get("concepts_detected", []),
            strengths=analysis_result.get("strengths", []),
            improvements=analysis_result.get("improvements", []),
            optimization_suggestions=analysis_result.get("optimization_suggestions", []),
            suggested_concepts=analysis_result.get("suggested_concepts", []),
            hint_1=analysis_result.get("hint_1", "Look closely at your loop termination criteria."),
            hint_2=analysis_result.get("hint_2", "Can you preserve the state invariant with less space?"),
            deeper_explanation=analysis_result.get("deeper_explanation", "This solution leverages structured traversal."),
            optimized_approach=analysis_result.get("optimized_approach", ""),
            ai_model_used=analysis_result.get("ai_model_used", "local")
        )
        db.add(record)
        db.commit()
        db.refresh(record)

        # 4. EVIDENCE-DRIVEN KNOWLEDGE MEMORY UPDATE
        # Update user's personal knowledge profile based on this practice event
        concepts = analysis_result.get("concepts_detected", [])
        improvements = analysis_result.get("improvements", [])
        is_successful = analysis_result.get("is_correct", True)
        
        # Filter improvements for repeated mistake tracking
        potential_mistakes = [imp for imp in improvements if any(k in imp.lower() for k in ["overflow", "boundary", "nested", "edge", "null", "off-by-one"])]
        
        knowledge_service.record_practice_evidence(
            db=db,
            user_id=user_id,
            concepts_detected=concepts,
            is_successful=is_successful,
            mistakes_identified=potential_mistakes
        )

        return CodeAnalyzeResponse(
            id=record.id,
            problem_title=record.problem_title,
            language=record.language,
            approach_detected=record.approach_detected,
            is_correct=record.is_correct,
            time_complexity=record.time_complexity,
            space_complexity=record.space_complexity,
            code_quality_score=record.code_quality_score,
            code_quality_summary=record.code_quality_summary or "",
            concepts_detected=record.concepts_detected,
            strengths=record.strengths,
            improvements=record.improvements,
            optimization_suggestions=record.optimization_suggestions,
            suggested_concepts=record.suggested_concepts,
            hint_1=record.hint_1 or "",
            hint_2=record.hint_2 or "",
            deeper_explanation=record.deeper_explanation or "",
            optimized_approach=record.optimized_approach,
            ai_model_used=record.ai_model_used,
            created_at=record.created_at
        )

    @staticmethod
    def get_user_history(db: Session, user_id: int, limit: int = 20) -> List[CodeAnalysis]:
        return db.query(CodeAnalysis).filter(
            CodeAnalysis.user_id == user_id
        ).order_by(desc(CodeAnalysis.created_at)).limit(limit).all()

code_service = CodeService()

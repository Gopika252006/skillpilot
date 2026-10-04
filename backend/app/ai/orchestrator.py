import logging
from typing import Dict, Any, List
from app.ai.base import BaseAIProvider
from app.ai.ollama_provider import OllamaProvider
from app.ai.fallback_engine import FallbackInferenceEngine
from app.core.config import settings

logger = logging.getLogger(__name__)

class AIOrchestrator:
    """
    Orchestrates AI requests between local open-weight inference (Ollama)
    and robust local fallback engine.
    Ensures zero downtime, strict schema adherence, and clear observability.
    """
    def __init__(self):
        self.ollama = OllamaProvider(
            base_url=settings.OLLAMA_BASE_URL,
            model=settings.OLLAMA_MODEL,
            timeout=settings.AI_TIMEOUT_SECONDS
        )
        self.fallback = FallbackInferenceEngine()

    def get_status(self) -> Dict[str, Any]:
        """Check AI status for UI badges and Admin health checks."""
        ollama_ok = self.ollama.is_available()
        return {
            "status": "connected" if ollama_ok else "fallback_active",
            "active_runtime": "Ollama (Open-Weight)" if ollama_ok else "CodePilot Rule-Based Fallback (Offline-Ready)",
            "configured_model": settings.OLLAMA_MODEL,
            "base_url": settings.OLLAMA_BASE_URL,
            "privacy_guarantee": "100% Local / Zero external data transmission"
        }

    def analyze_code(self, problem_title: str, problem_statement: str, language: str, user_code: str, user_context: Dict[str, Any]) -> Dict[str, Any]:
        if self.ollama.is_available():
            try:
                res = self.ollama.analyze_code(problem_title, problem_statement, language, user_code, user_context)
                required = ["approach_detected", "time_complexity", "space_complexity", "code_quality_score"]
                if isinstance(res, dict) and all(k in res for k in required):
                    res["ai_model_used"] = f"ollama:{settings.OLLAMA_MODEL}"
                    return res
                logger.warning("Ollama analyze_code output schema validation failed, falling back to rule-based engine.")
            except Exception as e:
                logger.warning(f"Ollama execution failed, falling back to rule-based engine: {e}")
        
        res = self.fallback.analyze_code(problem_title, problem_statement, language, user_code, user_context)
        res["ai_model_used"] = "codepilot:rule-based-fallback"
        return res

    def answer_question(self, message: str, user_context: Dict[str, Any]) -> Dict[str, Any]:
        if self.ollama.is_available():
            try:
                res = self.ollama.answer_question(message, user_context)
                if isinstance(res, dict) and "reply" in res:
                    res["model_used"] = f"ollama:{settings.OLLAMA_MODEL}"
                    return res
                logger.warning("Ollama answer_question output schema validation failed, falling back to rule-based engine.")
            except Exception as e:
                logger.warning(f"Ollama Q&A failed, falling back to rule-based engine: {e}")

        res = self.fallback.answer_question(message, user_context)
        res["model_used"] = "codepilot:rule-based-fallback"
        return res

    def extract_concepts(self, text: str) -> List[str]:
        if self.ollama.is_available():
            try:
                return self.ollama.extract_concepts(text)
            except Exception:
                pass
        return self.fallback.extract_concepts(text)

    def generate_weekly_plan(self, user_context: Dict[str, Any]) -> Dict[str, Any]:
        if self.ollama.is_available():
            try:
                res = self.ollama.generate_weekly_plan(user_context)
                if isinstance(res, dict) and "tasks" in res and isinstance(res["tasks"], list):
                    return res
                logger.warning("Ollama weekly plan output validation failed, falling back to rule-based engine.")
            except Exception as e:
                logger.warning(f"Ollama weekly plan failed: {e}")
        return self.fallback.generate_weekly_plan(user_context)

    def evaluate_assessment(self, questions: List[Dict[str, Any]], answers: Dict[str, Any], user_context: Dict[str, Any]) -> Dict[str, Any]:
        if self.ollama.is_available():
            try:
                res = self.ollama.evaluate_assessment(questions, answers, user_context)
                if isinstance(res, dict) and "score" in res:
                    return res
                logger.warning("Ollama assessment evaluation validation failed, falling back to rule-based engine.")
            except Exception as e:
                logger.warning(f"Ollama assessment evaluation failed: {e}")
        return self.fallback.evaluate_assessment(questions, answers, user_context)

    def evaluate_interview_answer(self, question: str, user_answer: str, user_context: Dict[str, Any]) -> Dict[str, Any]:
        if self.ollama.is_available():
            try:
                res = self.ollama.evaluate_interview_answer(question, user_answer, user_context)
                if isinstance(res, dict) and "score" in res:
                    return res
                logger.warning("Ollama interview evaluation validation failed, falling back to rule-based engine.")
            except Exception as e:
                logger.warning(f"Ollama interview answer evaluation failed: {e}")
        return self.fallback.evaluate_interview_answer(question, user_answer, user_context)

    def generate_career_analysis(self, user_context: Dict[str, Any]) -> Dict[str, Any]:
        if self.ollama.is_available():
            try:
                res = self.ollama.generate_career_analysis(user_context)
                if isinstance(res, dict) and "readiness_score" in res:
                    return res
                logger.warning("Ollama career analysis validation failed, falling back to rule-based engine.")
            except Exception as e:
                logger.warning(f"Ollama career analysis failed: {e}")
        return self.fallback.generate_career_analysis(user_context)

    def analyze_vault_item(self, title: str, content: str, content_type: str) -> Dict[str, Any]:
        if self.ollama.is_available():
            try:
                res = self.ollama.analyze_vault_item(title, content, content_type)
                if isinstance(res, dict) and "topic" in res:
                    return res
                logger.warning("Ollama vault analysis validation failed, falling back to rule-based engine.")
            except Exception as e:
                logger.warning(f"Ollama vault analysis failed: {e}")
        return self.fallback.analyze_vault_item(title, content, content_type)

    def ask_vault_document(self, document_content: str, question: str) -> Dict[str, Any]:
        if self.ollama.is_available():
            try:
                res = self.ollama.ask_vault_document(document_content, question)
                if isinstance(res, dict) and "answer" in res:
                    return res
                logger.warning("Ollama document ask validation failed, falling back to rule-based engine.")
            except Exception as e:
                logger.warning(f"Ollama document ask failed: {e}")
        return self.fallback.ask_vault_document(document_content, question)

ai_orchestrator = AIOrchestrator()

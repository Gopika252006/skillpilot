from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

class BaseAIProvider(ABC):
    """Abstract base class for all CodePilot AI model providers."""

    @abstractmethod
    def analyze_code(self, problem_title: str, problem_statement: str, language: str, user_code: str, user_context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze code for approach, complexity, correctness, concepts, and progressive hints."""
        pass

    @abstractmethod
    def answer_question(self, message: str, user_context: Dict[str, Any]) -> Dict[str, Any]:
        """Context-aware technical Q&A using user's personal knowledge profile."""
        pass

    @abstractmethod
    def extract_concepts(self, text: str) -> List[str]:
        """Extract normalized technical concepts from notes or learning logs."""
        pass

    @abstractmethod
    def generate_weekly_plan(self, user_context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Monday-style adaptive weekly plan targeting weak spots."""
        pass

    @abstractmethod
    def evaluate_assessment(self, questions: List[Dict[str, Any]], answers: Dict[str, Any], user_context: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate weekend assessment, detect gaps, recommend next week focus."""
        pass

    @abstractmethod
    def evaluate_interview_answer(self, question: str, user_answer: str, user_context: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate verbal/technical interview response and suggest follow-up."""
        pass

    @abstractmethod
    def generate_career_analysis(self, user_context: Dict[str, Any]) -> Dict[str, Any]:
        """Perform skill gap analysis between current skills and target role."""
        pass

    @abstractmethod
    def analyze_vault_item(self, title: str, content: str, content_type: str) -> Dict[str, Any]:
        """Extract topic, tags, concepts and summary for a saved vault item."""
        pass

    @abstractmethod
    def ask_vault_document(self, document_content: str, question: str) -> Dict[str, Any]:
        """Grounded Q&A over a specific saved document."""
        pass

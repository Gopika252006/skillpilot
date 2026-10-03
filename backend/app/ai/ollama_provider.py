import json
import logging
import requests
from typing import Dict, Any, List
from app.ai.base import BaseAIProvider
from app.core.config import settings

logger = logging.getLogger(__name__)

class OllamaProvider(BaseAIProvider):
    """
    Open-weight model provider utilizing local Ollama runtime.
    Supports models such as llama3.2:3b, qwen2.5-coder:7b, mistral, deepseek-r1, etc.
    """
    def __init__(self, base_url: str = None, model: str = None, timeout: int = None):
        self.base_url = (base_url or settings.OLLAMA_BASE_URL).rstrip("/")
        self.model = model or settings.OLLAMA_MODEL
        self.timeout = timeout or settings.AI_TIMEOUT_SECONDS

    def _query(self, system_prompt: str, user_prompt: str) -> Dict[str, Any]:
        """Send prompt to Ollama with JSON formatting requirement."""
        endpoint = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "system": system_prompt,
            "prompt": user_prompt,
            "stream": False,
            "format": "json",
            "options": {
                "temperature": 0.2,
                "top_p": 0.9
            }
        }
        resp = requests.post(endpoint, json=payload, timeout=self.timeout)
        resp.raise_for_status()
        data = resp.json()
        response_text = data.get("response", "").strip()
        
        # Parse JSON output from model
        try:
            return json.loads(response_text)
        except json.JSONDecodeError:
            # Try finding JSON block
            if "{" in response_text and "}" in response_text:
                start = response_text.find("{")
                end = response_text.rfind("}") + 1
                return json.loads(response_text[start:end])
            raise ValueError(f"Ollama response was not valid JSON: {response_text[:100]}...")

    def is_available(self) -> bool:
        """Check if local Ollama daemon is responsive and model is ready."""
        try:
            r = requests.get(f"{self.base_url}/api/tags", timeout=2)
            return r.status_code == 200
        except Exception:
            return False

    def analyze_code(self, problem_title: str, problem_statement: str, language: str, user_code: str, user_context: Dict[str, Any]) -> Dict[str, Any]:
        system_prompt = (
            "You are CodePilot AI, an elite technical mentor. You analyze code submissions critically, "
            "evaluating approach, correctness, Big-O complexity, concepts used, code quality, and progressive learning hints. "
            "Do NOT dump the full solution upfront; provide progressive hints to encourage deep learning. "
            "Return valid JSON matching this schema:\n"
            "{\n"
            '  "approach_detected": "string",\n'
            '  "is_correct": boolean,\n'
            '  "time_complexity": "O(...)",\n'
            '  "space_complexity": "O(...)",\n'
            '  "code_quality_score": integer (1-10),\n'
            '  "code_quality_summary": "string",\n'
            '  "concepts_detected": ["string"],\n'
            '  "strengths": ["string"],\n'
            '  "improvements": ["string"],\n'
            '  "optimization_suggestions": ["string"],\n'
            '  "suggested_concepts": ["string"],\n'
            '  "hint_1": "string (gentle nudge)",\n'
            '  "hint_2": "string (algorithmic guidance)",\n'
            '  "deeper_explanation": "string",\n'
            '  "optimized_approach": "string description"\n'
            "}"
        )
        user_prompt = f"""
{user_context.get('prompt_block', '')}

PROBLEM: {problem_title}
STATEMENT: {problem_statement or 'Standard LeetCode / competitive programming problem'}
LANGUAGE: {language}
USER CODE:
```{language}
{user_code}
```
Analyze this solution now.
"""
        return self._query(system_prompt, user_prompt)

    def answer_question(self, message: str, user_context: Dict[str, Any]) -> Dict[str, Any]:
        system_prompt = (
            "You are CodePilot, a personal technical AI companion that knows what the user knows. "
            "Use the user's specific background, strong skills, weak concepts, and recent coding history to explain technical topics. "
            "For example: 'Since you already know recursion well, think of Dynamic Programming as...'. "
            "Never pretend to know things not in context. "
            "Return valid JSON:\n"
            "{\n"
            '  "reply": "string (markdown allowed)",\n'
            '  "context_used": ["string explaining how personalization was applied"],\n'
            '  "suggested_followups": ["string"]\n'
            "}"
        )
        user_prompt = f"""
{user_context.get('prompt_block', '')}

USER QUESTION: {message}
"""
        return self._query(system_prompt, user_prompt)

    def extract_concepts(self, text: str) -> List[str]:
        system_prompt = (
            "Extract 2 to 6 specific computer science / software engineering technical concepts from this text. "
            "Return JSON: {\"concepts\": [\"Concept1\", \"Concept2\"]}"
        )
        res = self._query(system_prompt, f"TEXT: {text}")
        return res.get("concepts", [])

    def generate_weekly_plan(self, user_context: Dict[str, Any]) -> Dict[str, Any]:
        system_prompt = (
            "Generate a Monday-to-Sunday 15-20 min/day adaptive technical learning plan. "
            "Target the user's weak concepts, recurring mistakes, and career direction. "
            "Return JSON:\n"
            "{\n"
            '  "week_title": "string",\n'
            '  "focus_area": "string",\n'
            '  "rationale": "string",\n'
            '  "tasks": [\n'
            '    {"day_of_week": "Monday", "title": "string", "description": "string", "target_concept": "string", "estimated_minutes": 15}\n'
            '  ]\n'
            "}"
        )
        return self._query(system_prompt, user_context.get('prompt_block', ''))

    def evaluate_assessment(self, questions: List[Dict[str, Any]], answers: Dict[str, Any], user_context: Dict[str, Any]) -> Dict[str, Any]:
        system_prompt = (
            "Evaluate test answers. Score out of 100. Provide strong areas, weak areas, and recommendations. "
            "Return JSON: {\"score\": 85, \"feedback_summary\": \"...\", \"strong_areas\": [...], \"weak_areas\": [...], \"next_week_recommendations\": [...]}"
        )
        user_prompt = f"QUESTIONS: {json.dumps(questions)}\nANSWERS: {json.dumps(answers)}"
        return self._query(system_prompt, user_prompt)

    def evaluate_interview_answer(self, question: str, user_answer: str, user_context: Dict[str, Any]) -> Dict[str, Any]:
        system_prompt = (
            "Evaluate the user's technical interview answer. Assess correctness, clarity, depth, and give a follow-up question. "
            "Return JSON: {\"score\": 8.5, \"clarity_feedback\": \"...\", \"technical_depth_feedback\": \"...\", \"follow_up_question\": \"...\"}"
        )
        user_prompt = f"QUESTION: {question}\nANSWER: {user_answer}"
        return self._query(system_prompt, user_prompt)

    def generate_career_analysis(self, user_context: Dict[str, Any]) -> Dict[str, Any]:
        system_prompt = (
            "Compare user's current proven skills with their target role. "
            "Return JSON: {\"readiness_score\": 75, \"strong_skills\": [...], \"gap_skills\": [...], \"recommended_actions\": [{\"skill\": \"...\", \"why\": \"...\", \"priority\": \"High\"}], \"recommended_projects\": [{\"title\": \"...\", \"description\": \"...\", \"skills\": [...], \"why\": \"...\"}], \"recommended_certifications\": [{\"title\": \"...\", \"why\": \"...\"}]}"
        )
        return self._query(system_prompt, user_context.get('prompt_block', ''))

    def analyze_vault_item(self, title: str, content: str, content_type: str) -> Dict[str, Any]:
        system_prompt = (
            "Analyze saved technical knowledge item. Extract topic, tags, technical concepts, and a 2-sentence summary. "
            "Return JSON: {\"topic\": \"...\", \"tags\": [...], \"extracted_concepts\": [...], \"ai_summary\": \"...\"}"
        )
        user_prompt = f"TITLE: {title}\nTYPE: {content_type}\nCONTENT:\n{content[:2000]}"
        return self._query(system_prompt, user_prompt)

    def ask_vault_document(self, document_content: str, question: str) -> Dict[str, Any]:
        system_prompt = (
            "Answer the question using the provided document as primary ground truth. "
            "Clearly distinguish between facts directly in the document vs general background knowledge. "
            "Return JSON: {\"answer\": \"...\", \"sources_found\": boolean, \"key_quotes\": [...]}"
        )
        user_prompt = f"DOCUMENT CONTENT:\n{document_content[:4000]}\n\nQUESTION: {question}"
        return self._query(system_prompt, user_prompt)

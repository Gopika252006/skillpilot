from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.models import AptitudeAttempt

APTITUDE_DAILY_QUESTIONS = [
    {
        "id": 1,
        "category": "Quantitative",
        "question": "A pipeline processes 120 messages per second with 3 worker instances. If worker capacity degrades by 25% and traffic spikes by 50%, how many total workers are required to sustain the load without queue overflow?",
        "options": ["4 workers", "5 workers", "6 workers", "7 workers"],
        "correct_option": 2,
        "explanation": "Normal worker capacity = 120 / 3 = 40 msg/s. Degraded capacity = 40 * 0.75 = 30 msg/s. Spiked traffic = 120 * 1.5 = 180 msg/s. Workers required = 180 / 30 = 6 workers."
    },
    {
        "id": 2,
        "category": "Logical Reasoning",
        "question": "Statement: If a database uses write-ahead logging (WAL), then crash recovery is guaranteed. In which of the following cases is the statement definitively violated?",
        "options": [
            "The DB uses WAL and crash recovery succeeds.",
            "The DB does NOT use WAL and crash recovery succeeds.",
            "The DB uses WAL and crash recovery fails.",
            "The DB does NOT use WAL and crash recovery fails."
        ],
        "correct_option": 2,
        "explanation": "A conditional P -> Q is false if and only if P is true and Q is false (Uses WAL, but recovery fails)."
    },
    {
        "id": 3,
        "category": "Quantitative",
        "question": "An API has a cache hit ratio of 80%. Cache lookup takes 2ms, while database query takes 50ms. What is the average latency of the API endpoint?",
        "options": ["11.6 ms", "12.0 ms", "10.0 ms", "8.4 ms"],
        "correct_option": 0,
        "explanation": "Average latency = (0.80 * 2ms) + (0.20 * (2ms + 50ms)) = 1.6 + 10.4 = 12.0ms or if DB query already includes cache lookup check = 0.80*2 + 0.20*50 = 1.6 + 10.0 = 11.6ms."
    },
    {
        "id": 4,
        "category": "Verbal Reasoning",
        "question": "Choose the word most nearly opposite in meaning to 'EPHEMERAL' in the context of storage architecture:",
        "options": ["Volatile", "Persistent", "Stateless", "Distributed"],
        "correct_option": 1,
        "explanation": "'Ephemeral' means lasting for a very short time (temporary/volatile). The direct opposite in systems engineering is 'Persistent'."
    },
    {
        "id": 5,
        "category": "Logical Reasoning",
        "question": "Five microservices A, B, C, D, E have dependencies: A depends on B and C. C depends on D. D depends on E. B has no dependencies. Which service must be initialized first?",
        "options": ["A", "B", "C", "E"],
        "correct_option": 3,
        "explanation": "Topological sort: D depends on E, C depends on D, A depends on C. Therefore E has no internal dependencies in that chain and can be initialized first."
    }
]

class AptitudeService:
    """Manages lightweight daily 5-question aptitude sprints."""

    @staticmethod
    def get_daily_sprint() -> List[Dict[str, Any]]:
        return APTITUDE_DAILY_QUESTIONS

    @staticmethod
    def record_attempt(
        db: Session,
        user_id: int,
        question_idx: int,
        selected_option: int,
        time_taken_seconds: int
    ) -> Dict[str, Any]:
        if question_idx < 0 or question_idx >= len(APTITUDE_DAILY_QUESTIONS):
            raise ValueError("Invalid question index.")

        q = APTITUDE_DAILY_QUESTIONS[question_idx]
        is_correct = (selected_option == q["correct_option"])

        attempt = AptitudeAttempt(
            user_id=user_id,
            category=q["category"],
            question=q["question"],
            selected_option=selected_option,
            correct_option=q["correct_option"],
            is_correct=is_correct,
            explanation=q["explanation"],
            time_taken_seconds=time_taken_seconds
        )
        attempt.options = q["options"]
        db.add(attempt)
        db.commit()

        return {
            "is_correct": is_correct,
            "correct_option": q["correct_option"],
            "explanation": q["explanation"]
        }

    @staticmethod
    def get_stats(db: Session, user_id: int) -> Dict[str, Any]:
        attempts = db.query(AptitudeAttempt).filter(AptitudeAttempt.user_id == user_id).all()
        total = len(attempts)
        correct = sum(1 for a in attempts if a.is_correct)
        accuracy = round((correct / max(total, 1)) * 100, 1)

        return {
            "total_attempts": total,
            "correct": correct,
            "accuracy": accuracy,
            "recent": [
                {"category": a.category, "is_correct": a.is_correct, "time": a.time_taken_seconds}
                for a in attempts[-5:]
            ]
        }

aptitude_service = AptitudeService()

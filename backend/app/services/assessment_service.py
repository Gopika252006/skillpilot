from datetime import datetime
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.models import Assessment, WeeklyPlan
from app.schemas.schemas import AssessmentOut, AssessmentSubmitRequest
from app.ai.context_builder import build_user_technical_context
from app.ai.orchestrator import ai_orchestrator
from app.services.knowledge_service import knowledge_service

# Default high-yield assessment questions mapped by topic
QUESTION_BANK = [
    {
        "id": 1,
        "topic": "Binary Search",
        "question": "What is the key loop invariant when using while (low <= high) versus while (low < high) in binary search?",
        "options": [
            "while (low <= high) implies the search interval is closed [low, high], meaning mid could be a valid candidate on the last single-element check.",
            "while (low <= high) is only valid for arrays of even length.",
            "while (low < high) eliminates the need for calculating mid.",
            "There is no algorithmic difference; it is purely syntactical."
        ],
        "correct_option": 0,
        "explanation": "In a closed interval [low, high], when low == high, there is still one element left to inspect."
    },
    {
        "id": 2,
        "topic": "Sliding Window",
        "question": "When is an expanding and shrinking two-pointer window guaranteed to achieve O(n) total time complexity?",
        "options": [
            "Only when the elements are sorted.",
            "When both left and right pointers only move monotonically forward across the array at most N times each.",
            "When a nested while loop checks all elements backwards on every expansion.",
            "Only when using extra O(n) hash table auxiliary storage."
        ],
        "correct_option": 1,
        "explanation": "Because each pointer advances at most N times, the amortized work across the entire algorithm is bounded by 2N = O(n)."
    },
    {
        "id": 3,
        "topic": "Dynamic Programming",
        "question": "What property differentiates Dynamic Programming from Divide and Conquer?",
        "options": [
            "Divide and conquer operates in O(1) space, while DP always requires O(n^2).",
            "DP handles overlapping subproblems by caching state transitions, whereas divide and conquer solves disjoint subproblems independently.",
            "Divide and conquer cannot be solved recursively.",
            "DP is only applicable to graph data structures."
        ],
        "correct_option": 1,
        "explanation": "Overlapping subproblems + optimal substructure are the definitive hallmarks of Dynamic Programming."
    },
    {
        "id": 4,
        "topic": "System Design",
        "question": "Under the CAP theorem, what is the trade-off during a network partition in a distributed key-value store?",
        "options": [
            "You must trade off either Consistency (returning stale/differing data) or Availability (returning an error/refusing writes).",
            "Network partitions can be eliminated by adding more CPU cores.",
            "Partition tolerance is optional in distributed networks.",
            "Latency is prioritized over network packets."
        ],
        "correct_option": 0,
        "explanation": "When network partition P occurs, the system must choose between CP (consistent, unavailable nodes) or AP (available, but stale)."
    },
    {
        "id": 5,
        "topic": "Caching",
        "question": "In a Write-Through caching pattern, how are updates handled?",
        "options": [
            "Data is written only to cache and flushed to disk once daily.",
            "Data is written simultaneously to both the cache and the backing database before the write call returns success.",
            "The client writes directly to the DB and invalidates the cache asynchronously.",
            "Updates are queued into an event stream and eventually dropped if cache memory is full."
        ],
        "correct_option": 1,
        "explanation": "Write-through ensures strict synchronization between cache and DB at the expense of slightly higher write latency."
    }
]

class AssessmentService:
    """Manages weekend assessments and evidence-driven adaptive scoring."""

    @staticmethod
    def get_or_create_weekly_assessment(db: Session, user_id: int) -> Assessment:
        # Check for existing pending assessment
        existing = db.query(Assessment).filter(
            Assessment.user_id == user_id,
            Assessment.status == "PENDING"
        ).first()

        if existing:
            return existing

        # Generate new assessment
        topics = ["Binary Search", "Sliding Window", "Dynamic Programming", "System Design", "Caching"]
        assessment = Assessment(
            user_id=user_id,
            title="Weekly Synthesis & Boundary Assessment",
            status="PENDING",
            total_score=100.0
        )
        assessment.topics = topics
        assessment.questions = QUESTION_BANK
        assessment.user_answers = {}
        
        db.add(assessment)
        db.commit()
        db.refresh(assessment)
        return assessment

    @staticmethod
    def submit_assessment(db: Session, user_id: int, assessment_id: int, answers: Dict[str, Any]) -> Assessment:
        assessment = db.query(Assessment).filter(
            Assessment.id == assessment_id,
            Assessment.user_id == user_id
        ).first()

        if not assessment:
            raise ValueError("Assessment not found.")

        user_context = build_user_technical_context(db, user_id)
        eval_result = ai_orchestrator.evaluate_assessment(
            questions=assessment.questions,
            answers=answers,
            user_context=user_context
        )

        assessment.status = "COMPLETED"
        assessment.score = eval_result.get("score", 80.0)
        assessment.feedback_summary = eval_result.get("feedback_summary", "Assessment completed.")
        assessment.strong_areas = eval_result.get("strong_areas", [])
        assessment.weak_areas = eval_result.get("weak_areas", [])
        assessment.next_week_recommendations = eval_result.get("next_week_recommendations", [])
        assessment.user_answers = answers
        assessment.completed_at = datetime.utcnow()

        db.commit()
        db.refresh(assessment)

        # Update Personal Knowledge Profile with this test evidence
        tested_concepts = assessment.topics or []
        is_success = assessment.score >= 70.0
        knowledge_service.record_practice_evidence(
            db=db,
            user_id=user_id,
            concepts_detected=tested_concepts,
            is_successful=is_success,
            mistakes_identified=assessment.weak_areas
        )

        return assessment

assessment_service = AssessmentService()

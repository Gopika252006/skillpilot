from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.models.models import InterviewSession, InterviewExchange
from app.ai.context_builder import build_user_technical_context
from app.ai.orchestrator import ai_orchestrator

INTERVIEW_STARTER_QUESTIONS = {
    "Backend Software Engineer": [
        "Explain how database indexing using B+ Trees works, and why B+ trees are preferred over binary search trees for disk storage.",
        "How would you handle idempotency in a distributed payment processing API?",
        "Describe the mechanics of JWT authentication and how you would implement token revocation securely."
    ],
    "General": [
        "Can you walk me through the trade-offs between memoization and tabulation in Dynamic Programming?",
        "How do you determine whether a graph problem requires Breadth-First Search versus Depth-First Search?",
        "Explain how a hash collision is handled in modern standard libraries."
    ]
}

class InterviewService:
    """Manages adaptive verbal/technical interview sessions."""

    @staticmethod
    def start_session(db: Session, user_id: int, topic: str = "DSA & Backend Architecture") -> InterviewSession:
        user_context = build_user_technical_context(db, user_id)
        target_role = user_context.get("target_role", "Backend Software Engineer")

        questions = INTERVIEW_STARTER_QUESTIONS.get(target_role, INTERVIEW_STARTER_QUESTIONS["General"])

        session = InterviewSession(
            user_id=user_id,
            target_role=target_role,
            topic=topic,
            status="IN_PROGRESS"
        )
        db.add(session)
        db.commit()
        db.refresh(session)

        # Create first question exchange
        first_q = questions[0]
        exchange = InterviewExchange(
            session_id=session.id,
            question_number=1,
            question=first_q
        )
        db.add(exchange)
        db.commit()
        db.refresh(session)
        return session

    @staticmethod
    def submit_answer(
        db: Session,
        user_id: int,
        session_id: int,
        question_number: int,
        user_answer: str
    ) -> Dict[str, Any]:
        session = db.query(InterviewSession).filter(
            InterviewSession.id == session_id,
            InterviewSession.user_id == user_id
        ).first()

        if not session:
            raise ValueError("Interview session not found.")

        exchange = db.query(InterviewExchange).filter(
            InterviewExchange.session_id == session_id,
            InterviewExchange.question_number == question_number
        ).first()

        if not exchange:
            raise ValueError("Exchange question not found.")

        user_context = build_user_technical_context(db, user_id)
        eval_result = ai_orchestrator.evaluate_interview_answer(
            question=exchange.question,
            user_answer=user_answer,
            user_context=user_context
        )

        exchange.user_answer = user_answer
        exchange.score = eval_result.get("score", 7.5)
        exchange.ai_feedback = f"{eval_result.get('clarity_feedback', '')} {eval_result.get('technical_depth_feedback', '')}".strip()
        exchange.follow_up_question = eval_result.get("follow_up_question")

        db.commit()

        # Check if next question is needed or complete session
        target_role = session.target_role
        role_questions = INTERVIEW_STARTER_QUESTIONS.get(target_role, INTERVIEW_STARTER_QUESTIONS["General"])
        
        is_finished = (question_number >= len(role_questions))
        next_question = None

        if not is_finished:
            next_q_text = role_questions[question_number]
            next_exchange = InterviewExchange(
                session_id=session_id,
                question_number=question_number + 1,
                question=next_q_text
            )
            db.add(next_exchange)
            db.commit()
            next_question = next_q_text
        else:
            session.status = "COMPLETED"
            all_exchanges = db.query(InterviewExchange).filter(InterviewExchange.session_id == session_id).all()
            avg_score = round(sum(e.score or 7.0 for e in all_exchanges) / max(len(all_exchanges), 1), 1)
            session.overall_score = avg_score
            session.clarity_feedback = "Consistently demonstrated clear structure and articulated trade-offs."
            session.technical_depth_feedback = "Strong mastery of fundamental concepts and algorithmic reasoning."
            db.commit()

        return {
            "session_id": session_id,
            "question_number": question_number,
            "score": exchange.score,
            "feedback": exchange.ai_feedback,
            "follow_up_question": exchange.follow_up_question,
            "next_question": next_question,
            "is_completed": is_finished
        }

    @staticmethod
    def get_session(db: Session, user_id: int, session_id: int) -> Optional[InterviewSession]:
        return db.query(InterviewSession).filter(
            InterviewSession.id == session_id,
            InterviewSession.user_id == user_id
        ).first()

interview_service = InterviewService()

import json
from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Text, Boolean, Float, DateTime, ForeignKey, Index
)
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(String(50), default="USER", nullable=False)  # "USER" or "ADMIN"
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    concepts = relationship("KnowledgeConcept", back_populates="user", cascade="all, delete-orphan")
    code_analyses = relationship("CodeAnalysis", back_populates="user", cascade="all, delete-orphan")
    learning_logs = relationship("LearningLog", back_populates="user", cascade="all, delete-orphan")
    vault_items = relationship("KnowledgeVaultItem", back_populates="user", cascade="all, delete-orphan")
    weekly_plans = relationship("WeeklyPlan", back_populates="user", cascade="all, delete-orphan")
    assessments = relationship("Assessment", back_populates="user", cascade="all, delete-orphan")
    aptitude_attempts = relationship("AptitudeAttempt", back_populates="user", cascade="all, delete-orphan")
    interview_sessions = relationship("InterviewSession", back_populates="user", cascade="all, delete-orphan")
    chat_messages = relationship("ChatMessage", back_populates="user", cascade="all, delete-orphan")
    career_profile = relationship("CareerProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")


class UserProfile(Base):
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    target_role = Column(String(100), default="Backend Software Engineer")
    experience_level = Column(String(50), default="Intermediate")
    learning_goals = Column(Text, default="Master advanced DSA, system design, and distributed systems.")
    weekly_hours = Column(Integer, default=7)
    _current_technologies = Column("current_technologies", Text, default="[]")
    _interests = Column("interests", Text, default="[]")
    onboarding_completed = Column(Boolean, default=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="profile")
    
    @property
    def current_technologies(self):
        try:
            return json.loads(self._current_technologies or "[]")
        except Exception:
            return []
            
    @current_technologies.setter
    def current_technologies(self, val):
        self._current_technologies = json.dumps(val or [])

    @property
    def interests(self):
        try:
            return json.loads(self._interests or "[]")
        except Exception:
            return []
            
    @interests.setter
    def interests(self, val):
        self._interests = json.dumps(val or [])


class KnowledgeConcept(Base):
    __tablename__ = "knowledge_concepts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(150), nullable=False, index=True)
    category = Column(String(100), nullable=False, index=True)  # DSA, System Design, Backend, Core CS, etc.
    parent_concept = Column(String(150), nullable=True)
    status = Column(String(50), default="NOT_STARTED", nullable=False)  # NOT_STARTED, LEARNING, PRACTICED, STRONG, NEEDS_REVISION
    confidence = Column(Float, default=0.0)  # 0.0 to 1.0
    practice_count = Column(Integer, default=0)
    success_rate = Column(Float, default=0.0)
    _repeated_mistakes = Column("repeated_mistakes", Text, default="[]")
    _related_concepts = Column("related_concepts", Text, default="[]")
    last_practiced = Column(DateTime, nullable=True)
    last_revised = Column(DateTime, nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="concepts")
    
    __table_args__ = (
        Index("idx_user_concept", "user_id", "name", unique=True),
    )
    
    @property
    def repeated_mistakes(self):
        try:
            return json.loads(self._repeated_mistakes or "[]")
        except Exception:
            return []
            
    @repeated_mistakes.setter
    def repeated_mistakes(self, val):
        self._repeated_mistakes = json.dumps(val or [])

    @property
    def related_concepts(self):
        try:
            return json.loads(self._related_concepts or "[]")
        except Exception:
            return []
            
    @related_concepts.setter
    def related_concepts(self, val):
        self._related_concepts = json.dumps(val or [])


class CodeAnalysis(Base):
    __tablename__ = "code_analyses"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    problem_title = Column(String(255), nullable=False)
    problem_statement = Column(Text, nullable=True)
    language = Column(String(50), nullable=False)  # python, java, cpp, javascript
    user_code = Column(Text, nullable=False)
    approach_detected = Column(String(255), nullable=False)
    is_correct = Column(Boolean, default=True)
    time_complexity = Column(String(100), nullable=False)
    space_complexity = Column(String(100), nullable=False)
    code_quality_score = Column(Integer, default=8)  # 1 - 10
    code_quality_summary = Column(Text, nullable=True)
    _concepts_detected = Column("concepts_detected", Text, default="[]")
    _strengths = Column("strengths", Text, default="[]")
    _improvements = Column("improvements", Text, default="[]")
    _optimization_suggestions = Column("optimization_suggestions", Text, default="[]")
    _suggested_concepts = Column("suggested_concepts", Text, default="[]")
    hint_1 = Column(Text, nullable=True)
    hint_2 = Column(Text, nullable=True)
    deeper_explanation = Column(Text, nullable=True)
    optimized_approach = Column(Text, nullable=True)
    ai_model_used = Column(String(100), default="ollama:llama3.2:3b")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="code_analyses")
    
    @property
    def concepts_detected(self):
        try:
            return json.loads(self._concepts_detected or "[]")
        except Exception:
            return []
            
    @concepts_detected.setter
    def concepts_detected(self, val):
        self._concepts_detected = json.dumps(val or [])

    @property
    def strengths(self):
        try:
            return json.loads(self._strengths or "[]")
        except Exception:
            return []
            
    @strengths.setter
    def strengths(self, val):
        self._strengths = json.dumps(val or [])

    @property
    def improvements(self):
        try:
            return json.loads(self._improvements or "[]")
        except Exception:
            return []
            
    @improvements.setter
    def improvements(self, val):
        self._improvements = json.dumps(val or [])

    @property
    def optimization_suggestions(self):
        try:
            return json.loads(self._optimization_suggestions or "[]")
        except Exception:
            return []
            
    @optimization_suggestions.setter
    def optimization_suggestions(self, val):
        self._optimization_suggestions = json.dumps(val or [])

    @property
    def suggested_concepts(self):
        try:
            return json.loads(self._suggested_concepts or "[]")
        except Exception:
            return []
            
    @suggested_concepts.setter
    def suggested_concepts(self, val):
        self._suggested_concepts = json.dumps(val or [])


class LearningLog(Base):
    __tablename__ = "learning_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    topic = Column(String(200), nullable=False)
    notes = Column(Text, nullable=False)
    source = Column(String(200), nullable=True)
    time_spent_mins = Column(Integer, default=20)
    confidence_rating = Column(Integer, default=3)  # 1 - 5
    _extracted_concepts = Column("extracted_concepts", Text, default="[]")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="learning_logs")
    
    @property
    def extracted_concepts(self):
        try:
            return json.loads(self._extracted_concepts or "[]")
        except Exception:
            return []
            
    @extracted_concepts.setter
    def extracted_concepts(self, val):
        self._extracted_concepts = json.dumps(val or [])


class KnowledgeVaultItem(Base):
    __tablename__ = "knowledge_vault_items"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    content_type = Column(String(50), nullable=False)  # note, document, image, formula, code, link, ai_answer
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    file_path = Column(String(500), nullable=True)
    file_name = Column(String(255), nullable=True)
    file_size = Column(Integer, nullable=True)
    mime_type = Column(String(100), nullable=True)
    topic = Column(String(100), default="General", index=True)
    folder = Column(String(100), default="Personal Reference", index=True)
    _tags = Column("tags", Text, default="[]")
    _extracted_concepts = Column("extracted_concepts", Text, default="[]")
    ai_summary = Column(Text, nullable=True)
    is_favorite = Column(Boolean, default=False)
    is_archived = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="vault_items")
    
    @property
    def tags(self):
        try:
            return json.loads(self._tags or "[]")
        except Exception:
            return []
            
    @tags.setter
    def tags(self, val):
        self._tags = json.dumps(val or [])

    @property
    def extracted_concepts(self):
        try:
            return json.loads(self._extracted_concepts or "[]")
        except Exception:
            return []
            
    @extracted_concepts.setter
    def extracted_concepts(self, val):
        self._extracted_concepts = json.dumps(val or [])


class WeeklyPlan(Base):
    __tablename__ = "weekly_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    week_title = Column(String(200), nullable=False)
    focus_area = Column(String(150), nullable=False)
    rationale = Column(Text, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="weekly_plans")
    tasks = relationship("WeeklyTask", back_populates="plan", cascade="all, delete-orphan")


class WeeklyTask(Base):
    __tablename__ = "weekly_tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("weekly_plans.id", ondelete="CASCADE"), nullable=False)
    day_of_week = Column(String(50), nullable=False)  # Monday, Tuesday, etc.
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    target_concept = Column(String(150), nullable=True)
    estimated_minutes = Column(Integer, default=20)
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)
    
    plan = relationship("WeeklyPlan", back_populates="tasks")


class Assessment(Base):
    __tablename__ = "assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(200), nullable=False)
    _topics = Column("topics", Text, default="[]")
    _questions = Column("questions", Text, default="[]")
    _user_answers = Column("user_answers", Text, default="{}")
    score = Column(Float, nullable=True)
    total_score = Column(Float, default=100.0)
    feedback_summary = Column(Text, nullable=True)
    _strong_areas = Column("strong_areas", Text, default="[]")
    _weak_areas = Column("weak_areas", Text, default="[]")
    _next_week_recommendations = Column("next_week_recommendations", Text, default="[]")
    status = Column(String(50), default="PENDING")  # PENDING, COMPLETED
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    
    user = relationship("User", back_populates="assessments")
    
    @property
    def topics(self):
        try:
            return json.loads(self._topics or "[]")
        except Exception:
            return []
            
    @topics.setter
    def topics(self, val):
        self._topics = json.dumps(val or [])

    @property
    def questions(self):
        try:
            return json.loads(self._questions or "[]")
        except Exception:
            return []
            
    @questions.setter
    def questions(self, val):
        self._questions = json.dumps(val or [])

    @property
    def user_answers(self):
        try:
            return json.loads(self._user_answers or "{}")
        except Exception:
            return {}
            
    @user_answers.setter
    def user_answers(self, val):
        self._user_answers = json.dumps(val or {})

    @property
    def strong_areas(self):
        try:
            return json.loads(self._strong_areas or "[]")
        except Exception:
            return []
            
    @strong_areas.setter
    def strong_areas(self, val):
        self._strong_areas = json.dumps(val or [])

    @property
    def weak_areas(self):
        try:
            return json.loads(self._weak_areas or "[]")
        except Exception:
            return []
            
    @weak_areas.setter
    def weak_areas(self, val):
        self._weak_areas = json.dumps(val or [])

    @property
    def next_week_recommendations(self):
        try:
            return json.loads(self._next_week_recommendations or "[]")
        except Exception:
            return []
            
    @next_week_recommendations.setter
    def next_week_recommendations(self, val):
        self._next_week_recommendations = json.dumps(val or [])


class AptitudeAttempt(Base):
    __tablename__ = "aptitude_attempts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    category = Column(String(100), nullable=False)  # Quantitative, Logical Reasoning, Verbal
    question = Column(Text, nullable=False)
    _options = Column("options", Text, default="[]")
    selected_option = Column(Integer, nullable=False)
    correct_option = Column(Integer, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    explanation = Column(Text, nullable=True)
    time_taken_seconds = Column(Integer, default=45)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="aptitude_attempts")
    
    @property
    def options(self):
        try:
            return json.loads(self._options or "[]")
        except Exception:
            return []
            
    @options.setter
    def options(self, val):
        self._options = json.dumps(val or [])


class InterviewSession(Base):
    __tablename__ = "interview_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    target_role = Column(String(100), nullable=False)
    topic = Column(String(150), nullable=False)
    status = Column(String(50), default="IN_PROGRESS")  # IN_PROGRESS, COMPLETED
    overall_score = Column(Float, nullable=True)
    clarity_feedback = Column(Text, nullable=True)
    technical_depth_feedback = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="interview_sessions")
    exchanges = relationship("InterviewExchange", back_populates="session", cascade="all, delete-orphan")


class InterviewExchange(Base):
    __tablename__ = "interview_exchanges"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("interview_sessions.id", ondelete="CASCADE"), nullable=False)
    question_number = Column(Integer, nullable=False)
    question = Column(Text, nullable=False)
    user_answer = Column(Text, nullable=True)
    ai_feedback = Column(Text, nullable=True)
    score = Column(Float, nullable=True)
    follow_up_question = Column(Text, nullable=True)
    
    session = relationship("InterviewSession", back_populates="exchanges")


class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String(20), nullable=False)  # "user" or "assistant"
    content = Column(Text, nullable=False)
    _context_used = Column("context_used", Text, default="[]")
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="chat_messages")
    
    @property
    def context_used(self):
        try:
            return json.loads(self._context_used or "[]")
        except Exception:
            return []
            
    @context_used.setter
    def context_used(self, val):
        self._context_used = json.dumps(val or [])


class CareerProfile(Base):
    __tablename__ = "career_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    target_role = Column(String(100), default="Backend Software Engineer")
    readiness_score = Column(Float, default=72.0)  # percentage
    _strong_skills = Column("strong_skills", Text, default="[]")
    _gap_skills = Column("gap_skills", Text, default="[]")
    _recommended_actions = Column("recommended_actions", Text, default="[]")
    _recommended_projects = Column("recommended_projects", Text, default="[]")
    _recommended_certifications = Column("recommended_certifications", Text, default="[]")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="career_profile")
    
    @property
    def strong_skills(self):
        try:
            return json.loads(self._strong_skills or "[]")
        except Exception:
            return []
            
    @strong_skills.setter
    def strong_skills(self, val):
        self._strong_skills = json.dumps(val or [])

    @property
    def gap_skills(self):
        try:
            return json.loads(self._gap_skills or "[]")
        except Exception:
            return []
            
    @gap_skills.setter
    def gap_skills(self, val):
        self._gap_skills = json.dumps(val or [])

    @property
    def recommended_actions(self):
        try:
            return json.loads(self._recommended_actions or "[]")
        except Exception:
            return []
            
    @recommended_actions.setter
    def recommended_actions(self, val):
        self._recommended_actions = json.dumps(val or [])

    @property
    def recommended_projects(self):
        try:
            return json.loads(self._recommended_projects or "[]")
        except Exception:
            return []
            
    @recommended_projects.setter
    def recommended_projects(self, val):
        self._recommended_projects = json.dumps(val or [])

    @property
    def recommended_certifications(self):
        try:
            return json.loads(self._recommended_certifications or "[]")
        except Exception:
            return []
            
    @recommended_certifications.setter
    def recommended_certifications(self, val):
        self._recommended_certifications = json.dumps(val or [])

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

# --- Auth Schemas ---
class UserRegister(BaseModel):
    email: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)
    full_name: str = Field(..., min_length=2)
    role: Optional[str] = "USER"

class UserLogin(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: Dict[str, Any]

class UserOut(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# --- Profile & Onboarding ---
class UserProfileUpdate(BaseModel):
    target_role: Optional[str] = None
    experience_level: Optional[str] = None
    learning_goals: Optional[str] = None
    weekly_hours: Optional[int] = None
    current_technologies: Optional[List[str]] = None
    interests: Optional[List[str]] = None
    onboarding_completed: Optional[bool] = None

class UserProfileOut(BaseModel):
    id: int
    user_id: int
    target_role: str
    experience_level: str
    learning_goals: str
    weekly_hours: int
    current_technologies: List[str]
    interests: List[str]
    onboarding_completed: bool
    updated_at: datetime

    class Config:
        from_attributes = True

# --- Code Analyzer ---
class CodeAnalyzeRequest(BaseModel):
    problem_title: str = Field(..., min_length=2)
    problem_statement: Optional[str] = ""
    language: str = Field(..., pattern="^(python|java|cpp|javascript)$")
    user_code: str = Field(..., min_length=5)
    expected_approach: Optional[str] = None

class CodeAnalyzeResponse(BaseModel):
    id: Optional[int] = None
    problem_title: str
    language: str
    approach_detected: str
    is_correct: bool
    time_complexity: str
    space_complexity: str
    code_quality_score: int
    code_quality_summary: str
    concepts_detected: List[str]
    strengths: List[str]
    improvements: List[str]
    optimization_suggestions: List[str]
    suggested_concepts: List[str]
    hint_1: str
    hint_2: str
    deeper_explanation: str
    optimized_approach: Optional[str] = None
    ai_model_used: str
    created_at: Optional[datetime] = None

# --- Knowledge Concept & Memory ---
class ConceptOut(BaseModel):
    id: int
    name: str
    category: str
    parent_concept: Optional[str] = None
    status: str
    confidence: float
    practice_count: int
    success_rate: float
    repeated_mistakes: List[str]
    related_concepts: List[str]
    last_practiced: Optional[datetime] = None
    last_revised: Optional[datetime] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True

class KnowledgeGraphNode(BaseModel):
    id: str
    name: str
    category: str
    status: str
    confidence: float
    practice_count: int
    parent: Optional[str] = None

class KnowledgeGraphEdge(BaseModel):
    source: str
    target: str
    type: str  # "prerequisite", "parent_child", "related"

class KnowledgeGraphResponse(BaseModel):
    nodes: List[KnowledgeGraphNode]
    edges: List[KnowledgeGraphEdge]
    links: Optional[List[KnowledgeGraphEdge]] = None
    stats: Dict[str, Any]

# --- Knowledge Vault ---
class VaultItemCreate(BaseModel):
    content_type: str = Field(..., pattern="^(note|document|image|formula|code|link|ai_answer)$")
    title: str = Field(..., min_length=1)
    content: str = Field(...)
    topic: Optional[str] = "General"
    folder: Optional[str] = "Personal Reference"
    tags: Optional[List[str]] = []
    file_path: Optional[str] = None
    file_name: Optional[str] = None
    file_size: Optional[int] = None
    mime_type: Optional[str] = None
    extracted_concepts: Optional[List[str]] = []
    ai_summary: Optional[str] = None
    is_favorite: Optional[bool] = False

class VaultItemUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    topic: Optional[str] = None
    folder: Optional[str] = None
    tags: Optional[List[str]] = None
    is_favorite: Optional[bool] = None
    is_archived: Optional[bool] = None

class VaultItemOut(BaseModel):
    id: int
    content_type: str
    title: str
    content: str
    file_name: Optional[str] = None
    file_size: Optional[int] = None
    mime_type: Optional[str] = None
    topic: str
    folder: str
    tags: List[str]
    extracted_concepts: List[str]
    ai_summary: Optional[str] = None
    is_favorite: bool
    is_archived: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class VaultAskRequest(BaseModel):
    item_id: Optional[int] = None
    question: str

class VaultActionRequest(BaseModel):
    action: str  # summarize, extract_concepts, explain, flashcards, formula_explain
    content: Optional[str] = None

# --- Learning Log ---
class LearningLogCreate(BaseModel):
    topic: str = Field(..., min_length=2)
    notes: str = Field(..., min_length=5)
    source: Optional[str] = "Self Study"
    time_spent_mins: Optional[int] = 20
    confidence_rating: Optional[int] = 3

class LearningLogOut(BaseModel):
    id: int
    topic: str
    notes: str
    source: Optional[str]
    time_spent_mins: int
    confidence_rating: int
    extracted_concepts: List[str]
    created_at: datetime

    class Config:
        from_attributes = True

# --- Weekly Plan ---
class WeeklyTaskOut(BaseModel):
    id: int
    day_of_week: str
    title: str
    description: Optional[str]
    target_concept: Optional[str]
    estimated_minutes: int
    is_completed: bool
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True

class WeeklyPlanOut(BaseModel):
    id: int
    week_title: str
    focus_area: str
    rationale: str
    is_active: bool
    tasks: List[WeeklyTaskOut]

    class Config:
        from_attributes = True

# --- Assessment ---
class AssessmentSubmitRequest(BaseModel):
    answers: Dict[str, Any]  # question_id -> selected_option or text answer

class AssessmentOut(BaseModel):
    id: int
    title: str
    topics: List[str]
    questions: List[Dict[str, Any]]
    score: Optional[float]
    total_score: float
    feedback_summary: Optional[str]
    strong_areas: List[str]
    weak_areas: List[str]
    next_week_recommendations: List[str]
    status: str
    created_at: datetime
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True

# --- Aptitude ---
class AptitudeSubmitRequest(BaseModel):
    question_index: int
    selected_option: int
    time_taken_seconds: int

# --- Ask My AI Chat ---
class ChatRequest(BaseModel):
    message: str
    active_code: Optional[str] = None
    current_topic: Optional[str] = None

class ChatResponse(BaseModel):
    reply: str
    context_used: List[str]
    suggested_followups: List[str]
    model_used: str

# --- Interview ---
class InterviewStartRequest(BaseModel):
    topic: Optional[str] = "DSA & Backend Architecture"

class InterviewAnswerRequest(BaseModel):
    session_id: int
    question_number: int
    user_answer: str

# --- Career & Recommendations ---
class CareerProfileOut(BaseModel):
    target_role: str
    readiness_score: float
    strong_skills: List[str]
    gap_skills: List[str]
    recommended_actions: List[Dict[str, Any]]
    recommended_projects: List[Dict[str, Any]]
    recommended_certifications: List[Dict[str, Any]]

# --- Admin ---
class AdminStatsOut(BaseModel):
    total_users: int
    active_users: int
    total_code_analyses: int
    total_vault_items: int
    total_learning_logs: int
    system_health: str
    ai_status: str
    active_model: str

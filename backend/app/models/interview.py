"""
Interview session models
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class PersonaType(str, Enum):
    """User persona types"""
    CONFUSED = "confused"
    EFFICIENT = "efficient"
    CHATTY = "chatty"
    EDGE_CASE = "edge_case"
    NORMAL = "normal"

class QuestionType(str, Enum):
    """Question types"""
    TECHNICAL = "technical"
    BEHAVIORAL = "behavioral"
    SITUATIONAL = "situational"
    EXPERIENCE = "experience"

class InterviewQuestion(BaseModel):
    """Single interview question"""
    question_id: int
    question_text: str
    question_type: QuestionType
    related_to: Optional[str] = None  # Which resume section it relates to
    expected_elements: List[str] = []  # What a good answer should contain
    difficulty: str = "medium"  # easy, medium, hard

class Answer(BaseModel):
    """User's answer to a question"""
    question_id: int
    answer_text: str
    duration_seconds: float
    timestamp: datetime = Field(default_factory=datetime.now)
    word_count: int = 0
    
class FollowUpQuestion(BaseModel):
    """Follow-up question after initial answer"""
    text: str
    reason: str  # Why this follow-up was generated
    type: str  # probe, redirect, hint, challenge

class QuestionSession(BaseModel):
    """Session for a single question"""
    question: InterviewQuestion
    initial_answer: Optional[Answer] = None
    follow_ups: List[Dict[str, Any]] = []  # {question: str, answer: str}
    persona_detected: PersonaType = PersonaType.NORMAL
    evaluation: Optional[Dict[str, Any]] = None

class InterviewSession(BaseModel):
    """Complete interview session"""
    session_id: str
    user_name: Optional[str] = None
    target_role: str = "Software Engineer"
    resume_summary: str = ""
    questions: List[QuestionSession] = []
    current_question_index: int = 0
    start_time: datetime = Field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    status: str = "in_progress"  # in_progress, completed, cancelled
    
class StartInterviewRequest(BaseModel):
    """Request to start interview"""
    session_id: str
    target_role: str = "Software Engineer"
    
class SubmitAnswerRequest(BaseModel):
    """Request to submit an answer"""
    session_id: str
    question_id: int
    answer_text: str
    duration_seconds: float
    is_voice: bool = False

class SubmitAnswerResponse(BaseModel):
    """Response after submitting answer"""
    success: bool
    follow_up_question: Optional[FollowUpQuestion] = None
    next_question: Optional[InterviewQuestion] = None
    is_interview_complete: bool = False
    message: str = ""

"""
Report data models
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime

class ScoreBreakdown(BaseModel):
    """Detailed score breakdown"""
    confidence: float = Field(ge=0, le=100)
    communication: float = Field(ge=0, le=100)
    technical_depth: float = Field(ge=0, le=100)
    star_method_usage: float = Field(ge=0, le=100)
    behavioral_clarity: float = Field(ge=0, le=100)
    overall: float = Field(ge=0, le=100)

class STARAnalysis(BaseModel):
    """STAR method analysis for an answer"""
    situation_present: bool
    task_present: bool
    action_present: bool
    result_present: bool
    score: float = Field(ge=0, le=100)
    feedback: str

class QuestionEvaluation(BaseModel):
    """Evaluation for a single question"""
    question_id: int
    question_text: str
    answer_text: str
    word_count: int
    duration_seconds: float
    relevance_score: float = Field(ge=0, le=100)
    confidence_score: float = Field(ge=0, le=100)
    technical_depth_score: float = Field(ge=0, le=100)
    star_analysis: Optional[STARAnalysis] = None
    persona_detected: str
    strengths: List[str] = []
    weaknesses: List[str] = []
    feedback: str

class PerformanceReport(BaseModel):
    """Complete performance report"""
    session_id: str
    candidate_name: Optional[str] = None
    target_role: str
    interview_date: datetime
    duration_minutes: float
    
    # Overall scores
    scores: ScoreBreakdown
    
    # Question-by-question evaluation
    question_evaluations: List[QuestionEvaluation] = []
    
    # Summary analysis
    overall_strengths: List[str] = []
    overall_weaknesses: List[str] = []
    improvement_suggestions: List[str] = []
    
    # Persona summary
    dominant_persona: str
    persona_distribution: Dict[str, int] = {}
    
    # Behavioral analysis
    star_method_consistency: str  # consistent, inconsistent, not_used
    communication_style: str  # concise, verbose, unclear
    
    # Final recommendation
    recommendation_level: str  # Beginner, Intermediate, Strong
    ready_for_interviews: bool
    recommended_next_steps: List[str] = []
    
    # Metadata
    report_generated_at: datetime = Field(default_factory=datetime.now)
    
class ReportGenerationRequest(BaseModel):
    """Request to generate report"""
    session_id: str
    export_format: str = "json"  # json, pdf, both

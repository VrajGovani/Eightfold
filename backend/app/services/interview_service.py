"""
Interview Service - Core business logic for interview management
"""
import logging
import uuid
from typing import Dict, Optional
from datetime import datetime

from app.models.resume import ResumeData
from app.models.interview import (
    InterviewSession, QuestionSession, Answer,
    PersonaType, SubmitAnswerResponse, FollowUpQuestion
)
from app.agents.question_generator import QuestionGenerator
from app.agents.persona_detector import PersonaDetector
from app.agents.response_evaluator import ResponseEvaluator
from app.agents.followup_engine import FollowUpEngine
from app.agents.star_checker import STARChecker
from app.services.llm_service import LLMService
from app.config import settings

logger = logging.getLogger(__name__)

class InterviewService:
    """Manages interview sessions and logic"""
    
    def __init__(self):
        self.llm = LLMService()
        self.question_gen = QuestionGenerator(self.llm)
        self.persona_detector = PersonaDetector(self.llm)
        self.response_eval = ResponseEvaluator(self.llm)
        self.followup_engine = FollowUpEngine(self.llm)
        self.star_checker = STARChecker(self.llm)
        
        # In-memory session storage (use database in production)
        self.sessions: Dict[str, InterviewSession] = {}
        self.session_evaluations: Dict[str, list] = {}
    
    async def start_interview(
        self,
        session_id: str,
        resume_data: ResumeData,
        target_role: str
    ) -> InterviewSession:
        """Start a new interview session"""
        
        # Generate questions based on resume
        questions = await self.question_gen.generate_questions(resume_data, target_role)
        
        # Create session
        session = InterviewSession(
            session_id=session_id,
            user_name=resume_data.name,
            target_role=target_role,
            resume_summary=self._create_resume_summary(resume_data),
            questions=[QuestionSession(question=q) for q in questions],
            current_question_index=0,
            status="in_progress"
        )
        
        # Store session
        self.sessions[session_id] = session
        self.session_evaluations[session_id] = []
        
        logger.info(f"Started interview session {session_id} for {target_role}")
        return session
    
    def get_current_question(self, session_id: str):
        """Get the current question for a session"""
        session = self.sessions.get(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        if session.current_question_index >= len(session.questions):
            return None
        
        return session.questions[session.current_question_index].question
    
    async def submit_answer(
        self,
        session_id: str,
        question_id: int,
        answer_text: str,
        duration_seconds: float,
        is_voice: bool = False
    ) -> SubmitAnswerResponse:
        """Process submitted answer and generate response"""
        
        session = self.sessions.get(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        # Validate time limit
        if duration_seconds > settings.ANSWER_TIME_SECONDS:
            return SubmitAnswerResponse(
                success=False,
                message="Answer exceeded time limit. Moving to next question.",
                is_interview_complete=False
            )
        
        # Get current question session
        q_session = session.questions[session.current_question_index]
        
        # Create answer object
        word_count = len(answer_text.split())
        answer = Answer(
            question_id=question_id,
            answer_text=answer_text,
            duration_seconds=duration_seconds,
            word_count=word_count
        )
        
        # Store answer
        q_session.initial_answer = answer
        
        # Detect persona
        persona = await self.persona_detector.detect_persona(
            q_session.question.question_text,
            answer_text,
            duration_seconds,
            word_count
        )
        q_session.persona_detected = persona
        
        # Evaluate response
        evaluation = await self.response_eval.evaluate(
            q_session.question.question_text,
            answer_text,
            q_session.question.expected_elements,
            persona
        )
        
        # Check STAR pattern
        star_analysis = await self.star_checker.check_star_pattern(
            q_session.question.question_text,
            answer_text
        )
        evaluation["star_analysis"] = star_analysis
        evaluation["word_count"] = word_count
        evaluation["persona"] = persona.value
        
        # Store evaluation
        q_session.evaluation = evaluation
        self.session_evaluations[session_id].append(evaluation)
        
        # Generate follow-up if needed
        follow_up = await self.followup_engine.generate_follow_up(
            q_session.question.question_text,
            answer_text,
            evaluation,
            persona
        )
        
        if follow_up:
            # Add follow-up to session
            q_session.follow_ups.append({
                "question": follow_up.text,
                "answer": None,
                "type": follow_up.type
            })
            
            return SubmitAnswerResponse(
                success=True,
                follow_up_question=follow_up,
                message="Follow-up question generated",
                is_interview_complete=False
            )
        
        # Move to next question
        session.current_question_index += 1
        
        # Check if interview is complete
        if session.current_question_index >= len(session.questions):
            session.status = "completed"
            session.end_time = datetime.now()
            
            return SubmitAnswerResponse(
                success=True,
                message="Interview completed!",
                is_interview_complete=True
            )
        
        # Return next question
        next_question = session.questions[session.current_question_index].question
        
        return SubmitAnswerResponse(
            success=True,
            next_question=next_question,
            message="Answer submitted successfully",
            is_interview_complete=False
        )
    
    async def submit_followup_answer(
        self,
        session_id: str,
        answer_text: str,
        duration_seconds: float
    ) -> SubmitAnswerResponse:
        """Process follow-up answer"""
        
        session = self.sessions.get(session_id)
        if not session:
            raise ValueError(f"Session {session_id} not found")
        
        # Get current question session
        q_session = session.questions[session.current_question_index]
        
        # Store follow-up answer
        if q_session.follow_ups:
            q_session.follow_ups[-1]["answer"] = answer_text
        
        # Move to next question
        session.current_question_index += 1
        
        # Check if interview is complete
        if session.current_question_index >= len(session.questions):
            session.status = "completed"
            session.end_time = datetime.now()
            
            return SubmitAnswerResponse(
                success=True,
                message="Interview completed!",
                is_interview_complete=True
            )
        
        # Return next question
        next_question = session.questions[session.current_question_index].question
        
        return SubmitAnswerResponse(
            success=True,
            next_question=next_question,
            message="Follow-up answer submitted",
            is_interview_complete=False
        )
    
    def get_session(self, session_id: str) -> Optional[InterviewSession]:
        """Get session by ID"""
        return self.sessions.get(session_id)
    
    def get_session_evaluations(self, session_id: str) -> list:
        """Get all evaluations for a session"""
        return self.session_evaluations.get(session_id, [])
    
    def _create_resume_summary(self, resume_data: ResumeData) -> str:
        """Create a brief resume summary"""
        parts = []
        
        if resume_data.name:
            parts.append(f"Name: {resume_data.name}")
        
        if resume_data.skills:
            skills_str = ", ".join([s.name for s in resume_data.skills[:5]])
            parts.append(f"Skills: {skills_str}")
        
        if resume_data.experiences:
            exp = resume_data.experiences[0]
            parts.append(f"Recent: {exp.title} at {exp.company}")
        
        return " | ".join(parts)

# Global service instance
interview_service = InterviewService()

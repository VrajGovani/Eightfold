"""
Report Generator - Creates comprehensive performance reports
"""
import logging
from typing import List, Dict
from datetime import datetime
from app.models.report import (
    PerformanceReport, ScoreBreakdown, QuestionEvaluation, 
    STARAnalysis
)
from app.models.interview import InterviewSession, PersonaType
from app.services.llm_service import LLMService

logger = logging.getLogger(__name__)

class ReportGenerator:
    """Generates comprehensive interview performance reports"""
    
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service
    
    async def generate_report(
        self,
        session: InterviewSession,
        all_evaluations: List[Dict]
    ) -> PerformanceReport:
        """Generate complete performance report"""
        
        # Calculate scores
        scores = self._calculate_scores(all_evaluations)
        
        # Create question evaluations
        question_evals = self._create_question_evaluations(session, all_evaluations)
        
        # Analyze persona distribution
        persona_dist = self._analyze_persona_distribution(all_evaluations)
        dominant_persona = max(persona_dist, key=persona_dist.get)
        
        # Analyze STAR consistency
        star_consistency = self._analyze_star_consistency(all_evaluations)
        
        # Analyze communication style
        comm_style = self._analyze_communication_style(all_evaluations)
        
        # Generate insights using LLM
        insights = await self._generate_insights(
            session, all_evaluations, scores, dominant_persona
        )
        
        # Calculate duration
        duration_minutes = 0
        if session.end_time and session.start_time:
            duration_minutes = (session.end_time - session.start_time).total_seconds() / 60
        
        # Determine recommendation level
        rec_level, ready = self._determine_recommendation(scores.overall)
        
        report = PerformanceReport(
            session_id=session.session_id,
            candidate_name=session.user_name,
            target_role=session.target_role,
            interview_date=session.start_time,
            duration_minutes=duration_minutes,
            scores=scores,
            question_evaluations=question_evals,
            overall_strengths=insights.get("strengths", []),
            overall_weaknesses=insights.get("weaknesses", []),
            improvement_suggestions=insights.get("suggestions", []),
            dominant_persona=dominant_persona,
            persona_distribution=persona_dist,
            star_method_consistency=star_consistency,
            communication_style=comm_style,
            recommendation_level=rec_level,
            ready_for_interviews=ready,
            recommended_next_steps=insights.get("next_steps", [])
        )
        
        logger.info(f"Generated report for session {session.session_id}, score: {scores.overall}/100")
        return report
    
    def _calculate_scores(self, all_evaluations: List[Dict]) -> ScoreBreakdown:
        """Calculate aggregate scores"""
        
        if not all_evaluations:
            return ScoreBreakdown(
                confidence=50.0,
                communication=50.0,
                technical_depth=50.0,
                star_method_usage=0.0,
                behavioral_clarity=50.0,
                overall=50.0
            )
        
        # Average scores across all questions
        confidence_scores = []
        technical_scores = []
        clarity_scores = []
        star_scores = []
        relevance_scores = []
        
        for eval_data in all_evaluations:
            confidence_scores.append(eval_data.get("confidence_score", 50))
            technical_scores.append(eval_data.get("technical_depth_score", 50))
            clarity_scores.append(eval_data.get("clarity_score", 50))
            relevance_scores.append(eval_data.get("relevance_score", 50))
            
            star_analysis = eval_data.get("star_analysis", {})
            star_scores.append(star_analysis.get("score", 0))
        
        confidence = sum(confidence_scores) / len(confidence_scores)
        technical = sum(technical_scores) / len(technical_scores)
        communication = sum(clarity_scores) / len(clarity_scores)
        star = sum(star_scores) / len(star_scores) if star_scores else 0
        behavioral = sum(relevance_scores) / len(relevance_scores)
        
        overall = (confidence * 0.25 + technical * 0.25 + communication * 0.25 + 
                  star * 0.15 + behavioral * 0.10)
        
        return ScoreBreakdown(
            confidence=round(confidence, 2),
            communication=round(communication, 2),
            technical_depth=round(technical, 2),
            star_method_usage=round(star, 2),
            behavioral_clarity=round(behavioral, 2),
            overall=round(overall, 2)
        )
    
    def _create_question_evaluations(
        self,
        session: InterviewSession,
        all_evaluations: List[Dict]
    ) -> List[QuestionEvaluation]:
        """Create detailed question evaluations"""
        
        question_evals = []
        
        for i, q_session in enumerate(session.questions):
            if i >= len(all_evaluations):
                continue
            
            eval_data = all_evaluations[i]
            answer = q_session.initial_answer
            
            if not answer:
                continue
            
            star_data = eval_data.get("star_analysis", {})
            star_analysis = STARAnalysis(
                situation_present=star_data.get("situation_present", False),
                task_present=star_data.get("task_present", False),
                action_present=star_data.get("action_present", False),
                result_present=star_data.get("result_present", False),
                score=star_data.get("score", 0),
                feedback=star_data.get("feedback", "")
            )
            
            q_eval = QuestionEvaluation(
                question_id=q_session.question.question_id,
                question_text=q_session.question.question_text,
                answer_text=answer.answer_text,
                word_count=answer.word_count,
                duration_seconds=answer.duration_seconds,
                relevance_score=eval_data.get("relevance_score", 50),
                confidence_score=eval_data.get("confidence_score", 50),
                technical_depth_score=eval_data.get("technical_depth_score", 50),
                star_analysis=star_analysis,
                persona_detected=q_session.persona_detected.value,
                strengths=eval_data.get("strengths", []),
                weaknesses=eval_data.get("weaknesses", []),
                feedback=eval_data.get("feedback", "")
            )
            
            question_evals.append(q_eval)
        
        return question_evals
    
    def _analyze_persona_distribution(self, all_evaluations: List[Dict]) -> Dict[str, int]:
        """Analyze persona distribution"""
        
        distribution = {
            "confused": 0,
            "efficient": 0,
            "chatty": 0,
            "edge_case": 0,
            "normal": 0
        }
        
        for eval_data in all_evaluations:
            persona = eval_data.get("persona", "normal")
            if persona in distribution:
                distribution[persona] += 1
        
        return distribution
    
    def _analyze_star_consistency(self, all_evaluations: List[Dict]) -> str:
        """Analyze STAR method consistency"""
        
        star_scores = []
        for eval_data in all_evaluations:
            star_analysis = eval_data.get("star_analysis", {})
            star_scores.append(star_analysis.get("score", 0))
        
        if not star_scores:
            return "not_used"
        
        avg_score = sum(star_scores) / len(star_scores)
        
        if avg_score >= 70:
            return "consistent"
        elif avg_score >= 40:
            return "inconsistent"
        else:
            return "not_used"
    
    def _analyze_communication_style(self, all_evaluations: List[Dict]) -> str:
        """Analyze overall communication style"""
        
        word_counts = []
        clarity_scores = []
        
        for eval_data in all_evaluations:
            word_counts.append(eval_data.get("word_count", 0))
            clarity_scores.append(eval_data.get("clarity_score", 50))
        
        avg_words = sum(word_counts) / len(word_counts) if word_counts else 0
        avg_clarity = sum(clarity_scores) / len(clarity_scores) if clarity_scores else 50
        
        if avg_words > 200:
            return "verbose"
        elif avg_words < 50:
            return "terse"
        elif avg_clarity >= 75:
            return "concise"
        else:
            return "unclear"
    
    async def _generate_insights(
        self,
        session: InterviewSession,
        all_evaluations: List[Dict],
        scores: ScoreBreakdown,
        dominant_persona: str
    ) -> Dict[str, List[str]]:
        """Generate insights using LLM"""
        
        # Summarize evaluation data
        eval_summary = self._summarize_evaluations(all_evaluations)
        
        prompt = f"""Generate comprehensive interview feedback insights.

Target Role: {session.target_role}
Overall Score: {scores.overall}/100
Dominant Persona: {dominant_persona}

Score Breakdown:
- Confidence: {scores.confidence}/100
- Communication: {scores.communication}/100
- Technical Depth: {scores.technical_depth}/100
- STAR Method: {scores.star_method_usage}/100
- Behavioral Clarity: {scores.behavioral_clarity}/100

Evaluation Summary:
{eval_summary}

Generate:
1. Top 3-5 overall strengths
2. Top 3-5 areas for improvement
3. 5-7 specific, actionable improvement suggestions
4. 3-5 recommended next steps

Return JSON:
{{
    "strengths": ["Strength 1", "Strength 2", ...],
    "weaknesses": ["Weakness 1", "Weakness 2", ...],
    "suggestions": ["Do X to improve Y", ...],
    "next_steps": ["Practice X", "Study Y", ...]
}}"""
        
        try:
            response = await self.llm.generate(prompt, temperature=0.7)
            
            import json
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
                insights = json.loads(json_str)
            elif "```" in response:
                json_str = response.split("```")[1].split("```")[0].strip()
                insights = json.loads(json_str)
            else:
                insights = json.loads(response)
            
            return insights
            
        except Exception as e:
            logger.error(f"Error generating insights: {str(e)}")
            return self._get_fallback_insights(scores)
    
    def _summarize_evaluations(self, all_evaluations: List[Dict]) -> str:
        """Create a text summary of evaluations"""
        
        lines = []
        for i, eval_data in enumerate(all_evaluations, 1):
            lines.append(f"Q{i}: Relevance {eval_data.get('relevance_score', 50)}, "
                        f"Confidence {eval_data.get('confidence_score', 50)}, "
                        f"Depth {eval_data.get('technical_depth_score', 50)}")
        
        return "\n".join(lines)
    
    def _get_fallback_insights(self, scores: ScoreBreakdown) -> Dict[str, List[str]]:
        """Fallback insights if generation fails"""
        
        return {
            "strengths": ["Completed all interview questions", "Provided thoughtful responses"],
            "weaknesses": ["Could improve technical depth", "Practice STAR method"],
            "suggestions": [
                "Practice answering with the STAR method structure",
                "Prepare specific examples from past experiences",
                "Study technical concepts in more depth",
                "Record yourself answering questions to improve clarity"
            ],
            "next_steps": [
                "Do 5 more practice interviews",
                "Review common interview questions for your role",
                "Practice explaining technical concepts clearly"
            ]
        }
    
    def _determine_recommendation(self, overall_score: float) -> tuple:
        """Determine recommendation level and readiness"""
        
        if overall_score >= 75:
            return "Strong", True
        elif overall_score >= 60:
            return "Intermediate", True
        elif overall_score >= 45:
            return "Intermediate", False
        else:
            return "Beginner", False

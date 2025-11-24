"""
STAR Pattern Checker - Detects STAR method usage in answers
"""
import logging
import json
from typing import Dict
from app.services.llm_service import LLMService

logger = logging.getLogger(__name__)

class STARChecker:
    """Analyzes responses for STAR method (Situation, Task, Action, Result)"""
    
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service
    
    async def check_star_pattern(self, question: str, answer: str) -> Dict[str, any]:
        """Check if answer follows STAR method"""
        
        try:
            prompt = self._create_star_prompt(question, answer)
            response = await self.llm.generate(prompt, temperature=0.3)
            
            # Parse response
            try:
                if "```json" in response:
                    json_str = response.split("```json")[1].split("```")[0].strip()
                    analysis = json.loads(json_str)
                elif "```" in response:
                    json_str = response.split("```")[1].split("```")[0].strip()
                    analysis = json.loads(json_str)
                else:
                    analysis = json.loads(response)
            except json.JSONDecodeError:
                logger.error("Failed to parse STAR analysis JSON")
                return self._get_fallback_analysis()
            
            # Calculate score
            score = self._calculate_star_score(analysis)
            analysis["score"] = score
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error checking STAR pattern: {str(e)}")
            return self._get_fallback_analysis()
    
    def _create_star_prompt(self, question: str, answer: str) -> str:
        """Create prompt for STAR analysis"""
        
        return f"""Analyze this interview answer for the STAR method (Situation, Task, Action, Result).

Question: {question}

Answer: {answer}

For each STAR component, determine:
- Is it present in the answer?
- Quote the relevant part if present
- Rate quality (1-5) if present

Return JSON:
{{
    "situation_present": true,
    "situation_quote": "relevant quote here",
    "situation_quality": 4,
    "task_present": true,
    "task_quote": "relevant quote here",
    "task_quality": 3,
    "action_present": true,
    "action_quote": "relevant quote here",
    "action_quality": 5,
    "result_present": false,
    "result_quote": "",
    "result_quality": 0,
    "feedback": "Detailed feedback about STAR usage..."
}}

Be strict but fair in evaluation."""
    
    def _calculate_star_score(self, analysis: Dict) -> float:
        """Calculate overall STAR score (0-100)"""
        
        # Check presence (40% of score)
        presence_score = 0
        for component in ["situation", "task", "action", "result"]:
            if analysis.get(f"{component}_present", False):
                presence_score += 10
        
        # Check quality (60% of score)
        quality_score = 0
        quality_count = 0
        for component in ["situation", "task", "action", "result"]:
            if analysis.get(f"{component}_present", False):
                quality = analysis.get(f"{component}_quality", 0)
                quality_score += (quality / 5) * 15  # Scale to 15 points each
                quality_count += 1
        
        total_score = presence_score + quality_score
        return min(100.0, total_score)
    
    def _get_fallback_analysis(self) -> Dict:
        """Fallback analysis if processing fails"""
        return {
            "situation_present": False,
            "situation_quote": "",
            "situation_quality": 0,
            "task_present": False,
            "task_quote": "",
            "task_quality": 0,
            "action_present": False,
            "action_quote": "",
            "action_quality": 0,
            "result_present": False,
            "result_quote": "",
            "result_quality": 0,
            "score": 0.0,
            "feedback": "Could not analyze STAR pattern."
        }
    
    def get_star_feedback(self, analysis: Dict) -> str:
        """Generate helpful feedback about STAR usage"""
        
        missing = []
        weak = []
        
        for component in ["situation", "task", "action", "result"]:
            if not analysis.get(f"{component}_present", False):
                missing.append(component.capitalize())
            elif analysis.get(f"{component}_quality", 0) < 3:
                weak.append(component.capitalize())
        
        if not missing and not weak:
            return "Excellent use of the STAR method! All components are present and well-articulated."
        
        feedback_parts = []
        
        if missing:
            feedback_parts.append(f"Your answer is missing: {', '.join(missing)}.")
        
        if weak:
            feedback_parts.append(f"Consider strengthening: {', '.join(weak)}.")
        
        # Add specific advice
        if "Result" in missing:
            feedback_parts.append("Always quantify your results with metrics or specific outcomes.")
        
        if "Action" in missing or "Action" in weak:
            feedback_parts.append("Describe your specific actions and decisions in detail.")
        
        return " ".join(feedback_parts)

"""
Response Evaluator - Analyzes and scores interview answers
"""
import logging
import json
from typing import Dict, Any
from app.models.interview import PersonaType
from app.services.llm_service import LLMService

logger = logging.getLogger(__name__)

class ResponseEvaluator:
    """Evaluates interview responses for quality and relevance"""
    
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service
    
    async def evaluate(
        self,
        question: str,
        answer: str,
        expected_elements: list,
        persona: PersonaType
    ) -> Dict[str, Any]:
        """Comprehensive evaluation of an answer"""
        
        try:
            prompt = self._create_evaluation_prompt(
                question, answer, expected_elements, persona
            )
            
            response = await self.llm.generate(prompt, temperature=0.3)
            
            # Parse evaluation
            try:
                if "```json" in response:
                    json_str = response.split("```json")[1].split("```")[0].strip()
                    evaluation = json.loads(json_str)
                elif "```" in response:
                    json_str = response.split("```")[1].split("```")[0].strip()
                    evaluation = json.loads(json_str)
                else:
                    evaluation = json.loads(response)
            except json.JSONDecodeError:
                logger.error("Failed to parse evaluation JSON")
                return self._get_fallback_evaluation()
            
            # Ensure all required fields
            return self._normalize_evaluation(evaluation)
            
        except Exception as e:
            logger.error(f"Error evaluating response: {str(e)}")
            return self._get_fallback_evaluation()
    
    def _create_evaluation_prompt(
        self,
        question: str,
        answer: str,
        expected_elements: list,
        persona: PersonaType
    ) -> str:
        """Create evaluation prompt"""
        
        return f"""You are an expert interview evaluator. Analyze this interview response thoroughly.

Question: {question}

Expected Elements: {', '.join(expected_elements)}

Candidate's Answer: {answer}

Detected Persona: {persona.value}

Evaluate the response on these dimensions (0-100 scale):

1. **Relevance Score**: How well does the answer address the question?
2. **Confidence Score**: How confident and decisive is the candidate?
3. **Technical Depth Score**: How deep is the technical understanding demonstrated?
4. **Clarity Score**: How clear and well-structured is the communication?

Also provide:
- Is the answer on-topic or off-topic?
- Specific strengths (bullet points)
- Specific weaknesses (bullet points)
- Detailed feedback for improvement
- Whether a follow-up question is needed (and why)

Return a JSON object:
{{
    "relevance_score": 75,
    "confidence_score": 80,
    "technical_depth_score": 70,
    "clarity_score": 85,
    "is_on_topic": true,
    "strengths": ["Good use of specific example", "Clear problem statement"],
    "weaknesses": ["Missing quantifiable results", "Could explain technical decisions better"],
    "feedback": "Your answer shows good understanding, but...",
    "needs_follow_up": true,
    "follow_up_reason": "Need to probe deeper on architectural decisions"
}}"""
    
    def _normalize_evaluation(self, evaluation: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure evaluation has all required fields"""
        
        defaults = {
            "relevance_score": 50.0,
            "confidence_score": 50.0,
            "technical_depth_score": 50.0,
            "clarity_score": 50.0,
            "is_on_topic": True,
            "strengths": [],
            "weaknesses": [],
            "feedback": "Response received.",
            "needs_follow_up": False,
            "follow_up_reason": ""
        }
        
        # Merge with defaults
        for key, default_value in defaults.items():
            if key not in evaluation:
                evaluation[key] = default_value
        
        # Ensure scores are floats in range 0-100
        for score_key in ["relevance_score", "confidence_score", "technical_depth_score", "clarity_score"]:
            try:
                score = float(evaluation[score_key])
                evaluation[score_key] = max(0.0, min(100.0, score))
            except (ValueError, TypeError):
                evaluation[score_key] = 50.0
        
        return evaluation
    
    def _get_fallback_evaluation(self) -> Dict[str, Any]:
        """Fallback evaluation if processing fails"""
        return {
            "relevance_score": 50.0,
            "confidence_score": 50.0,
            "technical_depth_score": 50.0,
            "clarity_score": 50.0,
            "is_on_topic": True,
            "strengths": ["Response provided"],
            "weaknesses": ["Could not be fully evaluated"],
            "feedback": "Your response has been recorded.",
            "needs_follow_up": False,
            "follow_up_reason": ""
        }
    
    def calculate_overall_score(self, evaluation: Dict[str, Any]) -> float:
        """Calculate overall score from individual scores"""
        
        scores = [
            evaluation.get("relevance_score", 50),
            evaluation.get("confidence_score", 50),
            evaluation.get("technical_depth_score", 50),
            evaluation.get("clarity_score", 50)
        ]
        
        return sum(scores) / len(scores)

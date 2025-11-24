"""
Follow-up Engine - Generates intelligent follow-up questions
"""
import logging
from typing import Optional
from app.models.interview import FollowUpQuestion, PersonaType
from app.services.llm_service import LLMService

logger = logging.getLogger(__name__)

class FollowUpEngine:
    """Generates context-aware follow-up questions"""
    
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service
    
    async def generate_follow_up(
        self,
        question: str,
        answer: str,
        evaluation: dict,
        persona: PersonaType
    ) -> Optional[FollowUpQuestion]:
        """Generate intelligent follow-up question"""
        
        # Decide if follow-up is needed
        if not evaluation.get("needs_follow_up", False):
            return None
        
        # Determine follow-up type based on evaluation and persona
        follow_up_type = self._determine_follow_up_type(evaluation, persona)
        
        # Generate follow-up question
        follow_up_text = await self._generate_follow_up_text(
            question, answer, evaluation, persona, follow_up_type
        )
        
        if not follow_up_text:
            return None
        
        return FollowUpQuestion(
            text=follow_up_text,
            reason=evaluation.get("follow_up_reason", "Seeking clarification"),
            type=follow_up_type
        )
    
    def _determine_follow_up_type(self, evaluation: dict, persona: PersonaType) -> str:
        """Determine what type of follow-up is needed"""
        
        # Off-topic answer → redirect
        if not evaluation.get("is_on_topic", True):
            return "redirect"
        
        # Low relevance score → probe
        if evaluation.get("relevance_score", 50) < 60:
            return "probe"
        
        # Confused persona → hint
        if persona == PersonaType.CONFUSED:
            return "hint"
        
        # High confidence → challenge
        if evaluation.get("confidence_score", 50) > 80:
            return "challenge"
        
        # Missing depth → probe
        if evaluation.get("technical_depth_score", 50) < 60:
            return "probe"
        
        # Default
        return "probe"
    
    async def _generate_follow_up_text(
        self,
        question: str,
        answer: str,
        evaluation: dict,
        persona: PersonaType,
        follow_up_type: str
    ) -> Optional[str]:
        """Generate the actual follow-up question text"""
        
        # Get adaptation strategy for persona
        from app.agents.persona_detector import PersonaDetector
        detector = PersonaDetector(self.llm)
        strategy = detector.get_adaptation_strategy(persona)
        
        # Create prompt based on follow-up type
        prompt = self._create_follow_up_prompt(
            question, answer, evaluation, persona, follow_up_type, strategy
        )
        
        try:
            response = await self.llm.generate(prompt, temperature=0.7, max_tokens=150)
            
            # Extract just the question if wrapped in quotes or extra text
            follow_up = response.strip().strip('"\'')
            
            # Remove any preamble
            if ":" in follow_up:
                follow_up = follow_up.split(":", 1)[-1].strip()
            
            return follow_up
            
        except Exception as e:
            logger.error(f"Error generating follow-up: {str(e)}")
            return self._get_fallback_follow_up(follow_up_type)
    
    def _create_follow_up_prompt(
        self,
        question: str,
        answer: str,
        evaluation: dict,
        persona: PersonaType,
        follow_up_type: str,
        strategy: dict
    ) -> str:
        """Create prompt for follow-up generation"""
        
        type_instructions = {
            "redirect": """The candidate went off-topic. Generate a polite redirection that:
- Acknowledges their answer briefly
- Gently points out they drifted
- Refocuses them on the original question
- References specific elements from their resume if possible
Example: "I appreciate that context, but I notice you've drifted from the original question about X. Let's refocus: Can you specifically address..."
""",
            "probe": """The candidate's answer lacks depth. Generate a probing question that:
- Digs deeper into technical details
- Asks for specific examples or data
- Challenges them to explain their reasoning
- Seeks quantifiable results
Example: "You mentioned you improved performance. Can you walk me through exactly how you identified the bottleneck and what specific optimization techniques you applied?"
""",
            "hint": """The candidate seems confused or struggling. Generate a helpful hint that:
- Guides them without giving the answer
- Provides a framework or structure
- References their resume to jog memory
- Encourages them supportively
Example: "Let me help frame this: Think about your project at Company X where you worked with technology Y. How did you approach similar challenges there?"
""",
            "challenge": """The candidate seems very confident. Generate a challenging question that:
- Tests depth of understanding
- Explores edge cases or trade-offs
- Asks about alternatives not mentioned
- Probes decision-making process
Example: "That's a solid approach. But what if you had constraint X? How would that change your architecture, and what trade-offs would you consider?"
"""
        }
        
        instruction = type_instructions.get(follow_up_type, type_instructions["probe"])
        
        return f"""You are conducting a {persona.value} candidate's interview. 

Original Question: {question}

Their Answer: {answer}

Evaluation: Relevance {evaluation.get('relevance_score', 50)}/100, Confidence {evaluation.get('confidence_score', 50)}/100

Follow-up Type: {follow_up_type}

{instruction}

Tone: {strategy.get('tone', 'professional')}
Approach: {strategy.get('follow_up_style', 'contextual probing')}

Generate ONE follow-up question (just the question, no explanation):"""
    
    def _get_fallback_follow_up(self, follow_up_type: str) -> str:
        """Fallback follow-up questions"""
        
        fallbacks = {
            "redirect": "Let's refocus on the original question. Can you provide a more specific answer addressing the core issue?",
            "probe": "Can you elaborate more on that? What specific steps did you take, and what were the measurable outcomes?",
            "hint": "Think about your past experiences. Can you relate this to a specific project or situation from your background?",
            "challenge": "That's interesting. How would you handle this situation if you had different constraints? What alternatives did you consider?"
        }
        
        return fallbacks.get(follow_up_type, fallbacks["probe"])

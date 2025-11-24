"""
Persona Detector - Identifies user behavior patterns during interview
"""
import logging
from typing import Dict, List
from app.models.interview import PersonaType
from app.services.llm_service import LLMService

logger = logging.getLogger(__name__)

class PersonaDetector:
    """Detects and categorizes user personas based on responses"""
    
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service
        self.persona_history: List[PersonaType] = []
    
    async def detect_persona(
        self, 
        question: str, 
        answer: str,
        duration_seconds: float,
        word_count: int
    ) -> PersonaType:
        """Detect user persona from their answer"""
        
        # Rule-based detection (fast)
        persona = self._rule_based_detection(answer, duration_seconds, word_count)
        
        # LLM-based confirmation for edge cases
        if persona == PersonaType.EDGE_CASE or len(answer.split()) < 10:
            persona = await self._llm_based_detection(question, answer)
        
        # Track persona history
        self.persona_history.append(persona)
        
        logger.info(f"Detected persona: {persona.value} for answer of {word_count} words")
        return persona
    
    def _rule_based_detection(
        self, 
        answer: str, 
        duration_seconds: float, 
        word_count: int
    ) -> PersonaType:
        """Fast rule-based persona detection"""
        
        # Edge case detection
        if word_count < 10:
            return PersonaType.EDGE_CASE
        
        if word_count < 3:
            return PersonaType.EDGE_CASE
        
        # Check for nonsense
        unique_chars = len(set(answer.replace(' ', '').lower()))
        if unique_chars < 5:
            return PersonaType.EDGE_CASE
        
        # Confused user detection
        hesitation_words = ['um', 'uh', 'like', 'maybe', 'i think', 'i guess', 'kind of', 'sort of']
        hesitation_count = sum(answer.lower().count(word) for word in hesitation_words)
        
        if hesitation_count > 3 or (hesitation_count > 1 and word_count < 50):
            return PersonaType.CONFUSED
        
        # Chatty user detection
        if word_count > 300 or duration_seconds > 150:  # 2.5 minutes
            return PersonaType.CHATTY
        
        # Efficient user detection
        if 50 <= word_count <= 150 and duration_seconds < 90:
            # Check for structured language
            star_indicators = ['situation', 'task', 'action', 'result', 'first', 'then', 'finally']
            if any(indicator in answer.lower() for indicator in star_indicators):
                return PersonaType.EFFICIENT
        
        # Default to normal
        return PersonaType.NORMAL
    
    async def _llm_based_detection(self, question: str, answer: str) -> PersonaType:
        """LLM-based persona detection for complex cases"""
        
        prompt = f"""Analyze this interview response and categorize the user's persona.

Question: {question}

Answer: {answer}

Persona Types:
- CONFUSED: Hesitant, unclear, asks for clarification, lacks confidence
- EFFICIENT: Structured, concise, uses STAR method, direct
- CHATTY: Overly verbose, goes on tangents, excessive detail
- EDGE_CASE: Nonsense, invalid, extremely short, no attempt
- NORMAL: None of the above

Return ONLY the persona type (one word): CONFUSED, EFFICIENT, CHATTY, EDGE_CASE, or NORMAL"""
        
        try:
            response = await self.llm.generate(prompt, temperature=0.3, max_tokens=10)
            persona_str = response.strip().upper()
            
            # Map to PersonaType
            if "CONFUSED" in persona_str:
                return PersonaType.CONFUSED
            elif "EFFICIENT" in persona_str:
                return PersonaType.EFFICIENT
            elif "CHATTY" in persona_str:
                return PersonaType.CHATTY
            elif "EDGE" in persona_str or "EDGE_CASE" in persona_str:
                return PersonaType.EDGE_CASE
            else:
                return PersonaType.NORMAL
                
        except Exception as e:
            logger.error(f"Error in LLM persona detection: {str(e)}")
            return PersonaType.NORMAL
    
    def get_dominant_persona(self) -> PersonaType:
        """Get the most common persona across all answers"""
        if not self.persona_history:
            return PersonaType.NORMAL
        
        # Count occurrences
        persona_counts = {}
        for persona in self.persona_history:
            persona_counts[persona] = persona_counts.get(persona, 0) + 1
        
        # Return most common
        return max(persona_counts, key=persona_counts.get)
    
    def get_persona_distribution(self) -> Dict[str, int]:
        """Get distribution of personas"""
        distribution = {
            PersonaType.CONFUSED.value: 0,
            PersonaType.EFFICIENT.value: 0,
            PersonaType.CHATTY.value: 0,
            PersonaType.EDGE_CASE.value: 0,
            PersonaType.NORMAL.value: 0,
        }
        
        for persona in self.persona_history:
            distribution[persona.value] += 1
        
        return distribution
    
    def get_adaptation_strategy(self, persona: PersonaType) -> Dict[str, str]:
        """Get strategy for adapting to detected persona"""
        
        strategies = {
            PersonaType.CONFUSED: {
                "tone": "supportive and guiding",
                "approach": "Break down questions, provide hints, use simpler language",
                "follow_up_style": "gentle probing with examples",
                "feedback": "Encourage and guide towards structure"
            },
            PersonaType.EFFICIENT: {
                "tone": "professional and direct",
                "approach": "Keep questions crisp, move quickly, challenge more",
                "follow_up_style": "deep technical probes",
                "feedback": "Acknowledge efficiency, push for even more depth"
            },
            PersonaType.CHATTY: {
                "tone": "polite but redirective",
                "approach": "Interrupt gently, refocus on core question",
                "follow_up_style": "specific pointed questions",
                "feedback": "Encourage conciseness and focus"
            },
            PersonaType.EDGE_CASE: {
                "tone": "patient and clarifying",
                "approach": "Request clarification, offer multiple choice, simplify",
                "follow_up_style": "yes/no or structured options",
                "feedback": "Guide towards valid responses"
            },
            PersonaType.NORMAL: {
                "tone": "balanced and professional",
                "approach": "Standard interview technique",
                "follow_up_style": "contextual probing",
                "feedback": "Balanced feedback"
            }
        }
        
        return strategies.get(persona, strategies[PersonaType.NORMAL])

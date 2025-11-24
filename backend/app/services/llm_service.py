"""
LLM Service - Handles interactions with language models
"""
import logging
from typing import Optional
from app.config import settings

logger = logging.getLogger(__name__)

class LLMService:
    """Service for LLM interactions"""
    
    def __init__(self):
        self.provider = settings.LLM_PROVIDER
        self.model = settings.LLM_MODEL
        self.max_tokens = settings.MAX_TOKENS
        self.temperature = settings.TEMPERATURE
        
        # Initialize client based on provider
        if self.provider == "openai":
            self._init_openai()
        elif self.provider == "anthropic":
            self._init_anthropic()
        else:
            logger.warning(f"Unknown LLM provider: {self.provider}, using mock")
            self.client = None
    
    def _init_openai(self):
        """Initialize OpenAI client"""
        try:
            from openai import AsyncOpenAI
            self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
            logger.info(f"Initialized OpenAI client with model {self.model}")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI client: {str(e)}")
            self.client = None
    
    def _init_anthropic(self):
        """Initialize Anthropic client"""
        try:
            from anthropic import AsyncAnthropic
            self.client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
            logger.info(f"Initialized Anthropic client with model {self.model}")
        except Exception as e:
            logger.error(f"Failed to initialize Anthropic client: {str(e)}")
            self.client = None
    
    async def generate(
        self,
        prompt: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """Generate text from LLM"""
        
        temp = temperature if temperature is not None else self.temperature
        tokens = max_tokens if max_tokens is not None else self.max_tokens
        
        if not self.client:
            logger.warning("No LLM client available, returning mock response")
            return self._mock_response(prompt)
        
        try:
            if self.provider == "openai":
                return await self._generate_openai(prompt, temp, tokens)
            elif self.provider == "anthropic":
                return await self._generate_anthropic(prompt, temp, tokens)
            else:
                return self._mock_response(prompt)
        except Exception as e:
            logger.error(f"Error generating LLM response: {str(e)}")
            return self._mock_response(prompt)
    
    async def _generate_openai(self, prompt: str, temperature: float, max_tokens: int) -> str:
        """Generate using OpenAI"""
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert interview coach and evaluator."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    
    async def _generate_anthropic(self, prompt: str, temperature: float, max_tokens: int) -> str:
        """Generate using Anthropic"""
        response = await self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text
    
    def _mock_response(self, prompt: str) -> str:
        """Mock response for testing without API keys"""
        
        # Basic pattern matching for different types of prompts
        if "parse" in prompt.lower() or "extract" in prompt.lower():
            return """{
    "name": "John Doe",
    "email": "john.doe@email.com",
    "skills": [
        {"name": "Python", "category": "technical", "proficiency": "expert"},
        {"name": "JavaScript", "category": "technical", "proficiency": "intermediate"}
    ],
    "experiences": [{
        "company": "Tech Corp",
        "title": "Software Engineer",
        "start_date": "Jan 2020",
        "end_date": "Present",
        "responsibilities": ["Developed features", "Fixed bugs"],
        "achievements": ["Improved performance by 30%"],
        "technologies": ["Python", "React"]
    }],
    "projects": [],
    "education": [{
        "institution": "University",
        "degree": "BS Computer Science",
        "field": "Computer Science"
    }],
    "certifications": []
}"""
        elif "question" in prompt.lower() and "generate" in prompt.lower():
            return """{
    "questions": [
        {
            "question_text": "Tell me about a challenging project you worked on and how you overcame obstacles.",
            "question_type": "behavioral",
            "related_to": "work experience",
            "expected_elements": ["situation", "task", "action", "result"],
            "difficulty": "medium"
        },
        {
            "question_text": "Explain your approach to debugging a production issue.",
            "question_type": "technical",
            "related_to": "technical skills",
            "expected_elements": ["methodology", "tools", "process"],
            "difficulty": "medium"
        }
    ]
}"""
        elif "evaluate" in prompt.lower() or "score" in prompt.lower():
            return """{
    "relevance_score": 75,
    "confidence_score": 70,
    "technical_depth_score": 72,
    "clarity_score": 78,
    "is_on_topic": true,
    "strengths": ["Good structure", "Specific examples"],
    "weaknesses": ["Could add more technical details"],
    "feedback": "Your answer demonstrates understanding but could benefit from more depth.",
    "needs_follow_up": false,
    "follow_up_reason": ""
}"""
        elif "star" in prompt.lower():
            return """{
    "situation_present": true,
    "situation_quote": "When I was working at Tech Corp...",
    "situation_quality": 4,
    "task_present": true,
    "task_quote": "I was responsible for...",
    "task_quality": 3,
    "action_present": true,
    "action_quote": "I implemented...",
    "action_quality": 4,
    "result_present": false,
    "result_quote": "",
    "result_quality": 0,
    "feedback": "Good STAR structure, but missing quantifiable results."
}"""
        elif "follow" in prompt.lower():
            return "Can you elaborate more on the specific technical approach you used and why you chose it?"
        elif "persona" in prompt.lower():
            return "NORMAL"
        elif "role" in prompt.lower() and "[" in prompt:
            return '["Software Engineer", "Full Stack Developer", "Backend Engineer"]'
        elif "insight" in prompt.lower() or "strengths" in prompt.lower():
            return """{
    "strengths": ["Clear communication", "Good examples", "Technical knowledge"],
    "weaknesses": ["Could improve STAR method", "More quantifiable results needed"],
    "suggestions": [
        "Practice STAR method structure",
        "Quantify achievements with metrics",
        "Prepare more technical examples"
    ],
    "next_steps": [
        "Do 5 more practice interviews",
        "Review common questions",
        "Practice technical explanations"
    ]
}"""
        else:
            return "This is a mock response. Please configure a valid LLM API key."

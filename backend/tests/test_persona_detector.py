"""
Tests for Persona Detector
"""
import pytest
from app.agents.persona_detector import PersonaDetector
from app.services.llm_service import LLMService
from app.models.interview import PersonaType

@pytest.fixture
def llm_service():
    return LLMService()

@pytest.fixture
def persona_detector(llm_service):
    return PersonaDetector(llm_service)

@pytest.mark.asyncio
async def test_detect_confused_persona(persona_detector):
    """Test detection of confused persona"""
    question = "Tell me about your experience with Python"
    answer = "Um, well, I think I used Python, maybe in college? I'm not really sure, like, it was a while ago..."
    
    persona = await persona_detector.detect_persona(question, answer, 30.0, 20)
    
    assert persona == PersonaType.CONFUSED

@pytest.mark.asyncio
async def test_detect_efficient_persona(persona_detector):
    """Test detection of efficient persona"""
    question = "Describe a challenging project"
    answer = """In my previous role, I led a microservices migration project. 
    First, I analyzed the monolithic architecture and identified service boundaries. 
    Then, I implemented the services using Docker and Kubernetes. 
    Finally, we achieved 99.9% uptime and reduced deployment time by 70%."""
    
    persona = await persona_detector.detect_persona(question, answer, 60.0, 50)
    
    # Should be efficient or normal
    assert persona in [PersonaType.EFFICIENT, PersonaType.NORMAL]

@pytest.mark.asyncio
async def test_detect_chatty_persona(persona_detector):
    """Test detection of chatty persona"""
    long_answer = "Well, let me tell you about this. " * 50  # Very long, rambling answer
    
    persona = await persona_detector.detect_persona(
        "Tell me about yourself", long_answer, 180.0, 350
    )
    
    assert persona == PersonaType.CHATTY

@pytest.mark.asyncio
async def test_detect_edge_case_persona(persona_detector):
    """Test detection of edge case persona"""
    question = "Describe your experience"
    answer = "asdfasdf"
    
    persona = await persona_detector.detect_persona(question, answer, 5.0, 1)
    
    assert persona == PersonaType.EDGE_CASE

def test_get_adaptation_strategy(persona_detector):
    """Test that adaptation strategies are returned"""
    strategy = persona_detector.get_adaptation_strategy(PersonaType.CONFUSED)
    
    assert "tone" in strategy
    assert "approach" in strategy
    assert strategy["tone"] == "supportive and guiding"

def test_persona_distribution(persona_detector):
    """Test persona distribution tracking"""
    persona_detector.persona_history = [
        PersonaType.NORMAL,
        PersonaType.EFFICIENT,
        PersonaType.NORMAL
    ]
    
    distribution = persona_detector.get_persona_distribution()
    
    assert distribution[PersonaType.NORMAL.value] == 2
    assert distribution[PersonaType.EFFICIENT.value] == 1

def test_dominant_persona(persona_detector):
    """Test dominant persona calculation"""
    persona_detector.persona_history = [
        PersonaType.EFFICIENT,
        PersonaType.EFFICIENT,
        PersonaType.NORMAL
    ]
    
    dominant = persona_detector.get_dominant_persona()
    
    assert dominant == PersonaType.EFFICIENT

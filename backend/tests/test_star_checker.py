"""
Tests for STAR Pattern Checker
"""
import pytest
from app.agents.star_checker import STARChecker
from app.services.llm_service import LLMService

@pytest.fixture
def llm_service():
    return LLMService()

@pytest.fixture
def star_checker(llm_service):
    return STARChecker(llm_service)

@pytest.mark.asyncio
async def test_complete_star_pattern(star_checker):
    """Test detection of complete STAR pattern"""
    question = "Tell me about a challenging situation you faced"
    answer = """
    When I was working at Tech Corp (Situation), we had a critical production outage 
    affecting 10,000 users. I was responsible for identifying and fixing the issue (Task). 
    I quickly analyzed the logs, identified a memory leak in the caching layer, deployed a fix, 
    and implemented monitoring (Action). As a result, we restored service in 2 hours and 
    prevented future incidents with the new monitoring system (Result).
    """
    
    analysis = await star_checker.check_star_pattern(question, answer)
    
    assert analysis["score"] > 50  # Should have decent score
    # At least some STAR elements should be present
    assert analysis["situation_present"] or analysis["task_present"] or \
           analysis["action_present"] or analysis["result_present"]

@pytest.mark.asyncio
async def test_missing_result(star_checker):
    """Test detection when result is missing"""
    question = "Describe a project you worked on"
    answer = """
    I worked on a microservices migration project. 
    I was responsible for breaking down the monolith.
    I analyzed the code, identified service boundaries, and started implementing.
    """
    
    analysis = await star_checker.check_star_pattern(question, answer)
    
    # Result should be missing
    feedback = star_checker.get_star_feedback(analysis)
    assert "result" in feedback.lower() or "Result" in feedback

@pytest.mark.asyncio
async def test_no_star_pattern(star_checker):
    """Test answer with no STAR pattern"""
    question = "Tell me about your experience"
    answer = "I have worked with Python and JavaScript. I like coding."
    
    analysis = await star_checker.check_star_pattern(question, answer)
    
    assert analysis["score"] < 40  # Low score expected

def test_get_star_feedback(star_checker):
    """Test feedback generation"""
    analysis = {
        "situation_present": True,
        "task_present": True,
        "action_present": True,
        "result_present": True,
        "situation_quality": 4,
        "task_quality": 4,
        "action_quality": 4,
        "result_quality": 4,
        "score": 90.0,
        "feedback": "Excellent"
    }
    
    feedback = star_checker.get_star_feedback(analysis)
    assert "excellent" in feedback.lower()

def test_fallback_analysis(star_checker):
    """Test fallback analysis structure"""
    fallback = star_checker._get_fallback_analysis()
    
    assert "situation_present" in fallback
    assert "task_present" in fallback
    assert "action_present" in fallback
    assert "result_present" in fallback
    assert fallback["score"] == 0.0

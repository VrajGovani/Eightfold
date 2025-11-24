"""
Tests for Interview Logic
"""
import pytest
from app.services.interview_service import InterviewService
from app.models.resume import ResumeData, Skill, Experience

@pytest.fixture
def interview_service():
    return InterviewService()

@pytest.fixture
def sample_resume_data():
    return ResumeData(
        name="John Doe",
        email="john.doe@email.com",
        skills=[
            Skill(name="Python", category="technical", proficiency="expert"),
            Skill(name="JavaScript", category="technical", proficiency="intermediate")
        ],
        experiences=[
            Experience(
                company="Tech Corp",
                title="Software Engineer",
                start_date="2020-01",
                end_date="Present",
                responsibilities=["Develop features", "Fix bugs"],
                technologies=["Python", "React"]
            )
        ],
        raw_text="Sample resume text"
    )

@pytest.mark.asyncio
async def test_start_interview(interview_service, sample_resume_data):
    """Test starting an interview session"""
    session_id = "test-session-123"
    target_role = "Software Engineer"
    
    session = await interview_service.start_interview(
        session_id, sample_resume_data, target_role
    )
    
    assert session.session_id == session_id
    assert session.target_role == target_role
    assert len(session.questions) == 5  # Should have 5 questions
    assert session.status == "in_progress"

@pytest.mark.asyncio
async def test_submit_answer(interview_service, sample_resume_data):
    """Test submitting an answer"""
    session_id = "test-session-456"
    target_role = "Software Engineer"
    
    # Start interview
    session = await interview_service.start_interview(
        session_id, sample_resume_data, target_role
    )
    
    # Submit answer
    answer_text = "I worked on a challenging project where I had to optimize database queries. I analyzed the slow queries, added proper indexes, and reduced response time by 60%."
    response = await interview_service.submit_answer(
        session_id,
        1,
        answer_text,
        45.5,
        False
    )
    
    assert response.success is True
    # Either follow-up or next question should be present
    assert response.follow_up_question is not None or response.next_question is not None

@pytest.mark.asyncio
async def test_get_current_question(interview_service, sample_resume_data):
    """Test getting current question"""
    session_id = "test-session-789"
    
    session = await interview_service.start_interview(
        session_id, sample_resume_data, "Software Engineer"
    )
    
    current_q = interview_service.get_current_question(session_id)
    assert current_q is not None
    assert current_q.question_id == 1

def test_session_storage(interview_service, sample_resume_data):
    """Test that sessions are stored correctly"""
    session_id = "test-session-storage"
    
    # Session shouldn't exist initially
    assert interview_service.get_session(session_id) is None

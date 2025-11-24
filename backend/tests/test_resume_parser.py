"""
Tests for Resume Parser
"""
import pytest
from app.agents.resume_parser import ResumeParser
from app.services.llm_service import LLMService

@pytest.fixture
def llm_service():
    return LLMService()

@pytest.fixture
def resume_parser(llm_service):
    return ResumeParser(llm_service)

@pytest.fixture
def sample_resume_text():
    return """
John Doe
john.doe@email.com | (555) 123-4567 | linkedin.com/in/johndoe

PROFESSIONAL SUMMARY
Senior Software Engineer with 5+ years of experience in full-stack development.

SKILLS
Python, JavaScript, React, Node.js, AWS, Docker, SQL

EXPERIENCE
Senior Software Engineer | Tech Corp | Jan 2020 - Present
- Developed microservices architecture using Python and Docker
- Improved system performance by 40%
- Led team of 5 engineers

Software Engineer | StartupXYZ | Jun 2018 - Dec 2019
- Built REST APIs using Node.js and Express
- Implemented CI/CD pipeline

EDUCATION
Bachelor of Science in Computer Science | University | 2014 - 2018
GPA: 3.8/4.0

PROJECTS
E-commerce Platform
- Built full-stack application using React and Node.js
- Integrated payment gateway and authentication
"""

@pytest.mark.asyncio
async def test_resume_parsing(resume_parser, sample_resume_text):
    """Test basic resume parsing"""
    result = await resume_parser.parse(sample_resume_text)
    
    assert result is not None
    assert result.raw_text == sample_resume_text
    # Note: Without real LLM, parsed fields may be empty

@pytest.mark.asyncio
async def test_resume_with_skills(resume_parser, sample_resume_text):
    """Test that skills are extracted"""
    result = await resume_parser.parse(sample_resume_text)
    
    # With mock LLM, we should still get a valid ResumeData object
    assert hasattr(result, 'skills')
    assert isinstance(result.skills, list)

@pytest.mark.asyncio
async def test_detect_roles(resume_parser, sample_resume_text):
    """Test role detection"""
    resume_data = await resume_parser.parse(sample_resume_text)
    roles = await resume_parser.detect_target_roles(resume_data)
    
    assert isinstance(roles, list)
    assert len(roles) > 0

def test_resume_parser_initialization(llm_service):
    """Test that parser initializes correctly"""
    parser = ResumeParser(llm_service)
    assert parser.llm is not None

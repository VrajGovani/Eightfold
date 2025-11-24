"""
Resume data models
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class Skill(BaseModel):
    """Individual skill"""
    name: str
    category: Optional[str] = None  # technical, soft, language, etc.
    proficiency: Optional[str] = None  # beginner, intermediate, expert

class Experience(BaseModel):
    """Work experience entry"""
    company: str
    title: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    duration: Optional[str] = None
    responsibilities: List[str] = []
    achievements: List[str] = []
    technologies: List[str] = []

class Project(BaseModel):
    """Project entry"""
    name: str
    description: str
    technologies: List[str] = []
    role: Optional[str] = None
    outcomes: List[str] = []
    url: Optional[str] = None

class Education(BaseModel):
    """Education entry"""
    institution: str
    degree: str
    field: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    gpa: Optional[str] = None
    achievements: List[str] = []

class ResumeData(BaseModel):
    """Parsed resume data structure"""
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    summary: Optional[str] = None
    skills: List[Skill] = []
    experiences: List[Experience] = []
    projects: List[Project] = []
    education: List[Education] = []
    certifications: List[str] = []
    raw_text: str = ""
    
class ResumeUploadResponse(BaseModel):
    """Response after resume upload"""
    session_id: str
    resume_data: ResumeData
    detected_roles: List[str] = []
    message: str = "Resume parsed successfully"

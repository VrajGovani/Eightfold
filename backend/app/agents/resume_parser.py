"""
Resume Parser Agent - Extracts structured data from resume text
"""
import json
import logging
from typing import List, Dict, Any
from app.models.resume import ResumeData, Skill, Experience, Project, Education
from app.services.llm_service import LLMService

logger = logging.getLogger(__name__)

class ResumeParser:
    """Intelligent resume parsing using LLM"""
    
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service
    
    async def parse(self, raw_text: str) -> ResumeData:
        """Parse resume text into structured data"""
        try:
            # Create prompt for LLM to extract structured data
            prompt = self._create_parsing_prompt(raw_text)
            
            # Get structured extraction from LLM
            response = await self.llm.generate(prompt, temperature=0.3)
            
            # Parse JSON response
            try:
                parsed_data = json.loads(response)
            except json.JSONDecodeError:
                # Fallback: extract JSON from markdown code blocks
                if "```json" in response:
                    json_str = response.split("```json")[1].split("```")[0].strip()
                    parsed_data = json.loads(json_str)
                elif "```" in response:
                    json_str = response.split("```")[1].split("```")[0].strip()
                    parsed_data = json.loads(json_str)
                else:
                    raise
            
            # Convert to ResumeData model
            resume_data = self._convert_to_model(parsed_data, raw_text)
            
            logger.info(f"Successfully parsed resume with {len(resume_data.skills)} skills, "
                       f"{len(resume_data.experiences)} experiences, {len(resume_data.projects)} projects")
            
            return resume_data
            
        except Exception as e:
            logger.error(f"Error parsing resume: {str(e)}")
            # Return basic resume with raw text
            return ResumeData(raw_text=raw_text)
    
    def _create_parsing_prompt(self, raw_text: str) -> str:
        """Create prompt for resume parsing"""
        return f"""You are an expert resume parser. Extract structured information from the following resume text.

Resume Text:
{raw_text}

Extract and return a JSON object with the following structure:
{{
    "name": "Full name",
    "email": "email@example.com",
    "phone": "phone number",
    "linkedin": "LinkedIn URL if present",
    "github": "GitHub URL if present",
    "summary": "Professional summary or objective",
    "skills": [
        {{"name": "Python", "category": "technical", "proficiency": "expert"}},
        {{"name": "Leadership", "category": "soft", "proficiency": "intermediate"}}
    ],
    "experiences": [
        {{
            "company": "Company Name",
            "title": "Job Title",
            "start_date": "Jan 2020",
            "end_date": "Present",
            "duration": "3 years",
            "responsibilities": ["Responsibility 1", "Responsibility 2"],
            "achievements": ["Achievement 1", "Achievement 2"],
            "technologies": ["Tech1", "Tech2"]
        }}
    ],
    "projects": [
        {{
            "name": "Project Name",
            "description": "Brief description",
            "technologies": ["Tech1", "Tech2"],
            "role": "Your role",
            "outcomes": ["Outcome 1", "Outcome 2"],
            "url": "Project URL if available"
        }}
    ],
    "education": [
        {{
            "institution": "University Name",
            "degree": "Bachelor of Science",
            "field": "Computer Science",
            "start_date": "2015",
            "end_date": "2019",
            "gpa": "3.8/4.0",
            "achievements": ["Dean's List", "Honor Society"]
        }}
    ],
    "certifications": ["Certification 1", "Certification 2"]
}}

Return ONLY the JSON object, no additional text."""
    
    def _convert_to_model(self, parsed_data: Dict[str, Any], raw_text: str) -> ResumeData:
        """Convert parsed dictionary to ResumeData model"""
        
        # Convert skills
        skills = [
            Skill(**skill) if isinstance(skill, dict) else Skill(name=skill)
            for skill in parsed_data.get('skills', [])
        ]
        
        # Convert experiences
        experiences = [
            Experience(**exp) for exp in parsed_data.get('experiences', [])
        ]
        
        # Convert projects
        projects = [
            Project(**proj) for proj in parsed_data.get('projects', [])
        ]
        
        # Convert education
        education = [
            Education(**edu) for edu in parsed_data.get('education', [])
        ]
        
        return ResumeData(
            name=parsed_data.get('name'),
            email=parsed_data.get('email'),
            phone=parsed_data.get('phone'),
            linkedin=parsed_data.get('linkedin'),
            github=parsed_data.get('github'),
            summary=parsed_data.get('summary'),
            skills=skills,
            experiences=experiences,
            projects=projects,
            education=education,
            certifications=parsed_data.get('certifications', []),
            raw_text=raw_text
        )
    
    async def detect_target_roles(self, resume_data: ResumeData) -> List[str]:
        """Detect suitable job roles based on resume"""
        
        skills_str = ', '.join([s.name for s in resume_data.skills[:15]])
        exp_titles = [exp.title for exp in resume_data.experiences[:3]] if resume_data.experiences else []
        projects_str = ', '.join([p.name for p in resume_data.projects[:3]]) if resume_data.projects else 'None'
        education_str = resume_data.education[0].degree if resume_data.education else 'N/A'
        
        prompt = f"""Based on the following resume information, suggest 3-5 most suitable job roles:

Skills: {skills_str}
Experience Titles: {', '.join(exp_titles) if exp_titles else 'N/A'}
Projects: {projects_str}
Education: {education_str}

Consider roles: Software Engineer, Data Analyst, Data Engineer, Project Manager, Product Manager, Business Analyst, Marketing Manager, HR Manager, DevOps Engineer, Full-Stack Developer

Return only a JSON array of 3-5 role names, e.g., ["Software Engineer", "Data Analyst", "Project Manager"]"""
        
        response = await self.llm.generate(prompt, temperature=0.3)
        
        try:
            # Parse JSON response
            if "```json" in response:
                json_str = response.split("```json")[1].split("```")[0].strip()
                roles = json.loads(json_str)
            elif "[" in response:
                # Extract array from text
                start = response.index("[")
                end = response.rindex("]") + 1
                roles = json.loads(response[start:end])
            else:
                roles = ["Software Engineer"]  # Default
            
            return roles[:5]  # Return max 5 roles
            
        except Exception as e:
            logger.error(f"Error detecting roles: {str(e)}")
            return ["Software Engineer"]  # Default fallback

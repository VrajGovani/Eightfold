"""
Interview Question Generator - Creates personalized interview questions
"""
import logging
import json
from typing import List
from app.models.resume import ResumeData
from app.models.interview import InterviewQuestion, QuestionType
from app.services.llm_service import LLMService
from app.config import settings

logger = logging.getLogger(__name__)

class QuestionGenerator:
    """Generates dynamic interview questions based on resume"""
    
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service
    
    async def generate_questions(
        self, 
        resume_data: ResumeData, 
        target_role: str
    ) -> List[InterviewQuestion]:
        """Generate personalized interview questions"""
        
        try:
            prompt = self._create_generation_prompt(resume_data, target_role)
            response = await self.llm.generate(prompt, temperature=0.8)
            
            # Parse JSON response
            try:
                if "```json" in response:
                    json_str = response.split("```json")[1].split("```")[0].strip()
                    questions_data = json.loads(json_str)
                elif "```" in response:
                    json_str = response.split("```")[1].split("```")[0].strip()
                    questions_data = json.loads(json_str)
                else:
                    questions_data = json.loads(response)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse questions JSON: {str(e)}")
                return self._get_fallback_questions(target_role)
            
            # Convert to InterviewQuestion objects
            questions = []
            for i, q_data in enumerate(questions_data.get('questions', [])[:settings.TOTAL_QUESTIONS]):
                try:
                    question = InterviewQuestion(
                        question_id=i + 1,
                        question_text=q_data['question_text'],
                        question_type=QuestionType(q_data.get('question_type', 'behavioral')),
                        related_to=q_data.get('related_to'),
                        expected_elements=q_data.get('expected_elements', []),
                        difficulty=q_data.get('difficulty', 'medium')
                    )
                    questions.append(question)
                except Exception as e:
                    logger.error(f"Error creating question {i}: {str(e)}")
                    continue
            
            # Ensure we have exactly 5 questions
            while len(questions) < settings.TOTAL_QUESTIONS:
                questions.append(self._create_generic_question(len(questions) + 1, target_role))
            
            logger.info(f"Generated {len(questions)} questions for {target_role} role")
            return questions[:settings.TOTAL_QUESTIONS]
            
        except Exception as e:
            logger.error(f"Error generating questions: {str(e)}")
            return self._get_fallback_questions(target_role)
    
    def _create_generation_prompt(self, resume_data: ResumeData, target_role: str) -> str:
        """Create prompt for question generation"""
        
        skills_summary = ", ".join([s.name for s in resume_data.skills[:10]])
        
        exp_summary = ""
        internship_summary = ""
        if resume_data.experiences:
            regular_exp = [exp for exp in resume_data.experiences if 'intern' not in exp.title.lower()]
            internships = [exp for exp in resume_data.experiences if 'intern' in exp.title.lower()]
            
            if regular_exp:
                exp = regular_exp[0]
                exp_summary = f"{exp.title} at {exp.company}"
            
            if internships:
                internship_summary = "; ".join([f"{intern.title} at {intern.company}" for intern in internships[:2]])
        
        projects_summary = ""
        projects_details = []
        if resume_data.projects:
            projects_summary = ", ".join([p.name for p in resume_data.projects[:3]])
            projects_details = [f"{p.name}: {p.description[:100] if p.description else 'No description'}" for p in resume_data.projects[:2]]
        
        return f"""You are an expert interviewer for {target_role} positions. Generate exactly 5 interview questions based on this candidate's resume.

Resume Highlights:
- Skills: {skills_summary}
- Recent Experience: {exp_summary}
- Internships: {internship_summary if internship_summary else 'None listed'}
- Projects: {projects_summary}
- Project Details: {'; '.join(projects_details) if projects_details else 'No details available'}
- Education: {resume_data.education[0].degree if resume_data.education else 'Not specified'}

Requirements:
1. Generate exactly 5 questions
2. Mix question types: 2 technical, 2 behavioral, 1 situational
3. IMPORTANT: Reference specific items from their resume:
   - Ask about their PROJECTS (e.g., "Tell me about your {projects_summary.split(',')[0] if projects_summary else 'project'}...")
   - Ask about their INTERNSHIPS if they have any (e.g., "During your internship at...")
   - Ask about specific SKILLS they've listed
   - Ask about their WORK EXPERIENCE
4. Make questions progressively challenging
5. Include deep-dive questions that require STAR method answers
6. Each question should be specific to reveal their true knowledge

Return a JSON object with this structure:
{{
    "questions": [
        {{
            "question_text": "I see you worked with Python at XYZ Corp. Can you walk me through your most complex Python project and the architectural decisions you made?",
            "question_type": "technical",
            "related_to": "Python experience at XYZ Corp",
            "expected_elements": ["architecture explanation", "decision-making process", "technical details", "impact/results"],
            "difficulty": "medium"
        }},
        {{
            "question_text": "Tell me about a time when you had to debug a critical production issue. What was your approach?",
            "question_type": "behavioral",
            "related_to": "problem-solving experience",
            "expected_elements": ["situation context", "task/responsibility", "action steps", "measurable result"],
            "difficulty": "medium"
        }}
    ]
}}

Generate questions that will thoroughly assess this candidate for the {target_role} role."""
    
    def _get_fallback_questions(self, target_role: str) -> List[InterviewQuestion]:
        """Fallback questions if generation fails"""
        return [
            self._create_generic_question(1, target_role),
            self._create_generic_question(2, target_role),
            self._create_generic_question(3, target_role),
            self._create_generic_question(4, target_role),
            self._create_generic_question(5, target_role),
        ]
    
    def _create_generic_question(self, question_id: int, target_role: str) -> InterviewQuestion:
        """Create a generic question based on role"""
        
        technical_roles = ['software', 'data analyst', 'data engineer', 'developer', 'devops', 'engineer']
        is_technical = any(tech in target_role.lower() for tech in technical_roles)
        
        if is_technical:
            questions = {
                1: {"text": f"Tell me about a significant project or internship where you applied {target_role} skills.", "type": QuestionType.EXPERIENCE, "difficulty": "medium"},
                2: {"text": "Describe a technical challenge you faced in one of your projects. How did you overcome it?", "type": QuestionType.BEHAVIORAL, "difficulty": "easy"},
                3: {"text": f"Walk me through your approach to solving a complex problem in {target_role.lower()}. What tools do you use?", "type": QuestionType.TECHNICAL, "difficulty": "hard"},
                4: {"text": "Tell me about a time you had to learn a new technology quickly. What was your process?", "type": QuestionType.BEHAVIORAL, "difficulty": "medium"},
                5: {"text": "How do you ensure quality and maintainability in your work?", "type": QuestionType.SITUATIONAL, "difficulty": "medium"}
            }
        else:
            questions = {
                1: {"text": f"Tell me about your most impactful accomplishment as a {target_role}.", "type": QuestionType.EXPERIENCE, "difficulty": "medium"},
                2: {"text": "Describe a situation where you managed competing priorities. How did you handle it?", "type": QuestionType.BEHAVIORAL, "difficulty": "easy"},
                3: {"text": f"How would you approach a typical challenge in {target_role}?", "type": QuestionType.SITUATIONAL, "difficulty": "hard"},
                4: {"text": "Tell me about a time you had to influence stakeholders without authority.", "type": QuestionType.BEHAVIORAL, "difficulty": "medium"},
                5: {"text": "How do you measure success in your role?", "type": QuestionType.SITUATIONAL, "difficulty": "medium"}
            }
        
        q = questions.get(question_id, questions[1])
        return InterviewQuestion(
            question_id=question_id,
            question_text=q["text"],
            question_type=q["type"],
            difficulty=q["difficulty"]
        )


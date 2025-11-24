"""
API Routes
"""
import logging
import uuid
import json
from fastapi import APIRouter, File, UploadFile, HTTPException, Response
from fastapi.responses import JSONResponse, StreamingResponse

from app.models.resume import ResumeUploadResponse
from app.models.interview import (
    StartInterviewRequest, SubmitAnswerRequest, SubmitAnswerResponse
)
from app.models.report import ReportGenerationRequest, PerformanceReport
from app.agents.resume_parser import ResumeParser
from app.services.llm_service import LLMService
from app.services.interview_service import interview_service
from app.services.pdf_service import PDFService
from app.agents.report_generator import ReportGenerator
from app.utils.file_parser import FileParser
from app.utils.validators import is_valid_answer
from app.config import settings
from io import BytesIO

logger = logging.getLogger(__name__)

router = APIRouter()

# Initialize services
llm_service = LLMService()
resume_parser = ResumeParser(llm_service)
report_gen = ReportGenerator(llm_service)
pdf_service = PDFService()

@router.post("/upload-resume", response_model=ResumeUploadResponse)
async def upload_resume(file: UploadFile = File(...)):
    """Upload and parse resume"""
    try:
        logger.info(f"Received file upload: {file.filename}, content_type: {file.content_type}")
        
        # Validate file
        if not file.filename:
            logger.error("No filename provided")
            raise HTTPException(status_code=400, detail="No file provided")
        
        extension = file.filename.split('.')[-1].lower()
        logger.info(f"File extension: {extension}")
        
        if f".{extension}" not in settings.ALLOWED_EXTENSIONS:
            logger.error(f"Invalid extension: {extension}")
            raise HTTPException(
                status_code=400,
                detail=f"File type not supported. Allowed: {settings.ALLOWED_EXTENSIONS}"
            )
        
        # Read file
        file_content = await file.read()
        logger.info(f"File content size: {len(file_content)} bytes")
        
        if len(file_content) > settings.MAX_UPLOAD_SIZE:
            logger.error(f"File too large: {len(file_content)} bytes")
            raise HTTPException(status_code=400, detail="File too large")
        
        # Parse file
        logger.info("Parsing file content...")
        raw_text = await FileParser.parse_file(file.filename, file_content)
        logger.info(f"Extracted text length: {len(raw_text)} characters")
        
        if not raw_text or len(raw_text) < 50:
            logger.error("Extracted text too short or empty")
            raise HTTPException(status_code=400, detail="Could not extract text from file. Please ensure your resume has readable text.")
        
        # Parse resume with LLM
        logger.info("Parsing resume with LLM...")
        resume_data = await resume_parser.parse(raw_text)
        
        # Detect possible roles
        logger.info("Detecting target roles...")
        detected_roles = await resume_parser.detect_target_roles(resume_data)
        
        # Generate session ID
        session_id = str(uuid.uuid4())
        
        logger.info(f"Resume uploaded and parsed successfully, session: {session_id}")
        
        return ResumeUploadResponse(
            session_id=session_id,
            resume_data=resume_data,
            detected_roles=detected_roles,
            message="Resume parsed successfully"
        )
        
    except ValueError as e:
        logger.error(f"ValueError in upload: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading resume: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to process resume: {str(e)}")

@router.post("/start-interview")
async def start_interview(request: StartInterviewRequest):
    """Start interview session"""
    try:
        # This requires the resume data to be stored or passed
        # For simplicity, we'll fetch from session if it exists
        # In production, use a database
        
        # Create a minimal resume data for demo
        from app.models.resume import ResumeData
        
        # In production, retrieve stored resume data
        resume_data = ResumeData(raw_text="Sample resume")
        
        # Start interview
        session = await interview_service.start_interview(
            request.session_id,
            resume_data,
            request.target_role
        )
        
        # Return first question
        first_question = session.questions[0].question
        
        return {
            "success": True,
            "session_id": session.session_id,
            "question": first_question.dict(),
            "question_number": 1,
            "total_questions": settings.TOTAL_QUESTIONS,
            "prep_time_seconds": settings.PREP_TIME_SECONDS,
            "answer_time_seconds": settings.ANSWER_TIME_SECONDS
        }
        
    except Exception as e:
        logger.error(f"Error starting interview: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/submit-answer", response_model=SubmitAnswerResponse)
async def submit_answer(request: SubmitAnswerRequest):
    """Submit answer to current question"""
    try:
        # Validate answer
        if not is_valid_answer(request.answer_text):
            raise HTTPException(
                status_code=400,
                detail="Answer is too short or invalid. Please provide a meaningful response."
            )
        
        # Process answer
        response = await interview_service.submit_answer(
            request.session_id,
            request.question_id,
            request.answer_text,
            request.duration_seconds,
            request.is_voice
        )
        
        return response
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error submitting answer: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/submit-followup")
async def submit_followup(request: SubmitAnswerRequest):
    """Submit answer to follow-up question"""
    try:
        response = await interview_service.submit_followup_answer(
            request.session_id,
            request.answer_text,
            request.duration_seconds
        )
        
        return response
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error submitting follow-up: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/session/{session_id}")
async def get_session(session_id: str):
    """Get session status"""
    try:
        session = interview_service.get_session(session_id)
        
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        return {
            "session_id": session.session_id,
            "status": session.status,
            "current_question": session.current_question_index + 1,
            "total_questions": len(session.questions),
            "target_role": session.target_role
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching session: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-report")
async def generate_report(request: ReportGenerationRequest):
    """Generate performance report"""
    try:
        # Get session
        session = interview_service.get_session(request.session_id)
        
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        if session.status != "completed":
            raise HTTPException(status_code=400, detail="Interview not completed")
        
        # Get evaluations
        evaluations = interview_service.get_session_evaluations(request.session_id)
        
        # Generate report
        report = await report_gen.generate_report(session, evaluations)
        
        # Export based on format
        if request.export_format == "pdf":
            pdf_bytes = pdf_service.generate_report_pdf(report)
            
            return StreamingResponse(
                BytesIO(pdf_bytes),
                media_type="application/pdf",
                headers={
                    "Content-Disposition": f"attachment; filename=interview_report_{request.session_id}.pdf"
                }
            )
        
        elif request.export_format == "json":
            return JSONResponse(content=json.loads(report.json()))
        
        else:  # both
            pdf_bytes = pdf_service.generate_report_pdf(report)
            
            return {
                "json_report": json.loads(report.json()),
                "pdf_available": True,
                "pdf_download_url": f"/api/download-pdf/{request.session_id}"
            }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/download-pdf/{session_id}")
async def download_pdf(session_id: str):
    """Download PDF report"""
    try:
        session = interview_service.get_session(session_id)
        
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        evaluations = interview_service.get_session_evaluations(session_id)
        report = await report_gen.generate_report(session, evaluations)
        
        pdf_bytes = pdf_service.generate_report_pdf(report)
        
        return StreamingResponse(
            BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=interview_report_{session_id}.pdf"
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "interview-practice-partner-api",
        "llm_provider": settings.LLM_PROVIDER
    }

"""
Interview Practice Partner Backend
Main FastAPI application entry point
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging

from app.config import settings
from app.api import routes
from app.utils.logger import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Interview Practice Partner API",
    description="Intelligent conversational AI for mock job interviews",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(routes.router, prefix="/api")

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Interview Practice Partner API",
        "version": "1.0.0",
        "status": "active",
        "docs": "/docs"
    }

# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "service": "interview-practice-partner",
        "version": "1.0.0"
    }

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "message": str(exc) if settings.LOG_LEVEL == "DEBUG" else "An error occurred"
        }
    )

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Interview Practice Partner API starting up...")
    logger.info(f"Using LLM Provider: {settings.LLM_PROVIDER}")
    logger.info(f"Model: {settings.LLM_MODEL}")
    
# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Interview Practice Partner API shutting down...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

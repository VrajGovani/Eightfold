"""
Configuration management using Pydantic Settings
"""
from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    """Application settings"""
    
    # API Keys
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    
    # LLM Configuration
    LLM_PROVIDER: str = "openai"  # openai, anthropic, local
    LLM_MODEL: str = "gpt-4-turbo-preview"
    MAX_TOKENS: int = 2000
    TEMPERATURE: float = 0.7
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Database
    DATABASE_URL: str = "sqlite:///./interview_practice.db"
    
    # Security
    SECRET_KEY: str = "change-this-in-production"
    
    # File Upload
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: List[str] = [".pdf", ".docx", ".txt"]
    
    # Interview Settings
    PREP_TIME_SECONDS: int = 30
    ANSWER_TIME_SECONDS: int = 180  # 3 minutes
    TOTAL_QUESTIONS: int = 5
    
    # Paths
    UPLOAD_DIR: str = "uploads"
    REPORT_DIR: str = "reports"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Create directories if they don't exist
        os.makedirs(self.UPLOAD_DIR, exist_ok=True)
        os.makedirs(self.REPORT_DIR, exist_ok=True)

# Create settings instance
settings = Settings()

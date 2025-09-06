"""
Configuration settings for AI Job Readiness Platform

This module contains all configuration settings for the application,
including database, security, and environment-specific settings.

Author: AI Job Readiness Team
Version: 1.0.0
"""

import os
from typing import Optional, List, Any, Dict, Union
from pydantic_settings import BaseSettings
from pydantic import validator
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """
    Application settings configuration.
    
    This class manages all configuration settings for the application,
    including database connections, security settings, and API configuration.
    """
    
    # Application settings
    app_name: str = "AI Job Readiness API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Database settings
    database_url: Optional[str] = "sqlite+aiosqlite:///./ai_job_readiness.db"
    postgres_user: str = "postgres"
    postgres_password: str = "password"
    postgres_host: str = "localhost"
    postgres_port: str = "5432"
    postgres_db: str = "ai_job_readiness"
    
    # Security settings
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # JWT settings (for compatibility)
    jwt_secret: str = "supersecretkey"
    jwt_algorithm: str = "HS256"
    
    # API Keys
    openai_api_key: str = "your_openai_key"
    coursera_api_key: str = "your_coursera_key"
    
    # FastAPI-Users settings
    users_secret: str = "your-users-secret-change-in-production"
    verification_token_secret: str = "your-verification-secret-change-in-production"
    reset_password_token_secret: str = "your-reset-password-secret-change-in-production"
    verification_token_expire_hours: int = 24
    reset_password_token_expire_hours: int = 1
    
    # Email settings (for user verification and password reset)
    smtp_tls: bool = True
    smtp_port: Optional[int] = None
    smtp_host: Optional[str] = None
    smtp_user: Optional[str] = None
    smtp_password: Optional[str] = None
    emails_from_email: Optional[str] = None
    emails_from_name: Optional[str] = None
    
    # CORS settings
    backend_cors_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
    ]
    
    # API settings
    api_v1_str: str = "/api/v1"
    project_name: str = "AI Job Readiness Platform"
    
    # Logging settings
    log_level: str = "INFO"
    sql_echo: bool = False
    
    @validator("database_url", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        """Assemble database URL from individual components if not provided."""
        if isinstance(v, str):
            return v
        
        user = values.get("postgres_user")
        password = values.get("postgres_password")
        host = values.get("postgres_host")
        port = values.get("postgres_port")
        db = values.get("postgres_db")
        
        return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"
    
    @validator("backend_cors_origins", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        """Parse CORS origins from string or list."""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # Allow extra fields for backward compatibility


# Create global settings instance
settings = Settings()

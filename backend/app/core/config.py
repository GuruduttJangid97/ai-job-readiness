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
from pydantic import validator, Field
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class DatabaseSettings(BaseSettings):
    """Database configuration settings."""
    
    url: Optional[str] = Field(None, description="Complete database URL")
    user: str = Field("postgres", description="Database username")
    password: str = Field("password", description="Database password")
    host: str = Field("localhost", description="Database host")
    port: str = Field("5432", description="Database port")
    name: str = Field("ai_job_readiness", description="Database name")
    echo: bool = Field(False, description="Enable SQL query logging")
    pool_size: int = Field(10, description="Database connection pool size")
    max_overflow: int = Field(20, description="Maximum overflow connections")
    pool_pre_ping: bool = Field(True, description="Enable connection pre-ping")
    pool_recycle: int = Field(3600, description="Connection recycle time in seconds")
    
    @validator("url", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        """Assemble database URL from individual components if not provided."""
        if v:
            return v
        
        user = values.get("user")
        password = values.get("password")
        host = values.get("host")
        port = values.get("port")
        name = values.get("name")
        
        return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}"


class SecuritySettings(BaseSettings):
    """Security configuration settings."""
    
    secret_key: str = Field("your-secret-key-change-in-production", description="JWT secret key")
    algorithm: str = Field("HS256", description="JWT algorithm")
    access_token_expire_minutes: int = Field(30, description="Access token expiration in minutes")
    refresh_token_expire_days: int = Field(7, description="Refresh token expiration in days")
    
    # FastAPI-Users settings
    users_secret: str = Field("your-users-secret-change-in-production", description="FastAPI-Users secret")
    verification_token_secret: str = Field("your-verification-secret-change-in-production", description="Verification token secret")
    reset_password_token_secret: str = Field("your-reset-password-secret-change-in-production", description="Reset password token secret")
    verification_token_expire_hours: int = Field(24, description="Verification token expiration in hours")
    reset_password_token_expire_hours: int = Field(1, description="Reset password token expiration in hours")
    
    # Password requirements
    min_password_length: int = Field(8, description="Minimum password length")
    require_uppercase: bool = Field(True, description="Require uppercase letters in password")
    require_lowercase: bool = Field(True, description="Require lowercase letters in password")
    require_digits: bool = Field(True, description="Require digits in password")
    require_special_chars: bool = Field(False, description="Require special characters in password")


class EmailSettings(BaseSettings):
    """Email configuration settings."""
    
    smtp_tls: bool = Field(True, description="Enable SMTP TLS")
    smtp_port: Optional[int] = Field(None, description="SMTP port")
    smtp_host: Optional[str] = Field(None, description="SMTP host")
    smtp_user: Optional[str] = Field(None, description="SMTP username")
    smtp_password: Optional[str] = Field(None, description="SMTP password")
    from_email: Optional[str] = Field(None, description="From email address")
    from_name: Optional[str] = Field("AI Job Readiness", description="From name")


class APISettings(BaseSettings):
    """API configuration settings."""
    
    title: str = Field("AI Job Readiness API", description="API title")
    version: str = Field("1.0.0", description="API version")
    description: str = Field("Comprehensive job readiness assessment and analysis platform", description="API description")
    v1_str: str = Field("/api/v1", description="API v1 prefix")
    project_name: str = Field("AI Job Readiness Platform", description="Project name")
    
    # CORS settings
    cors_origins: List[str] = Field(
        default=[
            "http://localhost:3000",
            "http://localhost:3001",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:3001",
        ],
        description="Allowed CORS origins"
    )
    
    @validator("cors_origins", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        """Parse CORS origins from string or list."""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)


class FileSettings(BaseSettings):
    """File upload and storage settings."""
    
    upload_dir: str = Field("uploads", description="Base upload directory")
    resume_dir: str = Field("resumes", description="Resume upload subdirectory")
    max_file_size: int = Field(10 * 1024 * 1024, description="Maximum file size in bytes")
    allowed_extensions: List[str] = Field(
        default=[".pdf", ".doc", ".docx", ".txt"],
        description="Allowed file extensions"
    )
    
    @property
    def resume_upload_dir(self) -> str:
        """Get the full path to resume upload directory."""
        return os.path.join(self.upload_dir, self.resume_dir)


class LoggingSettings(BaseSettings):
    """Logging configuration settings."""
    
    level: str = Field("INFO", description="Logging level")
    format: str = Field(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log format"
    )
    file_path: Optional[str] = Field(None, description="Log file path")
    max_file_size: int = Field(10 * 1024 * 1024, description="Maximum log file size")
    backup_count: int = Field(5, description="Number of backup log files")


class AISettings(BaseSettings):
    """AI service configuration settings."""
    
    openai_api_key: str = Field("your_openai_key", description="OpenAI API key")
    coursera_api_key: str = Field("your_coursera_key", description="Coursera API key")
    model_version: str = Field("v1.0", description="AI model version")
    confidence_threshold: float = Field(0.7, description="Minimum confidence threshold for AI predictions")


class Settings(BaseSettings):
    """
    Main application settings configuration.
    
    This class manages all configuration settings for the application,
    including database connections, security settings, and API configuration.
    """
    
    # Environment
    environment: str = Field("development", description="Environment (development/staging/production)")
    debug: bool = Field(False, description="Debug mode")
    
    # Sub-configurations
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    security: SecuritySettings = Field(default_factory=SecuritySettings)
    email: EmailSettings = Field(default_factory=EmailSettings)
    api: APISettings = Field(default_factory=APISettings)
    file: FileSettings = Field(default_factory=FileSettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)
    ai: AISettings = Field(default_factory=AISettings)
    
    # Legacy compatibility properties
    @property
    def database_url(self) -> str:
        """Legacy property for backward compatibility."""
        return self.database.url
    
    @property
    def backend_cors_origins(self) -> List[str]:
        """Legacy property for backward compatibility."""
        return self.api.cors_origins
    
    @property
    def api_v1_str(self) -> str:
        """Legacy property for backward compatibility."""
        return self.api.v1_str
    
    @property
    def project_name(self) -> str:
        """Legacy property for backward compatibility."""
        return self.api.project_name
    
    @property
    def sql_echo(self) -> bool:
        """Legacy property for backward compatibility."""
        return self.database.echo
    
    @property
    def log_level(self) -> str:
        """Legacy property for backward compatibility."""
        return self.logging.level
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # Allow extra fields for backward compatibility


# Create global settings instance
settings = Settings()
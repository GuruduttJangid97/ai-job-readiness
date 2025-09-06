"""
Resume Pydantic Schemas for AI Job Readiness Platform

This module defines Pydantic schemas for resume-related operations including
creation, updates, reading, and validation. These schemas ensure data integrity
and provide clear API documentation.

The schemas include:
- ResumeCreate: For creating new resumes
- ResumeUpdate: For updating existing resumes
- ResumeRead: For reading resume data
- ResumeResponse: For API responses
- ResumeListResponse: For paginated resume lists

Author: AI Job Readiness Team
Version: 1.0.0
"""

import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, validator, field_validator, ConfigDict


class ResumeBase(BaseModel):
    """
    Base schema for resume operations.
    
    This schema contains common fields shared across all resume operations
    and provides validation for resume data.
    """
    title: str = Field(
        ..., 
        min_length=1, 
        max_length=200,
        description="Title or name of the resume"
    )
    summary: Optional[str] = Field(
        None,
        max_length=5000,
        description="Resume summary or objective"
    )
    experience_years: Optional[float] = Field(
        None,
        ge=0,
        le=100,
        description="Total years of work experience"
    )
    education_level: Optional[str] = Field(
        None,
        max_length=100,
        description="Highest education level achieved"
    )
    skills: Optional[List[str]] = Field(
        None,
        description="List of skills extracted from resume"
    )
    languages: Optional[List[Dict[str, Any]]] = Field(
        None,
        description="List of languages with proficiency levels"
    )
    is_public: bool = Field(
        False,
        description="Whether the resume is publicly visible"
    )

    @validator('skills')
    def validate_skills(cls, v):
        """Validate skills list."""
        if v is not None:
            if len(v) > 100:
                raise ValueError('Too many skills (max 100)')
            for skill in v:
                if not isinstance(skill, str) or len(skill.strip()) == 0:
                    raise ValueError('All skills must be non-empty strings')
        return v

    @validator('languages')
    def validate_languages(cls, v):
        """Validate languages list."""
        if v is not None:
            if len(v) > 20:
                raise ValueError('Too many languages (max 20)')
            for lang in v:
                if not isinstance(lang, dict):
                    raise ValueError('All languages must be dictionaries')
                if 'name' not in lang:
                    raise ValueError('Language must have a name')
        return v


class ResumeCreate(ResumeBase):
    """
    Schema for creating a new resume.
    
    This schema is used when creating a new resume and includes
    all the necessary fields for resume creation.
    """
    file_name: Optional[str] = Field(
        None,
        max_length=255,
        description="Original filename of the resume"
    )
    file_type: Optional[str] = Field(
        None,
        max_length=50,
        description="File type (PDF, DOC, DOCX, etc.)"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Software Engineer Resume",
                "summary": "Experienced software engineer with 5+ years in full-stack development",
                "experience_years": 5.5,
                "education_level": "Bachelor's Degree",
                "skills": ["Python", "JavaScript", "React", "Node.js", "PostgreSQL"],
                "languages": [
                    {"name": "English", "proficiency": "Native"},
                    {"name": "Spanish", "proficiency": "Intermediate"}
                ],
                "is_public": False,
                "file_name": "john_doe_resume.pdf",
                "file_type": "PDF"
            }
        }
    )


class ResumeUpdate(BaseModel):
    """
    Schema for updating an existing resume.
    
    This schema allows partial updates of resume fields.
    All fields are optional to support partial updates.
    """
    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=200,
        description="Title or name of the resume"
    )
    summary: Optional[str] = Field(
        None,
        max_length=5000,
        description="Resume summary or objective"
    )
    experience_years: Optional[float] = Field(
        None,
        ge=0,
        le=100,
        description="Total years of work experience"
    )
    education_level: Optional[str] = Field(
        None,
        max_length=100,
        description="Highest education level achieved"
    )
    skills: Optional[List[str]] = Field(
        None,
        description="List of skills extracted from resume"
    )
    languages: Optional[List[Dict[str, Any]]] = Field(
        None,
        description="List of languages with proficiency levels"
    )
    is_active: Optional[bool] = Field(
        None,
        description="Whether the resume is active"
    )
    is_public: Optional[bool] = Field(
        None,
        description="Whether the resume is publicly visible"
    )

    @validator('skills')
    def validate_skills(cls, v):
        """Validate skills list."""
        if v is not None:
            if len(v) > 100:
                raise ValueError('Too many skills (max 100)')
            for skill in v:
                if not isinstance(skill, str) or len(skill.strip()) == 0:
                    raise ValueError('All skills must be non-empty strings')
        return v

    @validator('languages')
    def validate_languages(cls, v):
        """Validate languages list."""
        if v is not None:
            if len(v) > 20:
                raise ValueError('Too many languages (max 20)')
            for lang in v:
                if not isinstance(lang, dict):
                    raise ValueError('All languages must be dictionaries')
                if 'name' not in lang:
                    raise ValueError('Language must have a name')
        return v

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Senior Software Engineer Resume",
                "summary": "Senior software engineer with 8+ years in full-stack development",
                "experience_years": 8.0,
                "skills": ["Python", "JavaScript", "React", "Node.js", "PostgreSQL", "Docker", "AWS"],
                "is_public": True
            }
        }
    )


class ResumeRead(ResumeBase):
    """
    Schema for reading resume data.
    
    This schema includes all resume fields including metadata
    and is used for API responses when reading resume data.
    """
    id: int = Field(..., description="Unique identifier for the resume")
    user_id: uuid.UUID = Field(..., description="ID of the user who owns this resume")
    file_name: Optional[str] = Field(None, description="Original filename of the resume")
    file_size: Optional[int] = Field(None, description="File size in bytes")
    file_size_mb: Optional[float] = Field(None, description="File size in megabytes")
    file_type: Optional[str] = Field(None, description="File type (PDF, DOC, DOCX, etc.)")
    is_active: bool = Field(..., description="Whether the resume is active")
    last_analyzed: Optional[datetime] = Field(None, description="Last analysis timestamp")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    needs_analysis: bool = Field(..., description="Whether the resume needs analysis")

    @field_validator('skills', mode='before')
    @classmethod
    def parse_skills(cls, v):
        """Parse skills from JSON string or list."""
        if isinstance(v, str):
            try:
                import json
                return json.loads(v)
            except (json.JSONDecodeError, TypeError):
                return []
        return v or []

    @field_validator('languages', mode='before')
    @classmethod
    def parse_languages(cls, v):
        """Parse languages from JSON string or list."""
        if isinstance(v, str):
            try:
                import json
                return json.loads(v)
            except (json.JSONDecodeError, TypeError):
                return []
        return v or []

    @field_validator('needs_analysis', mode='before')
    @classmethod
    def parse_needs_analysis(cls, v):
        """Parse needs_analysis from method or boolean."""
        if callable(v):
            return v()
        return bool(v)

    model_config = ConfigDict(from_attributes=True)


class ResumeResponse(ResumeRead):
    """
    Schema for resume API responses.
    
    This schema extends ResumeRead with additional computed fields
    and is used for API responses.
    """
    pass


class ResumeListResponse(BaseModel):
    """
    Schema for paginated resume list responses.
    
    This schema is used when returning a list of resumes
    with pagination information.
    """
    resumes: List[ResumeResponse] = Field(..., description="List of resumes")
    total: int = Field(..., description="Total number of resumes")
    page: int = Field(..., description="Current page number")
    size: int = Field(..., description="Number of resumes per page")
    pages: int = Field(..., description="Total number of pages")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "resumes": [
                    {
                        "id": 1,
                        "user_id": "123e4567-e89b-12d3-a456-426614174000",
                        "title": "Software Engineer Resume",
                        "summary": "Experienced software engineer...",
                        "experience_years": 5.5,
                        "education_level": "Bachelor's Degree",
                        "skills": ["Python", "JavaScript", "React"],
                        "languages": [{"name": "English", "proficiency": "Native"}],
                        "is_active": True,
                        "is_public": False,
                        "created_at": "2024-01-01T00:00:00Z",
                        "needs_analysis": True
                    }
                ],
                "total": 1,
                "page": 1,
                "size": 10,
                "pages": 1
            }
        }
    )


class ResumeFileUpload(BaseModel):
    """
    Schema for resume file upload operations.
    
    This schema is used when uploading resume files
    and includes file-specific validation.
    """
    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Title or name for the resume"
    )
    is_public: bool = Field(
        False,
        description="Whether the resume should be publicly visible"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "My Professional Resume",
                "is_public": False
            }
        }
    )


class ResumeAnalysisRequest(BaseModel):
    """
    Schema for requesting resume analysis.
    
    This schema is used when requesting analysis
    of a resume against a specific job posting.
    """
    job_title: Optional[str] = Field(
        None,
        max_length=200,
        description="Job title to analyze against"
    )
    company: Optional[str] = Field(
        None,
        max_length=200,
        description="Company name"
    )
    job_description: Optional[str] = Field(
        None,
        max_length=10000,
        description="Job description text"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "job_title": "Senior Software Engineer",
                "company": "Tech Corp",
                "job_description": "We are looking for a senior software engineer..."
            }
        }
    )


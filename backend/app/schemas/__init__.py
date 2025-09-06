"""
Pydantic schemas for AI Job Readiness Platform

This module contains all Pydantic schemas used for request/response validation,
data serialization, and API documentation in the AI Job Readiness platform.

Author: AI Job Readiness Team
Version: 1.0.0
"""

from .user import (
    UserCreate,
    UserUpdate,
    UserRead,
    UserProfile,
    UserProfileUpdate,
    UserResponse,
    UserListResponse
)

from .resume import (
    ResumeCreate,
    ResumeUpdate,
    ResumeRead,
    ResumeResponse,
    ResumeListResponse,
    ResumeFileUpload,
    ResumeAnalysisRequest
)

__all__ = [
    "UserCreate",
    "UserUpdate", 
    "UserRead",
    "UserProfile",
    "UserProfileUpdate",
    "UserResponse",
    "UserListResponse",
    "ResumeCreate",
    "ResumeUpdate",
    "ResumeRead",
    "ResumeResponse",
    "ResumeListResponse",
    "ResumeFileUpload",
    "ResumeAnalysisRequest"
]

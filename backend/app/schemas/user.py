"""
User Pydantic schemas for AI Job Readiness Platform

This module defines Pydantic schemas for user-related operations including
registration, authentication, profile management, and data validation.

The schemas extend FastAPI-Users base schemas to provide comprehensive
user management capabilities with additional profile fields and validation.

Author: AI Job Readiness Team
Version: 1.0.0
"""

import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, EmailStr, Field, validator
from fastapi_users import schemas


class UserBase(BaseModel):
    """
    Base user schema with common fields.
    
    This schema contains fields that are common across different user operations
    and provides validation for user data.
    """
    email: EmailStr = Field(..., description="User's email address")
    first_name: Optional[str] = Field(None, max_length=100, description="User's first name")
    last_name: Optional[str] = Field(None, max_length=100, description="User's last name")
    phone: Optional[str] = Field(None, max_length=20, description="User's phone number")
    bio: Optional[str] = Field(None, max_length=1000, description="User's biography")
    profile_picture_url: Optional[str] = Field(None, max_length=500, description="URL to user's profile picture")
    
    @validator('phone')
    def validate_phone(cls, v):
        """Validate phone number format if provided."""
        if v is not None:
            # Remove all non-digit characters for validation
            digits_only = ''.join(filter(str.isdigit, v))
            if len(digits_only) < 10 or len(digits_only) > 15:
                raise ValueError('Phone number must be between 10 and 15 digits')
        return v
    
    @validator('profile_picture_url')
    def validate_profile_picture_url(cls, v):
        """Validate profile picture URL format if provided."""
        if v is not None:
            if not (v.startswith('http://') or v.startswith('https://')):
                raise ValueError('Profile picture URL must start with http:// or https://')
        return v


class UserCreate(UserBase, schemas.BaseUserCreate):
    """
    Schema for user creation/registration.
    
    Extends FastAPI-Users BaseUserCreate with additional profile fields.
    This schema is used for user registration endpoints.
    """
    password: str = Field(..., min_length=8, max_length=100, description="User's password")
    
    @validator('password')
    def validate_password(cls, v):
        """Validate password strength."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v


class UserUpdate(UserBase, schemas.BaseUserUpdate):
    """
    Schema for user updates.
    
    Extends FastAPI-Users BaseUserUpdate with additional profile fields.
    This schema is used for updating user information.
    """
    pass


class UserRead(UserBase, schemas.BaseUser[uuid.UUID]):
    """
    Schema for reading user data.
    
    Extends FastAPI-Users BaseUser with additional profile fields.
    This schema is used for returning user data in API responses.
    """
    id: uuid.UUID = Field(..., description="User's unique identifier")
    is_active: bool = Field(..., description="Whether the user account is active")
    is_superuser: bool = Field(..., description="Whether the user has superuser privileges")
    is_verified: bool = Field(..., description="Whether the user's email is verified")
    created_at: datetime = Field(..., description="Timestamp when the user was created")
    updated_at: Optional[datetime] = Field(None, description="Timestamp when the user was last updated")
    
    class Config:
        from_attributes = True


class UserProfile(BaseModel):
    """
    Schema for user profile information.
    
    This schema provides a comprehensive view of user profile data
    including computed fields like full_name and role information.
    """
    id: uuid.UUID = Field(..., description="User's unique identifier")
    email: EmailStr = Field(..., description="User's email address")
    first_name: Optional[str] = Field(None, description="User's first name")
    last_name: Optional[str] = Field(None, description="User's last name")
    full_name: str = Field(..., description="User's full name")
    phone: Optional[str] = Field(None, description="User's phone number")
    bio: Optional[str] = Field(None, description="User's biography")
    profile_picture_url: Optional[str] = Field(None, description="URL to user's profile picture")
    is_active: bool = Field(..., description="Whether the user account is active")
    is_verified: bool = Field(..., description="Whether the user's email is verified")
    created_at: datetime = Field(..., description="Timestamp when the user was created")
    updated_at: Optional[datetime] = Field(None, description="Timestamp when the user was last updated")
    roles: List[str] = Field(default_factory=list, description="List of user's role names")
    role_assignments: Optional[List[Dict[str, Any]]] = Field(default_factory=list, description="Detailed role assignment information")
    
    class Config:
        from_attributes = True


class UserProfileUpdate(BaseModel):
    """
    Schema for updating user profile information.
    
    This schema allows users to update their profile information
    without affecting authentication-related fields.
    """
    first_name: Optional[str] = Field(None, max_length=100, description="User's first name")
    last_name: Optional[str] = Field(None, max_length=100, description="User's last name")
    phone: Optional[str] = Field(None, max_length=20, description="User's phone number")
    bio: Optional[str] = Field(None, max_length=1000, description="User's biography")
    profile_picture_url: Optional[str] = Field(None, max_length=500, description="URL to user's profile picture")
    
    @validator('phone')
    def validate_phone(cls, v):
        """Validate phone number format if provided."""
        if v is not None:
            # Remove all non-digit characters for validation
            digits_only = ''.join(filter(str.isdigit, v))
            if len(digits_only) < 10 or len(digits_only) > 15:
                raise ValueError('Phone number must be between 10 and 15 digits')
        return v
    
    @validator('profile_picture_url')
    def validate_profile_picture_url(cls, v):
        """Validate profile picture URL format if provided."""
        if v is not None:
            if not (v.startswith('http://') or v.startswith('https://')):
                raise ValueError('Profile picture URL must start with http:// or https://')
        return v


class UserResponse(BaseModel):
    """
    Standard user response schema.
    
    This schema provides a consistent format for user-related API responses
    with success status and message information.
    """
    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Response message")
    data: Optional[UserProfile] = Field(None, description="User data if applicable")
    
    class Config:
        from_attributes = True


class UserListResponse(BaseModel):
    """
    Schema for user list responses.
    
    This schema provides pagination and filtering capabilities
    for user list endpoints.
    """
    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Response message")
    data: List[UserProfile] = Field(..., description="List of users")
    total: int = Field(..., description="Total number of users")
    page: int = Field(..., description="Current page number")
    per_page: int = Field(..., description="Number of users per page")
    has_next: bool = Field(..., description="Whether there are more pages")
    has_prev: bool = Field(..., description="Whether there are previous pages")
    
    class Config:
        from_attributes = True


class UserLoginRequest(BaseModel):
    """
    Schema for user login requests.
    
    This schema handles user authentication requests
    with email and password validation.
    """
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., description="User's password")
    
    class Config:
        from_attributes = True


class UserLoginResponse(BaseModel):
    """
    Schema for user login responses.
    
    This schema provides authentication tokens and user information
    after successful login.
    """
    success: bool = Field(..., description="Whether the login was successful")
    message: str = Field(..., description="Response message")
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")
    user: UserProfile = Field(..., description="User profile information")
    
    class Config:
        from_attributes = True


class PasswordChangeRequest(BaseModel):
    """
    Schema for password change requests.
    
    This schema handles password change operations
    with current and new password validation.
    """
    current_password: str = Field(..., description="Current password")
    new_password: str = Field(..., min_length=8, max_length=100, description="New password")
    
    @validator('new_password')
    def validate_new_password(cls, v):
        """Validate new password strength."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v
    
    class Config:
        from_attributes = True


class PasswordResetRequest(BaseModel):
    """
    Schema for password reset requests.
    
    This schema handles password reset operations
    for users who have forgotten their passwords.
    """
    email: EmailStr = Field(..., description="User's email address")
    
    class Config:
        from_attributes = True


class PasswordResetConfirm(BaseModel):
    """
    Schema for password reset confirmation.
    
    This schema handles password reset confirmation
    with token and new password validation.
    """
    token: str = Field(..., description="Password reset token")
    new_password: str = Field(..., min_length=8, max_length=100, description="New password")
    
    @validator('new_password')
    def validate_new_password(cls, v):
        """Validate new password strength."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one digit')
        return v
    
    class Config:
        from_attributes = True

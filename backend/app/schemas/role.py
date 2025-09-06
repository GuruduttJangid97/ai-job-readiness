"""
Role Pydantic schemas for AI Job Readiness Platform

This module defines Pydantic schemas for role-related operations including
role creation, updates, assignment, and data validation.

The schemas provide comprehensive role management capabilities with
permission handling and validation.

Author: AI Job Readiness Team
Version: 1.0.0
"""

import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator


class RoleBase(BaseModel):
    """
    Base role schema with common fields.
    
    This schema contains fields that are common across different role operations
    and provides validation for role data.
    """
    name: str = Field(..., min_length=2, max_length=50, description="Role name (e.g., 'admin', 'user', 'moderator')")
    description: Optional[str] = Field(None, max_length=1000, description="Role description")
    permissions: Optional[List[str]] = Field(default_factory=list, description="List of permissions for this role")
    is_active: bool = Field(True, description="Whether the role is active and can be assigned")
    
    @validator('name')
    def validate_name(cls, v):
        """Validate role name format."""
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Role name must contain only alphanumeric characters, hyphens, and underscores')
        return v.lower()
    
    @validator('permissions')
    def validate_permissions(cls, v):
        """Validate permissions list."""
        if v is not None:
            for permission in v:
                if not isinstance(permission, str) or not permission.strip():
                    raise ValueError('All permissions must be non-empty strings')
        return v


class RoleCreate(RoleBase):
    """
    Schema for role creation.
    
    This schema is used for creating new roles in the system.
    """
    pass


class RoleUpdate(BaseModel):
    """
    Schema for role updates.
    
    This schema allows updating role information without requiring all fields.
    """
    name: Optional[str] = Field(None, min_length=2, max_length=50, description="Role name")
    description: Optional[str] = Field(None, max_length=1000, description="Role description")
    permissions: Optional[List[str]] = Field(None, description="List of permissions for this role")
    is_active: Optional[bool] = Field(None, description="Whether the role is active")
    
    @validator('name')
    def validate_name(cls, v):
        """Validate role name format if provided."""
        if v is not None:
            if not v.replace('_', '').replace('-', '').isalnum():
                raise ValueError('Role name must contain only alphanumeric characters, hyphens, and underscores')
        return v.lower() if v else v
    
    @validator('permissions')
    def validate_permissions(cls, v):
        """Validate permissions list if provided."""
        if v is not None:
            for permission in v:
                if not isinstance(permission, str) or not permission.strip():
                    raise ValueError('All permissions must be non-empty strings')
        return v


class RoleRead(RoleBase):
    """
    Schema for reading role data.
    
    This schema is used for returning role data in API responses.
    """
    id: int = Field(..., description="Role's unique identifier")
    created_at: datetime = Field(..., description="Timestamp when the role was created")
    updated_at: Optional[datetime] = Field(None, description="Timestamp when the role was last updated")
    
    class Config:
        from_attributes = True


class RoleResponse(BaseModel):
    """
    Standard role response schema.
    
    This schema provides a consistent format for role-related API responses
    with success status and message information.
    """
    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Response message")
    data: Optional[RoleRead] = Field(None, description="Role data if applicable")
    
    class Config:
        from_attributes = True


class RoleListResponse(BaseModel):
    """
    Schema for role list responses.
    
    This schema provides pagination and filtering capabilities
    for role list endpoints.
    """
    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Response message")
    data: List[RoleRead] = Field(..., description="List of roles")
    total: int = Field(..., description="Total number of roles")
    page: int = Field(..., description="Current page number")
    per_page: int = Field(..., description="Number of roles per page")
    has_next: bool = Field(..., description="Whether there are more pages")
    has_prev: bool = Field(..., description="Whether there are previous pages")
    
    class Config:
        from_attributes = True


class UserRoleAssignment(BaseModel):
    """
    Schema for user-role assignment operations.
    
    This schema handles assigning roles to users and managing
    role assignments.
    """
    user_id: uuid.UUID = Field(..., description="ID of the user to assign the role to")
    role_id: int = Field(..., description="ID of the role to assign")
    assigned_by: Optional[uuid.UUID] = Field(None, description="ID of the user who is making the assignment")
    
    class Config:
        from_attributes = True


class UserRoleAssignmentResponse(BaseModel):
    """
    Schema for user-role assignment responses.
    
    This schema provides information about role assignments
    including metadata about when and by whom the role was assigned.
    """
    id: int = Field(..., description="Assignment's unique identifier")
    user_id: uuid.UUID = Field(..., description="ID of the user")
    role_id: int = Field(..., description="ID of the role")
    role_name: str = Field(..., description="Name of the role")
    assigned_at: datetime = Field(..., description="When the role was assigned")
    assigned_by: Optional[uuid.UUID] = Field(None, description="Who assigned this role")
    is_active: bool = Field(..., description="Whether the assignment is active")
    
    class Config:
        from_attributes = True


class UserRoleListResponse(BaseModel):
    """
    Schema for user role list responses.
    
    This schema provides a list of roles assigned to a specific user.
    """
    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Response message")
    data: List[UserRoleAssignmentResponse] = Field(..., description="List of user role assignments")
    total: int = Field(..., description="Total number of role assignments")
    
    class Config:
        from_attributes = True


class RolePermissionUpdate(BaseModel):
    """
    Schema for updating role permissions.
    
    This schema handles adding or removing permissions from roles.
    """
    permissions: List[str] = Field(..., description="List of permissions to set for the role")
    
    @validator('permissions')
    def validate_permissions(cls, v):
        """Validate permissions list."""
        if not v:
            raise ValueError('Permissions list cannot be empty')
        for permission in v:
            if not isinstance(permission, str) or not permission.strip():
                raise ValueError('All permissions must be non-empty strings')
        return v
    
    class Config:
        from_attributes = True


class RoleStats(BaseModel):
    """
    Schema for role statistics.
    
    This schema provides statistics about role usage and assignments.
    """
    total_roles: int = Field(..., description="Total number of roles")
    active_roles: int = Field(..., description="Number of active roles")
    total_assignments: int = Field(..., description="Total number of role assignments")
    active_assignments: int = Field(..., description="Number of active role assignments")
    most_used_roles: List[Dict[str, Any]] = Field(..., description="Most frequently assigned roles")
    
    class Config:
        from_attributes = True


class RoleStatsResponse(BaseModel):
    """
    Schema for role statistics responses.
    
    This schema provides role statistics in a consistent API response format.
    """
    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Response message")
    data: RoleStats = Field(..., description="Role statistics data")
    
    class Config:
        from_attributes = True

"""
User management API endpoints for AI Job Readiness Platform

This module provides user management endpoints including profile management,
user listing, and administrative user operations.

Author: AI Job Readiness Team
Version: 1.0.0
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from typing import Any, Dict, List, Optional
import uuid

from app.core.users import (
    current_active_user,
    current_superuser,
    get_user_manager,
    UserManager,
)
from app.db.database import get_db
from app.models.user import User
from app.models.role import Role, UserRole
from app.schemas.user import (
    UserProfile,
    UserProfileUpdate,
    UserResponse,
    UserListResponse,
    PasswordChangeRequest,
)

# Create router for user management endpoints
router = APIRouter(
    prefix="/users",
    tags=["User Management"],
    responses={
        404: {"description": "Not found"},
        422: {"description": "Validation error"},
        500: {"description": "Internal server error"},
    },
)


@router.get("/profile", response_model=UserResponse, tags=["User Management"])
async def get_user_profile(
    current_user: User = Depends(current_active_user),
) -> UserResponse:
    """
    Get current user's profile information.
    
    This endpoint returns the complete profile information of the
    currently authenticated user, including roles and relationships.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        UserResponse: User profile information
    """
    try:
        # Get user roles
        roles = [user_role.role.name for user_role in current_user.roles if user_role.role]
        
        user_profile = UserProfile(
            id=current_user.id,
            email=current_user.email,
            first_name=current_user.first_name,
            last_name=current_user.last_name,
            full_name=current_user.full_name,
            phone=current_user.phone,
            bio=current_user.bio,
            profile_picture_url=current_user.profile_picture_url,
            is_active=current_user.is_active,
            is_verified=current_user.is_verified,
            created_at=current_user.created_at,
            updated_at=current_user.updated_at,
            roles=roles,
        )
        
        return UserResponse(
            success=True,
            message="User profile retrieved successfully",
            data=user_profile,
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user profile",
        )


@router.put("/profile", response_model=UserResponse, tags=["User Management"])
async def update_user_profile(
    profile_update: UserProfileUpdate,
    current_user: User = Depends(current_active_user),
    user_manager: UserManager = Depends(get_user_manager),
) -> UserResponse:
    """
    Update current user's profile information.
    
    This endpoint allows users to update their profile information
    including name, phone, bio, and profile picture.
    
    Args:
        profile_update: Profile update data
        current_user: Current authenticated user
        user_manager: User manager dependency
        
    Returns:
        UserResponse: Updated user profile information
    """
    try:
        # Prepare update data
        update_data = {}
        
        if profile_update.first_name is not None:
            update_data["first_name"] = profile_update.first_name
        if profile_update.last_name is not None:
            update_data["last_name"] = profile_update.last_name
        if profile_update.phone is not None:
            update_data["phone"] = profile_update.phone
        if profile_update.bio is not None:
            update_data["bio"] = profile_update.bio
        if profile_update.profile_picture_url is not None:
            update_data["profile_picture_url"] = profile_update.profile_picture_url
        
        # Update user
        updated_user = await user_manager.update(current_user, update_data)
        
        # Get updated user roles
        roles = [user_role.role.name for user_role in updated_user.roles if user_role.role]
        
        user_profile = UserProfile(
            id=updated_user.id,
            email=updated_user.email,
            first_name=updated_user.first_name,
            last_name=updated_user.last_name,
            full_name=updated_user.full_name,
            phone=updated_user.phone,
            bio=updated_user.bio,
            profile_picture_url=updated_user.profile_picture_url,
            is_active=updated_user.is_active,
            is_verified=updated_user.is_verified,
            created_at=updated_user.created_at,
            updated_at=updated_user.updated_at,
            roles=roles,
        )
        
        return UserResponse(
            success=True,
            message="User profile updated successfully",
            data=user_profile,
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user profile",
        )


@router.post("/change-password", tags=["User Management"])
async def change_password(
    password_change: PasswordChangeRequest,
    current_user: User = Depends(current_active_user),
    user_manager: UserManager = Depends(get_user_manager),
) -> Dict[str, Any]:
    """
    Change current user's password.
    
    This endpoint allows users to change their password by providing
    their current password and a new password.
    
    Args:
        password_change: Password change request data
        current_user: Current authenticated user
        user_manager: User manager dependency
        
    Returns:
        Dict[str, Any]: Password change confirmation
    """
    try:
        # Verify current password
        if not user_manager.password_helper.verify(
            password_change.current_password, current_user.hashed_password
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect",
            )
        
        # Update password
        await user_manager.update(
            current_user, {"hashed_password": password_change.new_password}
        )
        
        return {
            "success": True,
            "message": "Password changed successfully",
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to change password",
        )


@router.get("/list", response_model=UserListResponse, tags=["User Management"])
async def list_users(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=100, description="Number of users per page"),
    search: Optional[str] = Query(None, description="Search term for name or email"),
    role: Optional[str] = Query(None, description="Filter by role name"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    current_user: User = Depends(current_superuser),
    db: AsyncSession = Depends(get_db),
) -> UserListResponse:
    """
    List users with pagination and filtering (Admin only).
    
    This endpoint allows administrators to list users with pagination,
    search, and filtering capabilities.
    
    Args:
        page: Page number for pagination
        per_page: Number of users per page
        search: Search term for name or email
        role: Filter by role name
        is_active: Filter by active status
        current_user: Current authenticated user (must be superuser)
        db: Database session
        
    Returns:
        UserListResponse: Paginated list of users
    """
    try:
        # Build query
        query = select(User)
        
        # Apply filters
        if search:
            search_filter = or_(
                User.first_name.ilike(f"%{search}%"),
                User.last_name.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%"),
            )
            query = query.where(search_filter)
        
        if is_active is not None:
            query = query.where(User.is_active == is_active)
        
        if role:
            query = query.join(UserRole).join(Role).where(Role.name == role)
        
        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        # Apply pagination
        offset = (page - 1) * per_page
        query = query.offset(offset).limit(per_page)
        
        # Execute query
        result = await db.execute(query)
        users = result.scalars().all()
        
        # Convert to UserProfile objects
        user_profiles = []
        for user in users:
            roles = [user_role.role.name for user_role in user.roles if user_role.role]
            user_profile = UserProfile(
                id=user.id,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
                full_name=user.full_name,
                phone=user.phone,
                bio=user.bio,
                profile_picture_url=user.profile_picture_url,
                is_active=user.is_active,
                is_verified=user.is_verified,
                created_at=user.created_at,
                updated_at=user.updated_at,
                roles=roles,
            )
            user_profiles.append(user_profile)
        
        # Calculate pagination info
        has_next = (page * per_page) < total
        has_prev = page > 1
        
        return UserListResponse(
            success=True,
            message="Users retrieved successfully",
            data=user_profiles,
            total=total,
            page=page,
            per_page=per_page,
            has_next=has_next,
            has_prev=has_prev,
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve users",
        )


@router.get("/{user_id}", response_model=UserResponse, tags=["User Management"])
async def get_user_by_id(
    user_id: uuid.UUID,
    current_user: User = Depends(current_superuser),
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    """
    Get user by ID (Admin only).
    
    This endpoint allows administrators to retrieve a specific user's
    information by their ID.
    
    Args:
        user_id: User ID to retrieve
        current_user: Current authenticated user (must be superuser)
        db: Database session
        
    Returns:
        UserResponse: User information
    """
    try:
        # Find user by ID
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        
        # Get user roles
        roles = [user_role.role.name for user_role in user.roles if user_role.role]
        
        user_profile = UserProfile(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            full_name=user.full_name,
            phone=user.phone,
            bio=user.bio,
            profile_picture_url=user.profile_picture_url,
            is_active=user.is_active,
            is_verified=user.is_verified,
            created_at=user.created_at,
            updated_at=user.updated_at,
            roles=roles,
        )
        
        return UserResponse(
            success=True,
            message="User retrieved successfully",
            data=user_profile,
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user",
        )


@router.delete("/{user_id}", tags=["User Management"])
async def delete_user(
    user_id: uuid.UUID,
    current_user: User = Depends(current_superuser),
    user_manager: UserManager = Depends(get_user_manager),
) -> Dict[str, Any]:
    """
    Delete user by ID (Admin only).
    
    This endpoint allows administrators to delete a user account.
    The user cannot delete their own account.
    
    Args:
        user_id: User ID to delete
        current_user: Current authenticated user (must be superuser)
        user_manager: User manager dependency
        
    Returns:
        Dict[str, Any]: Deletion confirmation
    """
    try:
        # Prevent self-deletion
        if user_id == current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot delete your own account",
            )
        
        # Find user by ID
        user = await user_manager.get(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        
        # Delete user
        await user_manager.delete(user)
        
        return {
            "success": True,
            "message": "User deleted successfully",
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete user",
        )


@router.patch("/{user_id}/activate", tags=["User Management"])
async def activate_user(
    user_id: uuid.UUID,
    current_user: User = Depends(current_superuser),
    user_manager: UserManager = Depends(get_user_manager),
) -> Dict[str, Any]:
    """
    Activate user account (Admin only).
    
    This endpoint allows administrators to activate a user account.
    
    Args:
        user_id: User ID to activate
        current_user: Current authenticated user (must be superuser)
        user_manager: User manager dependency
        
    Returns:
        Dict[str, Any]: Activation confirmation
    """
    try:
        # Find user by ID
        user = await user_manager.get(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        
        # Activate user
        await user_manager.update(user, {"is_active": True})
        
        return {
            "success": True,
            "message": "User activated successfully",
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to activate user",
        )


@router.patch("/{user_id}/deactivate", tags=["User Management"])
async def deactivate_user(
    user_id: uuid.UUID,
    current_user: User = Depends(current_superuser),
    user_manager: UserManager = Depends(get_user_manager),
) -> Dict[str, Any]:
    """
    Deactivate user account (Admin only).
    
    This endpoint allows administrators to deactivate a user account.
    The user cannot deactivate their own account.
    
    Args:
        user_id: User ID to deactivate
        current_user: Current authenticated user (must be superuser)
        user_manager: User manager dependency
        
    Returns:
        Dict[str, Any]: Deactivation confirmation
    """
    try:
        # Prevent self-deactivation
        if user_id == current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot deactivate your own account",
            )
        
        # Find user by ID
        user = await user_manager.get(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        
        # Deactivate user
        await user_manager.update(user, {"is_active": False})
        
        return {
            "success": True,
            "message": "User deactivated successfully",
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to deactivate user",
        )

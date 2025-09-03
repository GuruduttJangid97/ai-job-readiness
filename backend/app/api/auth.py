"""
Authentication API endpoints for AI Job Readiness Platform

This module provides authentication endpoints including registration, login,
logout, email verification, and password reset functionality using FastAPI-Users.

Author: AI Job Readiness Team
Version: 1.0.0
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any, Dict

from app.core.users import (
    fastapi_users,
    current_active_user,
    current_verified_user,
    get_user_manager,
    UserManager,
)
from app.db.database import get_db
from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserRead,
    UserLoginResponse,
    PasswordResetRequest,
    PasswordResetConfirm,
)
from app.core.security import (
    generate_password_reset_token,
    verify_password_reset_token,
    get_password_hash,
)

# Create router for authentication endpoints
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
    responses={
        404: {"description": "Not found"},
        422: {"description": "Validation error"},
        500: {"description": "Internal server error"},
    },
)

# Include FastAPI-Users authentication routes
from app.core.users import auth_backend

router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/jwt", tags=["Authentication"]
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="",
    tags=["Authentication"],
)

router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="",
    tags=["Authentication"],
)

router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="",
    tags=["Authentication"],
)

router.include_router(
    fastapi_users.get_users_router(UserRead, UserRead),
    prefix="/users",
    tags=["Users"],
)


@router.post("/login", response_model=UserLoginResponse, tags=["Authentication"])
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_manager: UserManager = Depends(get_user_manager),
) -> UserLoginResponse:
    """
    Authenticate user and return access token.
    
    This endpoint authenticates a user with email and password,
    returning a JWT access token and user information.
    
    Args:
        form_data: OAuth2 password request form with username (email) and password
        user_manager: User manager dependency
        
    Returns:
        UserLoginResponse: Authentication response with token and user data
        
    Raises:
        HTTPException: If authentication fails
    """
    try:
        # Authenticate user
        user = await user_manager.authenticate(form_data)
        
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create access token
        access_token = await user_manager.create_access_token(user)
        
        # Get user roles
        roles = [user_role.role.name for user_role in user.roles if user_role.role]
        
        return UserLoginResponse(
            success=True,
            message="Login successful",
            access_token=access_token,
            token_type="bearer",
            expires_in=30 * 60,  # 30 minutes
            user={
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "full_name": user.full_name,
                "phone": user.phone,
                "bio": user.bio,
                "profile_picture_url": user.profile_picture_url,
                "is_active": user.is_active,
                "is_verified": user.is_verified,
                "created_at": user.created_at,
                "updated_at": user.updated_at,
                "roles": roles,
            }
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed",
        )


@router.post("/logout", tags=["Authentication"])
async def logout(
    current_user: User = Depends(current_active_user),
) -> Dict[str, Any]:
    """
    Logout current user.
    
    This endpoint handles user logout. In JWT-based authentication,
    logout is typically handled client-side by removing the token.
    This endpoint provides a confirmation response.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        Dict[str, Any]: Logout confirmation response
    """
    return {
        "success": True,
        "message": "Logout successful",
        "user_id": str(current_user.id),
    }


@router.post("/request-password-reset", tags=["Authentication"])
async def request_password_reset(
    request: PasswordResetRequest,
    user_manager: UserManager = Depends(get_user_manager),
) -> Dict[str, Any]:
    """
    Request password reset for a user.
    
    This endpoint initiates the password reset process by sending
    a reset token to the user's email address.
    
    Args:
        request: Password reset request with email
        user_manager: User manager dependency
        
    Returns:
        Dict[str, Any]: Password reset request confirmation
    """
    try:
        # Find user by email
        user = await user_manager.get_by_email(request.email)
        
        if not user:
            # Don't reveal if email exists or not for security
            return {
                "success": True,
                "message": "If the email exists, a password reset link has been sent",
            }
        
        # Generate reset token
        reset_token = generate_password_reset_token(user.email)
        
        # In a real application, you would send this token via email
        # For now, we'll just log it (remove this in production)
        print(f"Password reset token for {user.email}: {reset_token}")
        
        return {
            "success": True,
            "message": "If the email exists, a password reset link has been sent",
            "reset_token": reset_token,  # Remove this in production
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process password reset request",
        )


@router.post("/confirm-password-reset", tags=["Authentication"])
async def confirm_password_reset(
    request: PasswordResetConfirm,
    user_manager: UserManager = Depends(get_user_manager),
) -> Dict[str, Any]:
    """
    Confirm password reset with token and new password.
    
    This endpoint completes the password reset process by verifying
    the reset token and updating the user's password.
    
    Args:
        request: Password reset confirmation with token and new password
        user_manager: User manager dependency
        
    Returns:
        Dict[str, Any]: Password reset confirmation response
    """
    try:
        # Verify reset token
        email = verify_password_reset_token(request.token)
        
        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid or expired reset token",
            )
        
        # Find user by email
        user = await user_manager.get_by_email(email)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        
        # Update password
        hashed_password = get_password_hash(request.new_password)
        await user_manager.update(user, {"hashed_password": hashed_password})
        
        return {
            "success": True,
            "message": "Password has been reset successfully",
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to reset password",
        )


@router.get("/me", response_model=UserRead, tags=["Authentication"])
async def get_current_user(
    current_user: User = Depends(current_active_user),
) -> UserRead:
    """
    Get current authenticated user information.
    
    This endpoint returns the profile information of the currently
    authenticated user.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        UserRead: Current user information
    """
    return current_user


@router.get("/verify-email", tags=["Authentication"])
async def verify_email(
    token: str,
    user_manager: UserManager = Depends(get_user_manager),
) -> Dict[str, Any]:
    """
    Verify user email with verification token.
    
    This endpoint verifies a user's email address using the
    verification token sent to their email.
    
    Args:
        token: Email verification token
        user_manager: User manager dependency
        
    Returns:
        Dict[str, Any]: Email verification response
    """
    try:
        # Verify token and get user
        user = await user_manager.verify(token)
        
        return {
            "success": True,
            "message": "Email verified successfully",
            "user_id": str(user.id),
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired verification token",
        )


@router.post("/resend-verification", tags=["Authentication"])
async def resend_verification(
    email: str,
    user_manager: UserManager = Depends(get_user_manager),
) -> Dict[str, Any]:
    """
    Resend email verification token.
    
    This endpoint resends the email verification token to the user's
    email address.
    
    Args:
        email: User's email address
        user_manager: User manager dependency
        
    Returns:
        Dict[str, Any]: Resend verification response
    """
    try:
        # Find user by email
        user = await user_manager.get_by_email(email)
        
        if not user:
            # Don't reveal if email exists or not for security
            return {
                "success": True,
                "message": "If the email exists and is not verified, a verification link has been sent",
            }
        
        if user.is_verified:
            return {
                "success": True,
                "message": "Email is already verified",
            }
        
        # Request verification
        await user_manager.request_verify(user)
        
        return {
            "success": True,
            "message": "If the email exists and is not verified, a verification link has been sent",
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to resend verification email",
        )

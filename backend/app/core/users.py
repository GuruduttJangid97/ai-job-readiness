"""
FastAPI-Users configuration for AI Job Readiness Platform

This module configures FastAPI-Users with database adapter, user manager,
and authentication settings for the AI Job Readiness platform.

Author: AI Job Readiness Team
Version: 1.0.0
"""

import uuid
from typing import Optional
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import get_password_hash, verify_password
from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserRead


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    """
    User manager for FastAPI-Users.
    
    This class handles user creation, authentication, and management
    operations for the AI Job Readiness platform.
    """
    
    reset_password_token_secret = settings.reset_password_token_secret
    verification_token_secret = settings.verification_token_secret
    
    async def on_after_register(self, user: User, request: Optional[Request] = None):
        """
        Handle post-registration actions.
        
        Args:
            user: The newly registered user
            request: The HTTP request (optional)
        """
        print(f"User {user.id} has registered.")
    
    async def on_after_login(
        self,
        user: User,
        request: Optional[Request] = None,
        response: Optional[dict] = None,
    ):
        """
        Handle post-login actions.
        
        Args:
            user: The logged-in user
            request: The HTTP request (optional)
            response: The HTTP response (optional)
        """
        print(f"User {user.id} has logged in.")
    
    async def on_after_update(
        self,
        user: User,
        update_dict: dict,
        request: Optional[Request] = None,
    ):
        """
        Handle post-update actions.
        
        Args:
            user: The updated user
            update_dict: Dictionary of updated fields
            request: The HTTP request (optional)
        """
        print(f"User {user.id} has been updated.")
    
    async def on_after_request_verify(
        self,
        user: User,
        token: str,
        request: Optional[Request] = None,
    ):
        """
        Handle post-verification request actions.
        
        Args:
            user: The user requesting verification
            token: The verification token
            request: The HTTP request (optional)
        """
        print(f"Verification requested for user {user.id}. Verification token: {token}")
    
    async def on_after_verify(
        self,
        user: User,
        request: Optional[Request] = None,
    ):
        """
        Handle post-verification actions.
        
        Args:
            user: The verified user
            request: The HTTP request (optional)
        """
        print(f"User {user.id} has been verified.")
    
    async def on_after_forgot_password(
        self,
        user: User,
        token: str,
        request: Optional[Request] = None,
    ):
        """
        Handle post-forgot password actions.
        
        Args:
            user: The user who forgot their password
            token: The password reset token
            request: The HTTP request (optional)
        """
        print(f"User {user.id} has forgot their password. Reset token: {token}")
    
    async def on_after_reset_password(
        self,
        user: User,
        request: Optional[Request] = None,
    ):
        """
        Handle post-password reset actions.
        
        Args:
            user: The user who reset their password
            request: The HTTP request (optional)
        """
        print(f"User {user.id} has reset their password.")
    
    async def on_after_delete(
        self,
        user: User,
        request: Optional[Request] = None,
    ):
        """
        Handle post-deletion actions.
        
        Args:
            user: The deleted user
            request: The HTTP request (optional)
        """
        print(f"User {user.id} has been deleted.")
    
    async def validate_password(
        self,
        password: str,
        user: User,
    ) -> None:
        """
        Validate password strength.
        
        Args:
            password: The password to validate
            user: The user object
            
        Raises:
            InvalidPasswordException: If password doesn't meet requirements
        """
        if len(password) < 8:
            from fastapi_users.exceptions import InvalidPasswordException
            raise InvalidPasswordException(
                reason="Password should be at least 8 characters"
            )
        if not any(c.isupper() for c in password):
            from fastapi_users.exceptions import InvalidPasswordException
            raise InvalidPasswordException(
                reason="Password should contain at least one uppercase letter"
            )
        if not any(c.islower() for c in password):
            from fastapi_users.exceptions import InvalidPasswordException
            raise InvalidPasswordException(
                reason="Password should contain at least one lowercase letter"
            )
        if not any(c.isdigit() for c in password):
            from fastapi_users.exceptions import InvalidPasswordException
            raise InvalidPasswordException(
                reason="Password should contain at least one digit"
            )


async def get_user_db(session: AsyncSession = Depends(get_db)):
    """
    Get user database adapter.
    
    Args:
        session: Database session
        
    Yields:
        SQLAlchemyUserDatabase: User database adapter
    """
    yield SQLAlchemyUserDatabase(session, User)


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    """
    Get user manager.
    
    Args:
        user_db: User database adapter
        
    Yields:
        UserManager: User manager instance
    """
    yield UserManager(user_db)


# Configure authentication backend
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    """
    Get JWT authentication strategy.
    
    Returns:
        JWTStrategy: JWT authentication strategy
    """
    return JWTStrategy(
        secret=settings.users_secret,
        lifetime_seconds=settings.access_token_expire_minutes * 60,
    )


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

# Create FastAPI-Users instance
fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

# Get current user dependencies
current_active_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
current_verified_user = fastapi_users.current_user(active=True, verified=True)

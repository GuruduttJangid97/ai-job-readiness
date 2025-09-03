"""
Security utilities for AI Job Readiness Platform

This module provides security-related utilities including password hashing,
token generation, and authentication helpers.

Author: AI Job Readiness Team
Version: 1.0.0
"""

import secrets
from datetime import datetime, timedelta
from typing import Any, Union, Optional
from jose import jwt
from passlib.context import CryptContext
from .config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token.
    
    Args:
        subject: The subject (usually user ID) to encode in the token
        expires_delta: Optional expiration time delta
        
    Returns:
        str: Encoded JWT token
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.access_token_expire_minutes
        )
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def verify_token(token: str) -> Optional[str]:
    """
    Verify and decode a JWT token.
    
    Args:
        token: The JWT token to verify
        
    Returns:
        Optional[str]: The subject (user ID) if token is valid, None otherwise
    """
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        return payload.get("sub")
    except jwt.JWTError:
        return None


def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Args:
        password: Plain text password
        
    Returns:
        str: Hashed password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.
    
    Args:
        plain_password: Plain text password
        hashed_password: Hashed password to verify against
        
    Returns:
        bool: True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def generate_password_reset_token(email: str) -> str:
    """
    Generate a password reset token.
    
    Args:
        email: User's email address
        
    Returns:
        str: Password reset token
    """
    delta = timedelta(hours=settings.reset_password_token_expire_hours)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email}, 
        settings.reset_password_token_secret, 
        algorithm=settings.algorithm
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    """
    Verify a password reset token.
    
    Args:
        token: Password reset token
        
    Returns:
        Optional[str]: Email if token is valid, None otherwise
    """
    try:
        decoded_token = jwt.decode(
            token, 
            settings.reset_password_token_secret, 
            algorithms=[settings.algorithm]
        )
        return decoded_token.get("sub")
    except jwt.JWTError:
        return None


def generate_verification_token(email: str) -> str:
    """
    Generate an email verification token.
    
    Args:
        email: User's email address
        
    Returns:
        str: Email verification token
    """
    delta = timedelta(hours=settings.verification_token_expire_hours)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email}, 
        settings.verification_token_secret, 
        algorithm=settings.algorithm
    )
    return encoded_jwt


def verify_verification_token(token: str) -> Optional[str]:
    """
    Verify an email verification token.
    
    Args:
        token: Email verification token
        
    Returns:
        Optional[str]: Email if token is valid, None otherwise
    """
    try:
        decoded_token = jwt.decode(
            token, 
            settings.verification_token_secret, 
            algorithms=[settings.algorithm]
        )
        return decoded_token.get("sub")
    except jwt.JWTError:
        return None


def generate_random_string(length: int = 32) -> str:
    """
    Generate a random string of specified length.
    
    Args:
        length: Length of the random string
        
    Returns:
        str: Random string
    """
    return secrets.token_urlsafe(length)

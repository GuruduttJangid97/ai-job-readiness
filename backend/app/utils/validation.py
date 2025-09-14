"""
Custom validation utilities for AI Job Readiness Platform

This module provides custom validation functions that are used
throughout the application for data validation and sanitization.

Author: AI Job Readiness Team
Version: 1.0.0
"""

import re
import uuid
from datetime import datetime, date
from typing import Any, Optional, List, Dict, Union
from pydantic import ValidationError as PydanticValidationError

from app.core.config import settings


def validate_password_strength(password: str) -> tuple[bool, List[str]]:
    """
    Validate password strength based on configured requirements.
    
    Args:
        password: Password to validate
        
    Returns:
        tuple[bool, List[str]]: (is_valid, error_messages)
    """
    errors = []
    
    if not password:
        errors.append("Password is required")
        return False, errors
    
    # Check minimum length
    if len(password) < settings.security.min_password_length:
        errors.append(f"Password must be at least {settings.security.min_password_length} characters long")
    
    # Check for uppercase letters
    if settings.security.require_uppercase and not any(c.isupper() for c in password):
        errors.append("Password must contain at least one uppercase letter")
    
    # Check for lowercase letters
    if settings.security.require_lowercase and not any(c.islower() for c in password):
        errors.append("Password must contain at least one lowercase letter")
    
    # Check for digits
    if settings.security.require_digits and not any(c.isdigit() for c in password):
        errors.append("Password must contain at least one digit")
    
    # Check for special characters
    if settings.security.require_special_chars and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append("Password must contain at least one special character")
    
    return len(errors) == 0, errors


def validate_json_data(data: Any, schema: Optional[Dict[str, Any]] = None) -> tuple[bool, Optional[str]]:
    """
    Validate JSON data structure.
    
    Args:
        data: Data to validate
        schema: Optional schema to validate against
        
    Returns:
        tuple[bool, Optional[str]]: (is_valid, error_message)
    """
    try:
        # Basic JSON structure validation
        if not isinstance(data, (dict, list, str, int, float, bool, type(None))):
            return False, "Invalid JSON data type"
        
        # If schema is provided, perform basic validation
        if schema and isinstance(data, dict):
            required_fields = schema.get("required", [])
            for field in required_fields:
                if field not in data:
                    return False, f"Missing required field: {field}"
        
        return True, None
        
    except Exception as e:
        return False, f"JSON validation error: {str(e)}"


def validate_uuid(uuid_string: str) -> bool:
    """
    Validate UUID string format.
    
    Args:
        uuid_string: String to validate as UUID
        
    Returns:
        bool: True if valid UUID, False otherwise
    """
    if not uuid_string:
        return False
    
    try:
        uuid.UUID(uuid_string)
        return True
    except ValueError:
        return False


def validate_date_range(start_date: Union[str, datetime, date], 
                       end_date: Union[str, datetime, date]) -> tuple[bool, Optional[str]]:
    """
    Validate that start_date is before end_date.
    
    Args:
        start_date: Start date
        end_date: End date
        
    Returns:
        tuple[bool, Optional[str]]: (is_valid, error_message)
    """
    try:
        # Convert strings to datetime if needed
        if isinstance(start_date, str):
            start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        elif isinstance(start_date, date) and not isinstance(start_date, datetime):
            start_date = datetime.combine(start_date, datetime.min.time())
        
        if isinstance(end_date, str):
            end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        elif isinstance(end_date, date) and not isinstance(end_date, datetime):
            end_date = datetime.combine(end_date, datetime.min.time())
        
        if start_date >= end_date:
            return False, "Start date must be before end date"
        
        return True, None
        
    except (ValueError, TypeError) as e:
        return False, f"Invalid date format: {str(e)}"


def validate_file_upload(file_data: Dict[str, Any]) -> tuple[bool, List[str]]:
    """
    Validate file upload data.
    
    Args:
        file_data: File upload data dictionary
        
    Returns:
        tuple[bool, List[str]]: (is_valid, error_messages)
    """
    errors = []
    
    # Check required fields
    required_fields = ["filename", "content_type", "size"]
    for field in required_fields:
        if field not in file_data:
            errors.append(f"Missing required field: {field}")
    
    if errors:
        return False, errors
    
    # Validate filename
    if not file_data.get("filename"):
        errors.append("Filename cannot be empty")
    
    # Validate content type
    if not file_data.get("content_type"):
        errors.append("Content type cannot be empty")
    
    # Validate file size
    file_size = file_data.get("size", 0)
    if not isinstance(file_size, int) or file_size <= 0:
        errors.append("Invalid file size")
    elif file_size > settings.file.max_file_size:
        max_size_mb = settings.file.max_file_size // (1024 * 1024)
        errors.append(f"File size exceeds maximum limit of {max_size_mb}MB")
    
    return len(errors) == 0, errors


def validate_pagination_params(page: int, per_page: int, max_per_page: int = 100) -> tuple[bool, List[str]]:
    """
    Validate pagination parameters.
    
    Args:
        page: Page number
        per_page: Items per page
        max_per_page: Maximum items per page allowed
        
    Returns:
        tuple[bool, List[str]]: (is_valid, error_messages)
    """
    errors = []
    
    if not isinstance(page, int) or page < 1:
        errors.append("Page must be a positive integer")
    
    if not isinstance(per_page, int) or per_page < 1:
        errors.append("Per page must be a positive integer")
    elif per_page > max_per_page:
        errors.append(f"Per page cannot exceed {max_per_page}")
    
    return len(errors) == 0, errors


def validate_search_query(query: str, min_length: int = 2, max_length: int = 100) -> tuple[bool, Optional[str]]:
    """
    Validate search query parameters.
    
    Args:
        query: Search query string
        min_length: Minimum query length
        max_length: Maximum query length
        
    Returns:
        tuple[bool, Optional[str]]: (is_valid, error_message)
    """
    if not query:
        return True, None  # Empty query is allowed
    
    if len(query) < min_length:
        return False, f"Search query must be at least {min_length} characters long"
    
    if len(query) > max_length:
        return False, f"Search query cannot exceed {max_length} characters"
    
    # Check for potentially malicious patterns
    malicious_patterns = [
        r'<script.*?>.*?</script>',
        r'javascript:',
        r'data:',
        r'vbscript:',
    ]
    
    for pattern in malicious_patterns:
        if re.search(pattern, query, re.IGNORECASE):
            return False, "Search query contains potentially malicious content"
    
    return True, None


def validate_email_domain(email: str, allowed_domains: Optional[List[str]] = None) -> bool:
    """
    Validate email domain against allowed domains.
    
    Args:
        email: Email address to validate
        allowed_domains: List of allowed domains (if None, all domains allowed)
        
    Returns:
        bool: True if domain is allowed, False otherwise
    """
    if not email or not allowed_domains:
        return True
    
    try:
        domain = email.split('@')[1].lower()
        return domain in [d.lower() for d in allowed_domains]
    except IndexError:
        return False


def validate_phone_format(phone: str, country_code: str = "US") -> tuple[bool, Optional[str]]:
    """
    Validate phone number format.
    
    Args:
        phone: Phone number to validate
        country_code: Country code for validation
        
    Returns:
        tuple[bool, Optional[str]]: (is_valid, error_message)
    """
    if not phone:
        return True, None  # Empty phone is allowed
    
    # Basic phone number validation
    phone_pattern = r'^[\+]?[1-9][\d]{0,15}$'
    if not re.match(phone_pattern, phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')):
        return False, "Invalid phone number format"
    
    return True, None


def validate_score_range(score: float, min_score: float = 0.0, max_score: float = 100.0) -> tuple[bool, Optional[str]]:
    """
    Validate score is within valid range.
    
    Args:
        score: Score to validate
        min_score: Minimum valid score
        max_score: Maximum valid score
        
    Returns:
        tuple[bool, Optional[str]]: (is_valid, error_message)
    """
    if not isinstance(score, (int, float)):
        return False, "Score must be a number"
    
    if score < min_score or score > max_score:
        return False, f"Score must be between {min_score} and {max_score}"
    
    return True, None


def validate_analysis_type(analysis_type: str) -> tuple[bool, Optional[str]]:
    """
    Validate analysis type is one of the allowed types.
    
    Args:
        analysis_type: Analysis type to validate
        
    Returns:
        tuple[bool, Optional[str]]: (is_valid, error_message)
    """
    allowed_types = ["overall", "job_match", "skill_analysis", "experience_analysis", "education_analysis"]
    
    if analysis_type not in allowed_types:
        return False, f"Invalid analysis type. Must be one of: {', '.join(allowed_types)}"
    
    return True, None


def sanitize_input(text: str, max_length: Optional[int] = None) -> str:
    """
    Sanitize user input by removing potentially harmful content.
    
    Args:
        text: Text to sanitize
        max_length: Maximum length to truncate to
        
    Returns:
        str: Sanitized text
    """
    if not text:
        return ""
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove script tags and javascript
    text = re.sub(r'<script.*?>.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'javascript:', '', text, flags=re.IGNORECASE)
    
    # Remove SQL injection patterns
    sql_patterns = [
        r'(\b(union|select|insert|update|delete|drop|create|alter)\b)',
        r'(\b(or|and)\s+\d+\s*=\s*\d+)',
        r'(\'|\"|;|--|\/\*|\*\/)',
    ]
    
    for pattern in sql_patterns:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text.strip())
    
    # Truncate if max_length is specified
    if max_length and len(text) > max_length:
        text = text[:max_length].rstrip()
    
    return text

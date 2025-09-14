"""
Utility modules for AI Job Readiness Platform

This package contains utility functions and classes that are used
across the application to reduce code duplication and improve maintainability.

Modules:
- file_utils: File handling and validation utilities
- text_utils: Text processing and validation utilities
- validation: Custom validation functions
- response: Standardized response utilities
- exceptions: Custom exception classes
- decorators: Common decorators for API endpoints

Author: AI Job Readiness Team
Version: 1.0.0
"""

from .file_utils import (
    validate_file_extension,
    validate_file_size,
    generate_unique_filename,
    get_file_extension,
    get_file_size_mb,
)
from .text_utils import (
    clean_text,
    extract_keywords,
    validate_email,
    validate_phone,
    validate_url,
    slugify,
)
from .validation import (
    validate_password_strength,
    validate_json_data,
    validate_uuid,
    validate_date_range,
)
from .response import (
    create_success_response,
    create_error_response,
    create_paginated_response,
    ResponseModel,
)
from .exceptions import (
    AIJobReadinessException,
    ValidationError,
    FileUploadError,
    DatabaseError,
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    ConflictError,
)
from .decorators import (
    handle_errors,
    validate_request,
    require_permissions,
    rate_limit,
)

__all__ = [
    # File utilities
    "validate_file_extension",
    "validate_file_size", 
    "generate_unique_filename",
    "get_file_extension",
    "get_file_size_mb",
    
    # Text utilities
    "clean_text",
    "extract_keywords",
    "validate_email",
    "validate_phone",
    "validate_url",
    "slugify",
    
    # Validation utilities
    "validate_password_strength",
    "validate_json_data",
    "validate_uuid",
    "validate_date_range",
    
    # Response utilities
    "create_success_response",
    "create_error_response",
    "create_paginated_response",
    "ResponseModel",
    
    # Exception classes
    "AIJobReadinessException",
    "ValidationError",
    "FileUploadError",
    "DatabaseError",
    "AuthenticationError",
    "AuthorizationError",
    "NotFoundError",
    "ConflictError",
    
    # Decorators
    "handle_errors",
    "validate_request",
    "require_permissions",
    "rate_limit",
]

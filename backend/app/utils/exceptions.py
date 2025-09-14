"""
Custom exception classes for AI Job Readiness Platform

This module defines custom exception classes that provide
better error handling and more specific error messages.

Author: AI Job Readiness Team
Version: 1.0.0
"""

from typing import Optional, List, Dict, Any


class AIJobReadinessException(Exception):
    """Base exception class for AI Job Readiness Platform."""
    
    def __init__(
        self,
        message: str = "An error occurred",
        details: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = None
    ):
        self.message = message
        self.details = details or {}
        self.error_code = error_code
        super().__init__(self.message)


class ValidationError(AIJobReadinessException):
    """Exception raised for validation errors."""
    
    def __init__(
        self,
        message: str = "Validation failed",
        field_errors: Optional[Dict[str, List[str]]] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.field_errors = field_errors or {}
        super().__init__(message, details, "VALIDATION_ERROR")


class FileUploadError(AIJobReadinessException):
    """Exception raised for file upload errors."""
    
    def __init__(
        self,
        message: str = "File upload failed",
        filename: Optional[str] = None,
        file_size: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.filename = filename
        self.file_size = file_size
        super().__init__(message, details, "FILE_UPLOAD_ERROR")


class DatabaseError(AIJobReadinessException):
    """Exception raised for database operation errors."""
    
    def __init__(
        self,
        message: str = "Database operation failed",
        operation: Optional[str] = None,
        table: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.operation = operation
        self.table = table
        super().__init__(message, details, "DATABASE_ERROR")


class AuthenticationError(AIJobReadinessException):
    """Exception raised for authentication errors."""
    
    def __init__(
        self,
        message: str = "Authentication failed",
        user_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.user_id = user_id
        super().__init__(message, details, "AUTHENTICATION_ERROR")


class AuthorizationError(AIJobReadinessException):
    """Exception raised for authorization errors."""
    
    def __init__(
        self,
        message: str = "Access denied",
        user_id: Optional[str] = None,
        required_permission: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.user_id = user_id
        self.required_permission = required_permission
        super().__init__(message, details, "AUTHORIZATION_ERROR")


class NotFoundError(AIJobReadinessException):
    """Exception raised when a resource is not found."""
    
    def __init__(
        self,
        message: str = "Resource not found",
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.resource_type = resource_type
        self.resource_id = resource_id
        super().__init__(message, details, "NOT_FOUND")


class ConflictError(AIJobReadinessException):
    """Exception raised when there's a resource conflict."""
    
    def __init__(
        self,
        message: str = "Resource conflict",
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        conflicting_field: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.resource_type = resource_type
        self.resource_id = resource_id
        self.conflicting_field = conflicting_field
        super().__init__(message, details, "CONFLICT")


class RateLimitError(AIJobReadinessException):
    """Exception raised when rate limit is exceeded."""
    
    def __init__(
        self,
        message: str = "Rate limit exceeded",
        limit: Optional[int] = None,
        window: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.limit = limit
        self.window = window
        super().__init__(message, details, "RATE_LIMIT_EXCEEDED")


class ExternalServiceError(AIJobReadinessException):
    """Exception raised for external service errors."""
    
    def __init__(
        self,
        message: str = "External service error",
        service_name: Optional[str] = None,
        status_code: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.service_name = service_name
        self.status_code = status_code
        super().__init__(message, details, "EXTERNAL_SERVICE_ERROR")


class AIAnalysisError(AIJobReadinessException):
    """Exception raised for AI analysis errors."""
    
    def __init__(
        self,
        message: str = "AI analysis failed",
        analysis_type: Optional[str] = None,
        model_version: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.analysis_type = analysis_type
        self.model_version = model_version
        super().__init__(message, details, "AI_ANALYSIS_ERROR")


class ConfigurationError(AIJobReadinessException):
    """Exception raised for configuration errors."""
    
    def __init__(
        self,
        message: str = "Configuration error",
        setting_name: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.setting_name = setting_name
        super().__init__(message, details, "CONFIGURATION_ERROR")


class BusinessLogicError(AIJobReadinessException):
    """Exception raised for business logic violations."""
    
    def __init__(
        self,
        message: str = "Business logic violation",
        rule_name: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.rule_name = rule_name
        super().__init__(message, details, "BUSINESS_LOGIC_ERROR")


class DataIntegrityError(AIJobReadinessException):
    """Exception raised for data integrity violations."""
    
    def __init__(
        self,
        message: str = "Data integrity violation",
        constraint_name: Optional[str] = None,
        table_name: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.constraint_name = constraint_name
        self.table_name = table_name
        super().__init__(message, details, "DATA_INTEGRITY_ERROR")


class SerializationError(AIJobReadinessException):
    """Exception raised for data serialization/deserialization errors."""
    
    def __init__(
        self,
        message: str = "Serialization error",
        data_type: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.data_type = data_type
        super().__init__(message, details, "SERIALIZATION_ERROR")


class CacheError(AIJobReadinessException):
    """Exception raised for cache operation errors."""
    
    def __init__(
        self,
        message: str = "Cache operation failed",
        operation: Optional[str] = None,
        key: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.operation = operation
        self.key = key
        super().__init__(message, details, "CACHE_ERROR")


class EmailError(AIJobReadinessException):
    """Exception raised for email operation errors."""
    
    def __init__(
        self,
        message: str = "Email operation failed",
        recipient: Optional[str] = None,
        template: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.recipient = recipient
        self.template = template
        super().__init__(message, details, "EMAIL_ERROR")


class NotificationError(AIJobReadinessException):
    """Exception raised for notification errors."""
    
    def __init__(
        self,
        message: str = "Notification failed",
        notification_type: Optional[str] = None,
        user_id: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.notification_type = notification_type
        self.user_id = user_id
        super().__init__(message, details, "NOTIFICATION_ERROR")

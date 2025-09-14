"""
Common decorators for API endpoints in AI Job Readiness Platform

This module provides decorators that can be used to add common
functionality to API endpoints such as error handling, validation,
and rate limiting.

Author: AI Job Readiness Team
Version: 1.0.0
"""

import time
import functools
from typing import Callable, Any, Dict, List, Optional, Union
from fastapi import HTTPException, status, Request
from fastapi.responses import JSONResponse

from .exceptions import (
    AIJobReadinessException,
    ValidationError,
    RateLimitError,
    AuthenticationError,
    AuthorizationError
)
from .response import create_error_response


def handle_errors(
    default_message: str = "An error occurred",
    log_errors: bool = True
):
    """
    Decorator to handle common exceptions in API endpoints.
    
    Args:
        default_message: Default error message for unhandled exceptions
        log_errors: Whether to log errors
        
    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except ValidationError as e:
                if log_errors:
                    print(f"Validation error in {func.__name__}: {e.message}")
                return create_error_response(
                    message=e.message,
                    errors=list(e.field_errors.values()) if e.field_errors else None,
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
            except AuthenticationError as e:
                if log_errors:
                    print(f"Authentication error in {func.__name__}: {e.message}")
                return create_error_response(
                    message=e.message,
                    status_code=status.HTTP_401_UNAUTHORIZED
                )
            except AuthorizationError as e:
                if log_errors:
                    print(f"Authorization error in {func.__name__}: {e.message}")
                return create_error_response(
                    message=e.message,
                    status_code=status.HTTP_403_FORBIDDEN
                )
            except RateLimitError as e:
                if log_errors:
                    print(f"Rate limit error in {func.__name__}: {e.message}")
                return create_error_response(
                    message=e.message,
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS
                )
            except AIJobReadinessException as e:
                if log_errors:
                    print(f"Application error in {func.__name__}: {e.message}")
                return create_error_response(
                    message=e.message,
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            except HTTPException as e:
                if log_errors:
                    print(f"HTTP error in {func.__name__}: {e.detail}")
                return create_error_response(
                    message=str(e.detail),
                    status_code=e.status_code
                )
            except Exception as e:
                if log_errors:
                    print(f"Unexpected error in {func.__name__}: {str(e)}")
                return create_error_response(
                    message=default_message,
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return wrapper
    return decorator


def validate_request(
    required_fields: Optional[List[str]] = None,
    allowed_fields: Optional[List[str]] = None,
    validate_types: Optional[Dict[str, type]] = None
):
    """
    Decorator to validate request data.
    
    Args:
        required_fields: List of required field names
        allowed_fields: List of allowed field names
        validate_types: Dictionary mapping field names to expected types
        
    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract request data from kwargs
            request_data = None
            for key, value in kwargs.items():
                if hasattr(value, '__dict__') and not key.startswith('_'):
                    request_data = value
                    break
            
            if request_data and hasattr(request_data, '__dict__'):
                data_dict = request_data.__dict__ if hasattr(request_data, '__dict__') else {}
                
                # Check required fields
                if required_fields:
                    missing_fields = [field for field in required_fields if field not in data_dict]
                    if missing_fields:
                        raise ValidationError(
                            message="Missing required fields",
                            field_errors={field: ["This field is required"] for field in missing_fields}
                        )
                
                # Check allowed fields
                if allowed_fields:
                    invalid_fields = [field for field in data_dict.keys() if field not in allowed_fields]
                    if invalid_fields:
                        raise ValidationError(
                            message="Invalid fields provided",
                            field_errors={field: ["This field is not allowed"] for field in invalid_fields}
                        )
                
                # Validate field types
                if validate_types:
                    type_errors = {}
                    for field, expected_type in validate_types.items():
                        if field in data_dict and data_dict[field] is not None:
                            if not isinstance(data_dict[field], expected_type):
                                type_errors[field] = [f"Expected {expected_type.__name__}, got {type(data_dict[field]).__name__}"]
                    
                    if type_errors:
                        raise ValidationError(
                            message="Invalid field types",
                            field_errors=type_errors
                        )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def require_permissions(*permissions: str):
    """
    Decorator to require specific permissions for an endpoint.
    
    Args:
        *permissions: Required permissions
        
    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract current user from kwargs
            current_user = None
            for key, value in kwargs.items():
                if key == 'current_user' and hasattr(value, 'get_role_names'):
                    current_user = value
                    break
            
            if not current_user:
                raise AuthenticationError("Authentication required")
            
            # Check if user has required permissions
            user_permissions = []
            for role in current_user.roles:
                if hasattr(role, 'role') and role.role:
                    user_permissions.extend(role.role.get_permissions_list())
            
            missing_permissions = [perm for perm in permissions if perm not in user_permissions]
            if missing_permissions:
                raise AuthorizationError(
                    message="Insufficient permissions",
                    required_permission=missing_permissions[0]
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def rate_limit(
    max_requests: int = 100,
    window_seconds: int = 3600,
    key_func: Optional[Callable] = None
):
    """
    Decorator to implement rate limiting for endpoints.
    
    Args:
        max_requests: Maximum number of requests allowed
        window_seconds: Time window in seconds
        key_func: Function to generate rate limit key
        
    Returns:
        Decorated function
    """
    # Simple in-memory rate limiting (in production, use Redis)
    rate_limit_storage: Dict[str, List[float]] = {}
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract request and user info
            request = None
            user_id = None
            
            for key, value in kwargs.items():
                if isinstance(value, Request):
                    request = value
                elif key == 'current_user' and hasattr(value, 'id'):
                    user_id = str(value.id)
            
            # Generate rate limit key
            if key_func:
                rate_key = key_func(request, user_id)
            elif user_id:
                rate_key = f"user:{user_id}:{func.__name__}"
            else:
                # Use IP address as fallback
                client_ip = request.client.host if request else "unknown"
                rate_key = f"ip:{client_ip}:{func.__name__}"
            
            # Check rate limit
            current_time = time.time()
            window_start = current_time - window_seconds
            
            # Clean old entries
            if rate_key in rate_limit_storage:
                rate_limit_storage[rate_key] = [
                    timestamp for timestamp in rate_limit_storage[rate_key]
                    if timestamp > window_start
                ]
            else:
                rate_limit_storage[rate_key] = []
            
            # Check if limit exceeded
            if len(rate_limit_storage[rate_key]) >= max_requests:
                raise RateLimitError(
                    message="Rate limit exceeded",
                    limit=max_requests,
                    window=window_seconds
                )
            
            # Add current request
            rate_limit_storage[rate_key].append(current_time)
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator


def cache_response(
    ttl_seconds: int = 300,
    key_func: Optional[Callable] = None
):
    """
    Decorator to cache endpoint responses.
    
    Args:
        ttl_seconds: Time to live in seconds
        key_func: Function to generate cache key
        
    Returns:
        Decorated function
    """
    # Simple in-memory caching (in production, use Redis)
    cache_storage: Dict[str, Dict[str, Any]] = {}
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                # Simple key based on function name and arguments
                key_parts = [func.__name__]
                for key, value in sorted(kwargs.items()):
                    if hasattr(value, 'id'):
                        key_parts.append(f"{key}:{value.id}")
                    elif isinstance(value, (str, int, float)):
                        key_parts.append(f"{key}:{value}")
                cache_key = ":".join(key_parts)
            
            # Check cache
            current_time = time.time()
            if cache_key in cache_storage:
                cached_data = cache_storage[cache_key]
                if current_time - cached_data['timestamp'] < ttl_seconds:
                    return cached_data['data']
                else:
                    # Remove expired entry
                    del cache_storage[cache_key]
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            cache_storage[cache_key] = {
                'data': result,
                'timestamp': current_time
            }
            
            return result
        return wrapper
    return decorator


def log_execution_time(func: Callable) -> Callable:
    """
    Decorator to log function execution time.
    
    Returns:
        Decorated function
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        execution_time = time.time() - start_time
        print(f"{func.__name__} executed in {execution_time:.4f} seconds")
        return result
    return wrapper


def retry_on_failure(
    max_retries: int = 3,
    delay_seconds: float = 1.0,
    backoff_factor: float = 2.0
):
    """
    Decorator to retry function on failure.
    
    Args:
        max_retries: Maximum number of retries
        delay_seconds: Initial delay between retries
        backoff_factor: Factor to multiply delay by after each retry
        
    Returns:
        Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            delay = delay_seconds
            
            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries:
                        print(f"Attempt {attempt + 1} failed for {func.__name__}: {str(e)}")
                        print(f"Retrying in {delay} seconds...")
                        time.sleep(delay)
                        delay *= backoff_factor
                    else:
                        print(f"All {max_retries + 1} attempts failed for {func.__name__}")
            
            # If we get here, all retries failed
            raise last_exception
        return wrapper
    return decorator

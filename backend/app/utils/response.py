"""
Response utilities for AI Job Readiness Platform

This module provides standardized response utilities for consistent
API responses across the application.

Author: AI Job Readiness Team
Version: 1.0.0
"""

from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field
from fastapi import status
from fastapi.responses import JSONResponse


class ResponseModel(BaseModel):
    """Base response model for consistent API responses."""
    
    success: bool = Field(..., description="Whether the operation was successful")
    message: str = Field(..., description="Response message")
    data: Optional[Any] = Field(None, description="Response data if applicable")
    errors: Optional[List[str]] = Field(None, description="Error messages if any")
    meta: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")


class PaginationMeta(BaseModel):
    """Pagination metadata model."""
    
    page: int = Field(..., description="Current page number")
    per_page: int = Field(..., description="Number of items per page")
    total: int = Field(..., description="Total number of items")
    pages: int = Field(..., description="Total number of pages")
    has_next: bool = Field(..., description="Whether there are more pages")
    has_prev: bool = Field(..., description="Whether there are previous pages")


class PaginatedResponseModel(ResponseModel):
    """Paginated response model."""
    
    data: List[Any] = Field(..., description="List of items")
    pagination: PaginationMeta = Field(..., description="Pagination metadata")


def create_success_response(
    message: str = "Operation successful",
    data: Optional[Any] = None,
    meta: Optional[Dict[str, Any]] = None,
    status_code: int = status.HTTP_200_OK
) -> JSONResponse:
    """
    Create a standardized success response.
    
    Args:
        message: Success message
        data: Response data
        meta: Additional metadata
        status_code: HTTP status code
        
    Returns:
        JSONResponse: Standardized success response
    """
    response_data = ResponseModel(
        success=True,
        message=message,
        data=data,
        meta=meta
    )
    
    return JSONResponse(
        content=response_data.model_dump(exclude_none=True),
        status_code=status_code
    )


def create_error_response(
    message: str = "Operation failed",
    errors: Optional[List[str]] = None,
    status_code: int = status.HTTP_400_BAD_REQUEST,
    meta: Optional[Dict[str, Any]] = None
) -> JSONResponse:
    """
    Create a standardized error response.
    
    Args:
        message: Error message
        errors: List of specific error messages
        status_code: HTTP status code
        meta: Additional metadata
        
    Returns:
        JSONResponse: Standardized error response
    """
    response_data = ResponseModel(
        success=False,
        message=message,
        errors=errors,
        meta=meta
    )
    
    return JSONResponse(
        content=response_data.model_dump(exclude_none=True),
        status_code=status_code
    )


def create_paginated_response(
    data: List[Any],
    page: int,
    per_page: int,
    total: int,
    message: str = "Data retrieved successfully",
    meta: Optional[Dict[str, Any]] = None
) -> JSONResponse:
    """
    Create a standardized paginated response.
    
    Args:
        data: List of items
        page: Current page number
        per_page: Number of items per page
        total: Total number of items
        message: Success message
        meta: Additional metadata
        
    Returns:
        JSONResponse: Standardized paginated response
    """
    pages = (total + per_page - 1) // per_page
    has_next = page < pages
    has_prev = page > 1
    
    pagination = PaginationMeta(
        page=page,
        per_page=per_page,
        total=total,
        pages=pages,
        has_next=has_next,
        has_prev=has_prev
    )
    
    response_data = PaginatedResponseModel(
        success=True,
        message=message,
        data=data,
        pagination=pagination,
        meta=meta
    )
    
    return JSONResponse(
        content=response_data.model_dump(exclude_none=True),
        status_code=status.HTTP_200_OK
    )


def create_created_response(
    message: str = "Resource created successfully",
    data: Optional[Any] = None,
    meta: Optional[Dict[str, Any]] = None
) -> JSONResponse:
    """
    Create a standardized created response.
    
    Args:
        message: Success message
        data: Created resource data
        meta: Additional metadata
        
    Returns:
        JSONResponse: Standardized created response
    """
    return create_success_response(
        message=message,
        data=data,
        meta=meta,
        status_code=status.HTTP_201_CREATED
    )


def create_updated_response(
    message: str = "Resource updated successfully",
    data: Optional[Any] = None,
    meta: Optional[Dict[str, Any]] = None
) -> JSONResponse:
    """
    Create a standardized updated response.
    
    Args:
        message: Success message
        data: Updated resource data
        meta: Additional metadata
        
    Returns:
        JSONResponse: Standardized updated response
    """
    return create_success_response(
        message=message,
        data=data,
        meta=meta,
        status_code=status.HTTP_200_OK
    )


def create_deleted_response(
    message: str = "Resource deleted successfully",
    meta: Optional[Dict[str, Any]] = None
) -> JSONResponse:
    """
    Create a standardized deleted response.
    
    Args:
        message: Success message
        meta: Additional metadata
        
    Returns:
        JSONResponse: Standardized deleted response
    """
    return create_success_response(
        message=message,
        meta=meta,
        status_code=status.HTTP_200_OK
    )


def create_not_found_response(
    message: str = "Resource not found",
    errors: Optional[List[str]] = None
) -> JSONResponse:
    """
    Create a standardized not found response.
    
    Args:
        message: Error message
        errors: List of specific error messages
        
    Returns:
        JSONResponse: Standardized not found response
    """
    return create_error_response(
        message=message,
        errors=errors,
        status_code=status.HTTP_404_NOT_FOUND
    )


def create_unauthorized_response(
    message: str = "Authentication required",
    errors: Optional[List[str]] = None
) -> JSONResponse:
    """
    Create a standardized unauthorized response.
    
    Args:
        message: Error message
        errors: List of specific error messages
        
    Returns:
        JSONResponse: Standardized unauthorized response
    """
    return create_error_response(
        message=message,
        errors=errors,
        status_code=status.HTTP_401_UNAUTHORIZED
    )


def create_forbidden_response(
    message: str = "Access denied",
    errors: Optional[List[str]] = None
) -> JSONResponse:
    """
    Create a standardized forbidden response.
    
    Args:
        message: Error message
        errors: List of specific error messages
        
    Returns:
        JSONResponse: Standardized forbidden response
    """
    return create_error_response(
        message=message,
        errors=errors,
        status_code=status.HTTP_403_FORBIDDEN
    )


def create_validation_error_response(
    message: str = "Validation failed",
    errors: Optional[List[str]] = None
) -> JSONResponse:
    """
    Create a standardized validation error response.
    
    Args:
        message: Error message
        errors: List of specific error messages
        
    Returns:
        JSONResponse: Standardized validation error response
    """
    return create_error_response(
        message=message,
        errors=errors,
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )


def create_conflict_response(
    message: str = "Resource conflict",
    errors: Optional[List[str]] = None
) -> JSONResponse:
    """
    Create a standardized conflict response.
    
    Args:
        message: Error message
        errors: List of specific error messages
        
    Returns:
        JSONResponse: Standardized conflict response
    """
    return create_error_response(
        message=message,
        errors=errors,
        status_code=status.HTTP_409_CONFLICT
    )


def create_internal_error_response(
    message: str = "Internal server error",
    errors: Optional[List[str]] = None
) -> JSONResponse:
    """
    Create a standardized internal error response.
    
    Args:
        message: Error message
        errors: List of specific error messages
        
    Returns:
        JSONResponse: Standardized internal error response
    """
    return create_error_response(
        message=message,
        errors=errors,
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    )


def create_rate_limit_response(
    message: str = "Rate limit exceeded",
    errors: Optional[List[str]] = None
) -> JSONResponse:
    """
    Create a standardized rate limit response.
    
    Args:
        message: Error message
        errors: List of specific error messages
        
    Returns:
        JSONResponse: Standardized rate limit response
    """
    return create_error_response(
        message=message,
        errors=errors,
        status_code=status.HTTP_429_TOO_MANY_REQUESTS
    )

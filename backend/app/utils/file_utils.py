"""
File handling and validation utilities for AI Job Readiness Platform

This module provides utilities for file operations including validation,
processing, and management of uploaded files.

Author: AI Job Readiness Team
Version: 1.0.0
"""

import os
import uuid
from pathlib import Path
from typing import List, Optional, Tuple
from fastapi import UploadFile, HTTPException, status

from app.core.config import settings


def validate_file_extension(
    filename: str, 
    allowed_extensions: Optional[List[str]] = None
) -> bool:
    """
    Validate file extension against allowed extensions.
    
    Args:
        filename: Name of the file to validate
        allowed_extensions: List of allowed extensions (defaults to settings)
        
    Returns:
        bool: True if extension is allowed, False otherwise
    """
    if not filename:
        return False
    
    if allowed_extensions is None:
        allowed_extensions = settings.file.allowed_extensions
    
    file_ext = Path(filename).suffix.lower()
    return file_ext in allowed_extensions


def validate_file_size(
    file_size: int, 
    max_size: Optional[int] = None
) -> bool:
    """
    Validate file size against maximum allowed size.
    
    Args:
        file_size: Size of the file in bytes
        max_size: Maximum allowed size in bytes (defaults to settings)
        
    Returns:
        bool: True if size is within limits, False otherwise
    """
    if max_size is None:
        max_size = settings.file.max_file_size
    
    return file_size <= max_size


def generate_unique_filename(original_filename: str) -> str:
    """
    Generate a unique filename while preserving the original extension.
    
    Args:
        original_filename: Original filename
        
    Returns:
        str: Unique filename with preserved extension
    """
    if not original_filename:
        return str(uuid.uuid4())
    
    file_path = Path(original_filename)
    extension = file_path.suffix
    unique_id = str(uuid.uuid4())
    
    return f"{unique_id}{extension}"


def get_file_extension(filename: str) -> str:
    """
    Get file extension from filename.
    
    Args:
        filename: Name of the file
        
    Returns:
        str: File extension (including dot) or empty string
    """
    if not filename:
        return ""
    
    return Path(filename).suffix.lower()


def get_file_size_mb(file_size_bytes: int) -> float:
    """
    Convert file size from bytes to megabytes.
    
    Args:
        file_size_bytes: File size in bytes
        
    Returns:
        float: File size in megabytes (rounded to 2 decimal places)
    """
    return round(file_size_bytes / (1024 * 1024), 2)


def validate_upload_file(
    file: UploadFile,
    allowed_extensions: Optional[List[str]] = None,
    max_size: Optional[int] = None
) -> Tuple[bool, Optional[str]]:
    """
    Comprehensive file validation for uploads.
    
    Args:
        file: FastAPI UploadFile object
        allowed_extensions: List of allowed extensions
        max_size: Maximum file size in bytes
        
    Returns:
        Tuple[bool, Optional[str]]: (is_valid, error_message)
    """
    if not file.filename:
        return False, "No filename provided"
    
    # Validate extension
    if not validate_file_extension(file.filename, allowed_extensions):
        allowed = allowed_extensions or settings.file.allowed_extensions
        return False, f"File type not allowed. Allowed types: {', '.join(allowed)}"
    
    # Note: File size validation should be done after reading the file content
    # as UploadFile doesn't provide size before reading
    
    return True, None


async def save_upload_file(
    file: UploadFile,
    upload_dir: str,
    custom_filename: Optional[str] = None
) -> Tuple[str, str, int]:
    """
    Save uploaded file to disk.
    
    Args:
        file: FastAPI UploadFile object
        upload_dir: Directory to save the file
        custom_filename: Custom filename (if None, generates unique name)
        
    Returns:
        Tuple[str, str, int]: (file_path, filename, file_size)
        
    Raises:
        HTTPException: If file saving fails
    """
    try:
        # Create upload directory if it doesn't exist
        Path(upload_dir).mkdir(parents=True, exist_ok=True)
        
        # Generate filename
        if custom_filename:
            filename = custom_filename
        else:
            filename = generate_unique_filename(file.filename)
        
        file_path = os.path.join(upload_dir, filename)
        
        # Read file content
        content = await file.read()
        file_size = len(content)
        
        # Validate file size
        if not validate_file_size(file_size):
            max_size_mb = settings.file.max_file_size // (1024 * 1024)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File too large. Maximum size: {max_size_mb}MB"
            )
        
        # Save file
        with open(file_path, "wb") as buffer:
            buffer.write(content)
        
        return file_path, filename, file_size
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save file: {str(e)}"
        )


def delete_file(file_path: str) -> bool:
    """
    Delete file from disk.
    
    Args:
        file_path: Path to the file to delete
        
    Returns:
        bool: True if file was deleted successfully, False otherwise
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except OSError:
        return False


def get_file_info(file_path: str) -> Optional[dict]:
    """
    Get file information.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Optional[dict]: File information or None if file doesn't exist
    """
    try:
        if not os.path.exists(file_path):
            return None
        
        stat = os.stat(file_path)
        return {
            "path": file_path,
            "filename": os.path.basename(file_path),
            "size": stat.st_size,
            "size_mb": get_file_size_mb(stat.st_size),
            "extension": get_file_extension(file_path),
            "created_at": stat.st_ctime,
            "modified_at": stat.st_mtime,
        }
    except OSError:
        return None


def ensure_upload_directory(upload_dir: str) -> bool:
    """
    Ensure upload directory exists.
    
    Args:
        upload_dir: Directory path to create
        
    Returns:
        bool: True if directory exists or was created successfully
    """
    try:
        Path(upload_dir).mkdir(parents=True, exist_ok=True)
        return True
    except OSError:
        return False


def get_safe_filename(filename: str) -> str:
    """
    Get a safe filename by removing or replacing unsafe characters.
    
    Args:
        filename: Original filename
        
    Returns:
        str: Safe filename
    """
    if not filename:
        return str(uuid.uuid4())
    
    # Remove or replace unsafe characters
    safe_chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-_"
    safe_filename = "".join(c if c in safe_chars else "_" for c in filename)
    
    # Remove multiple consecutive underscores
    while "__" in safe_filename:
        safe_filename = safe_filename.replace("__", "_")
    
    # Remove leading/trailing underscores and dots
    safe_filename = safe_filename.strip("._")
    
    # Ensure filename is not empty
    if not safe_filename:
        safe_filename = str(uuid.uuid4())
    
    return safe_filename

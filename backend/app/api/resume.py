"""
Resume API Router for AI Job Readiness Platform

This module provides comprehensive API endpoints for resume management including:
- CRUD operations for resumes
- File upload and management
- Resume analysis and scoring
- User-specific resume operations
- Public resume sharing

Author: AI Job Readiness Team
Version: 1.0.0
"""

import uuid
import os
import shutil
from datetime import datetime
from typing import List, Optional, Dict, Any
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Query, status
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func, desc
from sqlalchemy.orm import selectinload

from app.db.database import get_db
from app.models.user import User
from app.models.resume import Resume
from app.models.score import Score
from app.schemas.resume import (
    ResumeCreate, 
    ResumeUpdate, 
    ResumeResponse, 
    ResumeListResponse,
    ResumeFileUpload,
    ResumeAnalysisRequest
)
from app.core.users import current_active_user
from app.core.config import settings

# Create router instance
router = APIRouter(prefix="/resumes", tags=["Resumes"])

# Configure file upload settings
UPLOAD_DIR = Path("uploads/resumes")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
ALLOWED_EXTENSIONS = {".pdf", ".doc", ".docx", ".txt"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


@router.post("/", response_model=ResumeResponse, status_code=status.HTTP_201_CREATED)
async def create_resume(
    resume_data: ResumeCreate,
    current_user: User = Depends(current_active_user),
    db: AsyncSession = Depends(get_db)
) -> ResumeResponse:
    """
    Create a new resume for the current user.
    
    This endpoint allows authenticated users to create a new resume
    with basic information and optional file metadata.
    
    Args:
        resume_data: Resume creation data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        ResumeResponse: Created resume data
        
    Raises:
        HTTPException: If resume creation fails
    """
    try:
        # Create new resume instance
        resume = Resume(
            user_id=current_user.id,
            title=resume_data.title,
            summary=resume_data.summary,
            experience_years=resume_data.experience_years,
            education_level=resume_data.education_level,
            is_public=resume_data.is_public,
            file_name=resume_data.file_name,
            file_type=resume_data.file_type
        )
        
        # Set skills and languages if provided
        if resume_data.skills:
            resume.set_skills_list(resume_data.skills)
        if resume_data.languages:
            resume.set_languages_list(resume_data.languages)
        
        # Add to database
        db.add(resume)
        await db.commit()
        await db.refresh(resume)
        
        return ResumeResponse.model_validate(resume)
        
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create resume: {str(e)}"
        )


@router.get("/", response_model=ResumeListResponse)
async def list_user_resumes(
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Number of resumes per page"),
    is_active: Optional[bool] = Query(None, description="Filter by active status"),
    is_public: Optional[bool] = Query(None, description="Filter by public status"),
    current_user: User = Depends(current_active_user),
    db: AsyncSession = Depends(get_db)
) -> ResumeListResponse:
    """
    List resumes for the current user with pagination and filtering.
    
    This endpoint returns a paginated list of resumes belonging to the
    current user with optional filtering by status.
    
    Args:
        page: Page number (1-based)
        size: Number of resumes per page
        is_active: Filter by active status
        is_public: Filter by public status
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        ResumeListResponse: Paginated list of resumes
    """
    try:
        # Build query
        query = select(Resume).where(Resume.user_id == current_user.id)
        
        # Apply filters
        if is_active is not None:
            query = query.where(Resume.is_active == is_active)
        if is_public is not None:
            query = query.where(Resume.is_public == is_public)
        
        # Get total count
        count_query = select(func.count(Resume.id)).where(Resume.user_id == current_user.id)
        if is_active is not None:
            count_query = count_query.where(Resume.is_active == is_active)
        if is_public is not None:
            count_query = count_query.where(Resume.is_public == is_public)
        
        total_result = await db.execute(count_query)
        total = total_result.scalar()
        
        # Apply pagination
        offset = (page - 1) * size
        query = query.offset(offset).limit(size).order_by(desc(Resume.created_at))
        
        # Execute query
        result = await db.execute(query)
        resumes = result.scalars().all()
        
        # Calculate pagination info
        pages = (total + size - 1) // size
        
        return ResumeListResponse(
            resumes=[ResumeResponse.model_validate(resume) for resume in resumes],
            total=total,
            page=page,
            size=size,
            pages=pages
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list resumes: {str(e)}"
        )


@router.get("/{resume_id}", response_model=ResumeResponse)
async def get_resume(
    resume_id: int,
    current_user: User = Depends(current_active_user),
    db: AsyncSession = Depends(get_db)
) -> ResumeResponse:
    """
    Get a specific resume by ID.
    
    This endpoint returns detailed information about a specific resume
    belonging to the current user.
    
    Args:
        resume_id: ID of the resume to retrieve
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        ResumeResponse: Resume data
        
    Raises:
        HTTPException: If resume not found or access denied
    """
    try:
        # Query resume with user validation
        query = select(Resume).where(
            and_(Resume.id == resume_id, Resume.user_id == current_user.id)
        )
        result = await db.execute(query)
        resume = result.scalar_one_or_none()
        
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found or access denied"
            )
        
        return ResumeResponse.model_validate(resume)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get resume: {str(e)}"
        )


@router.put("/{resume_id}", response_model=ResumeResponse)
async def update_resume(
    resume_id: int,
    resume_data: ResumeUpdate,
    current_user: User = Depends(current_active_user),
    db: AsyncSession = Depends(get_db)
) -> ResumeResponse:
    """
    Update an existing resume.
    
    This endpoint allows partial updates of resume information.
    Only provided fields will be updated.
    
    Args:
        resume_id: ID of the resume to update
        resume_data: Updated resume data
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        ResumeResponse: Updated resume data
        
    Raises:
        HTTPException: If resume not found or update fails
    """
    try:
        # Get existing resume
        query = select(Resume).where(
            and_(Resume.id == resume_id, Resume.user_id == current_user.id)
        )
        result = await db.execute(query)
        resume = result.scalar_one_or_none()
        
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found or access denied"
            )
        
        # Update fields if provided
        update_data = resume_data.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            if field == "skills" and value is not None:
                resume.set_skills_list(value)
            elif field == "languages" and value is not None:
                resume.set_languages_list(value)
            else:
                setattr(resume, field, value)
        
        # Update timestamp
        resume.updated_at = datetime.utcnow()
        
        await db.commit()
        await db.refresh(resume)
        
        return ResumeResponse.model_validate(resume)
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update resume: {str(e)}"
        )


@router.delete("/{resume_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_resume(
    resume_id: int,
    current_user: User = Depends(current_active_user),
    db: AsyncSession = Depends(get_db)
) -> None:
    """
    Delete a resume.
    
    This endpoint permanently deletes a resume and all associated files.
    
    Args:
        resume_id: ID of the resume to delete
        current_user: Current authenticated user
        db: Database session
        
    Raises:
        HTTPException: If resume not found or deletion fails
    """
    try:
        # Get existing resume
        query = select(Resume).where(
            and_(Resume.id == resume_id, Resume.user_id == current_user.id)
        )
        result = await db.execute(query)
        resume = result.scalar_one_or_none()
        
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found or access denied"
            )
        
        # Delete associated file if exists
        if resume.file_path and os.path.exists(resume.file_path):
            try:
                os.remove(resume.file_path)
            except OSError:
                pass  # Continue even if file deletion fails
        
        # Delete from database
        await db.delete(resume)
        await db.commit()
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete resume: {str(e)}"
        )


@router.post("/{resume_id}/upload", response_model=ResumeResponse)
async def upload_resume_file(
    resume_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(current_active_user),
    db: AsyncSession = Depends(get_db)
) -> ResumeResponse:
    """
    Upload a resume file.
    
    This endpoint allows users to upload resume files (PDF, DOC, DOCX, TXT)
    and associates them with an existing resume.
    
    Args:
        resume_id: ID of the resume to upload file for
        file: Uploaded file
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        ResumeResponse: Updated resume data
        
    Raises:
        HTTPException: If upload fails or file is invalid
    """
    try:
        # Get existing resume
        query = select(Resume).where(
            and_(Resume.id == resume_id, Resume.user_id == current_user.id)
        )
        result = await db.execute(query)
        resume = result.scalar_one_or_none()
        
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found or access denied"
            )
        
        # Validate file
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No filename provided"
            )
        
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        
        # Check file size
        file_content = await file.read()
        if len(file_content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File too large. Maximum size: {MAX_FILE_SIZE // (1024*1024)}MB"
            )
        
        # Generate unique filename
        file_id = str(uuid.uuid4())
        filename = f"{file_id}{file_ext}"
        file_path = UPLOAD_DIR / filename
        
        # Save file
        with open(file_path, "wb") as buffer:
            buffer.write(file_content)
        
        # Update resume with file information
        resume.file_name = file.filename
        resume.file_path = str(file_path)
        resume.file_size = len(file_content)
        resume.file_type = file_ext[1:].upper()  # Remove dot and uppercase
        resume.updated_at = datetime.utcnow()
        
        await db.commit()
        await db.refresh(resume)
        
        return ResumeResponse.model_validate(resume)
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload file: {str(e)}"
        )


@router.get("/{resume_id}/download")
async def download_resume_file(
    resume_id: int,
    current_user: User = Depends(current_active_user),
    db: AsyncSession = Depends(get_db)
) -> FileResponse:
    """
    Download a resume file.
    
    This endpoint allows users to download their resume files.
    
    Args:
        resume_id: ID of the resume to download
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        FileResponse: Resume file
        
    Raises:
        HTTPException: If file not found or access denied
    """
    try:
        # Get resume with file information
        query = select(Resume).where(
            and_(Resume.id == resume_id, Resume.user_id == current_user.id)
        )
        result = await db.execute(query)
        resume = result.scalar_one_or_none()
        
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found or access denied"
            )
        
        if not resume.file_path or not os.path.exists(resume.file_path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume file not found"
            )
        
        return FileResponse(
            path=resume.file_path,
            filename=resume.file_name or f"resume_{resume_id}.{resume.file_type.lower()}",
            media_type="application/octet-stream"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to download file: {str(e)}"
        )


@router.post("/{resume_id}/analyze", response_model=Dict[str, Any])
async def analyze_resume(
    resume_id: int,
    analysis_request: ResumeAnalysisRequest,
    current_user: User = Depends(current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Analyze a resume against job requirements.
    
    This endpoint triggers AI-powered analysis of a resume against
    specific job requirements or general job readiness criteria.
    
    Args:
        resume_id: ID of the resume to analyze
        analysis_request: Analysis parameters
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Dict[str, Any]: Analysis results
        
    Raises:
        HTTPException: If analysis fails
    """
    try:
        # Get resume
        query = select(Resume).where(
            and_(Resume.id == resume_id, Resume.user_id == current_user.id)
        )
        result = await db.execute(query)
        resume = result.scalar_one_or_none()
        
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found or access denied"
            )
        
        # Update last analyzed timestamp
        resume.last_analyzed = datetime.utcnow()
        await db.commit()
        
        # TODO: Implement actual AI analysis logic
        # This is a placeholder implementation
        analysis_result = {
            "resume_id": resume_id,
            "analysis_timestamp": resume.last_analyzed.isoformat(),
            "job_title": analysis_request.job_title,
            "company": analysis_request.company,
            "overall_score": 85.5,
            "strengths": [
                "Strong technical skills",
                "Relevant experience",
                "Good education background"
            ],
            "areas_for_improvement": [
                "Add more specific achievements",
                "Include quantifiable results",
                "Update contact information"
            ],
            "skills_match": 0.8,
            "experience_match": 0.75,
            "education_match": 0.9,
            "recommendations": [
                "Highlight your most relevant projects",
                "Add metrics to quantify your achievements",
                "Tailor your summary to the job description"
            ]
        }
        
        return analysis_result
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze resume: {str(e)}"
        )


@router.get("/public/{resume_id}", response_model=ResumeResponse)
async def get_public_resume(
    resume_id: int,
    db: AsyncSession = Depends(get_db)
) -> ResumeResponse:
    """
    Get a public resume by ID.
    
    This endpoint allows access to resumes that are marked as public.
    No authentication is required.
    
    Args:
        resume_id: ID of the public resume
        db: Database session
        
    Returns:
        ResumeResponse: Public resume data
        
    Raises:
        HTTPException: If resume not found or not public
    """
    try:
        # Query public resume
        query = select(Resume).where(
            and_(Resume.id == resume_id, Resume.is_public == True, Resume.is_active == True)
        )
        result = await db.execute(query)
        resume = result.scalar_one_or_none()
        
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Public resume not found"
            )
        
        return ResumeResponse.model_validate(resume)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get public resume: {str(e)}"
        )


@router.get("/stats/summary", response_model=Dict[str, Any])
async def get_resume_stats(
    current_user: User = Depends(current_active_user),
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get resume statistics for the current user.
    
    This endpoint provides summary statistics about the user's resumes
    including counts, file types, and analysis status.
    
    Args:
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        Dict[str, Any]: Resume statistics
    """
    try:
        # Get basic counts
        total_query = select(func.count(Resume.id)).where(Resume.user_id == current_user.id)
        active_query = select(func.count(Resume.id)).where(
            and_(Resume.user_id == current_user.id, Resume.is_active == True)
        )
        public_query = select(func.count(Resume.id)).where(
            and_(Resume.user_id == current_user.id, Resume.is_public == True)
        )
        analyzed_query = select(func.count(Resume.id)).where(
            and_(Resume.user_id == current_user.id, Resume.last_analyzed.isnot(None))
        )
        
        total_result = await db.execute(total_query)
        active_result = await db.execute(active_query)
        public_result = await db.execute(public_query)
        analyzed_result = await db.execute(analyzed_query)
        
        total = total_result.scalar()
        active = active_result.scalar()
        public = public_result.scalar()
        analyzed = analyzed_result.scalar()
        
        # Get file type distribution
        file_types_query = select(
            Resume.file_type, 
            func.count(Resume.id).label('count')
        ).where(
            and_(Resume.user_id == current_user.id, Resume.file_type.isnot(None))
        ).group_by(Resume.file_type)
        
        file_types_result = await db.execute(file_types_query)
        file_types = {row.file_type: row.count for row in file_types_result}
        
        return {
            "total_resumes": total,
            "active_resumes": active,
            "public_resumes": public,
            "analyzed_resumes": analyzed,
            "file_types": file_types,
            "analysis_rate": round(analyzed / total * 100, 2) if total > 0 else 0
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get resume stats: {str(e)}"
        )

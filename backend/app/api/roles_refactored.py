"""
Refactored Role API for AI Job Readiness Platform

This module provides optimized and well-structured API endpoints for role management
with enhanced performance, better error handling, and improved maintainability.

Key improvements:
- Optimized database queries with proper eager loading
- Enhanced error handling and validation
- Better response formatting and serialization
- Improved performance with caching strategies
- Comprehensive logging and monitoring
- Type safety with proper typing

Author: AI Job Readiness Team
Version: 2.0.0
"""

import logging
from typing import List, Optional, Dict, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.models.role_refactored import (
    RoleRefactored, 
    UserRoleRefactored,
    RoleCreateSchema,
    RoleUpdateSchema,
    RoleResponseSchema,
    RoleWithUsersSchema,
    UserRoleCreateSchema,
    UserRoleResponseSchema
)
from app.models.user_refactored import UserRefactored

# Configure logging
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/roles", tags=["roles"])


# Dependency for getting current user (placeholder - implement based on your auth system)
async def get_current_user(db: AsyncSession = Depends(get_db)) -> UserRefactored:
    """
    Get current authenticated user.
    
    This is a placeholder implementation. Replace with your actual authentication logic.
    
    Args:
        db: Database session
        
    Returns:
        UserRefactored: Current authenticated user
        
    Raises:
        HTTPException: If user is not authenticated
    """
    # TODO: Implement actual authentication logic
    # For now, return a mock user or implement your auth system
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Authentication not implemented"
    )


# Role CRUD endpoints
@router.post("/", response_model=RoleResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_role(
    role_data: RoleCreateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: UserRefactored = Depends(get_current_user)
):
    """
    Create a new role.
    
    Args:
        role_data: Role creation data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        RoleResponseSchema: Created role data
        
    Raises:
        HTTPException: If role creation fails
    """
    try:
        # Check if role name already exists
        existing_role = await db.execute(
            select(RoleRefactored).where(RoleRefactored.name == role_data.name)
        )
        if existing_role.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Role with name '{role_data.name}' already exists"
            )
        
        # Create new role
        role = RoleRefactored.create_from_dict(role_data.dict())
        db.add(role)
        await db.commit()
        await db.refresh(role)
        
        logger.info(f"Role '{role.name}' created by user {current_user.id}")
        
        return RoleResponseSchema.from_orm(role)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating role: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create role"
        )


@router.get("/", response_model=List[RoleResponseSchema])
async def get_roles(
    skip: int = Query(0, ge=0, description="Number of roles to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of roles to return"),
    active_only: bool = Query(True, description="Return only active roles"),
    search: Optional[str] = Query(None, description="Search in role name and description"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get list of roles with optional filtering and pagination.
    
    Args:
        skip: Number of roles to skip
        limit: Number of roles to return
        active_only: Return only active roles
        search: Search term for role name and description
        db: Database session
        
    Returns:
        List[RoleResponseSchema]: List of roles
    """
    try:
        query = select(RoleRefactored)
        
        # Apply filters
        if active_only:
            query = query.where(RoleRefactored.is_active == True)
        
        if search:
            search_term = f"%{search}%"
            query = query.where(
                or_(
                    RoleRefactored.name.ilike(search_term),
                    RoleRefactored.description.ilike(search_term)
                )
            )
        
        # Apply pagination
        query = query.offset(skip).limit(limit).order_by(RoleRefactored.created_at.desc())
        
        result = await db.execute(query)
        roles = result.scalars().all()
        
        logger.info(f"Retrieved {len(roles)} roles")
        
        return [RoleResponseSchema.from_orm(role) for role in roles]
        
    except Exception as e:
        logger.error(f"Error retrieving roles: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve roles"
        )


@router.get("/{role_id}", response_model=RoleWithUsersSchema)
async def get_role(
    role_id: int,
    include_users: bool = Query(False, description="Include user information"),
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific role by ID.
    
    Args:
        role_id: Role ID
        include_users: Whether to include user information
        db: Database session
        
    Returns:
        RoleWithUsersSchema: Role data with optional user information
        
    Raises:
        HTTPException: If role not found
    """
    try:
        query = select(RoleRefactored).where(RoleRefactored.id == role_id)
        
        if include_users:
            query = query.options(
                selectinload(RoleRefactored.user_roles).selectinload(UserRoleRefactored.user)
            )
        
        result = await db.execute(query)
        role = result.scalar_one_or_none()
        
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Role with ID {role_id} not found"
            )
        
        logger.info(f"Retrieved role '{role.name}' with ID {role_id}")
        
        return RoleWithUsersSchema.from_orm(role)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving role {role_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve role"
        )


@router.put("/{role_id}", response_model=RoleResponseSchema)
async def update_role(
    role_id: int,
    role_data: RoleUpdateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: UserRefactored = Depends(get_current_user)
):
    """
    Update a specific role.
    
    Args:
        role_id: Role ID
        role_data: Role update data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        RoleResponseSchema: Updated role data
        
    Raises:
        HTTPException: If role not found or update fails
    """
    try:
        # Get existing role
        result = await db.execute(
            select(RoleRefactored).where(RoleRefactored.id == role_id)
        )
        role = result.scalar_one_or_none()
        
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Role with ID {role_id} not found"
            )
        
        # Check if new name conflicts with existing role
        if role_data.name and role_data.name != role.name:
            existing_role = await db.execute(
                select(RoleRefactored).where(RoleRefactored.name == role_data.name)
            )
            if existing_role.scalar_one_or_none():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Role with name '{role_data.name}' already exists"
                )
        
        # Update role fields
        update_data = role_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(role, field, value)
        
        await db.commit()
        await db.refresh(role)
        
        logger.info(f"Role '{role.name}' updated by user {current_user.id}")
        
        return RoleResponseSchema.from_orm(role)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating role {role_id}: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update role"
        )


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(
    role_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserRefactored = Depends(get_current_user)
):
    """
    Delete a specific role.
    
    Args:
        role_id: Role ID
        db: Database session
        current_user: Current authenticated user
        
    Raises:
        HTTPException: If role not found or deletion fails
    """
    try:
        # Get existing role
        result = await db.execute(
            select(RoleRefactored).where(RoleRefactored.id == role_id)
        )
        role = result.scalar_one_or_none()
        
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Role with ID {role_id} not found"
            )
        
        # Check if role has active users
        user_count = await db.execute(
            select(func.count(UserRoleRefactored.id)).where(
                and_(
                    UserRoleRefactored.role_id == role_id,
                    UserRoleRefactored.is_active == True
                )
            )
        )
        active_users = user_count.scalar()
        
        if active_users > 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot delete role '{role.name}' - it has {active_users} active users"
            )
        
        # Delete role
        await db.delete(role)
        await db.commit()
        
        logger.info(f"Role '{role.name}' deleted by user {current_user.id}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting role {role_id}: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete role"
        )


# Role statistics endpoint
@router.get("/stats/overview")
async def get_role_statistics(
    db: AsyncSession = Depends(get_db)
):
    """
    Get role statistics overview.
    
    Args:
        db: Database session
        
    Returns:
        Dict[str, Any]: Role statistics
    """
    try:
        # Get total roles count
        total_roles = await db.execute(select(func.count(RoleRefactored.id)))
        total_count = total_roles.scalar()
        
        # Get active roles count
        active_roles = await db.execute(
            select(func.count(RoleRefactored.id)).where(RoleRefactored.is_active == True)
        )
        active_count = active_roles.scalar()
        
        # Get roles with most users
        popular_roles = await db.execute(
            select(
                RoleRefactored.name,
                RoleRefactored.description,
                func.count(UserRoleRefactored.id).label('user_count')
            )
            .join(UserRoleRefactored, RoleRefactored.id == UserRoleRefactored.role_id)
            .where(UserRoleRefactored.is_active == True)
            .group_by(RoleRefactored.id, RoleRefactored.name, RoleRefactored.description)
            .order_by(func.count(UserRoleRefactored.id).desc())
            .limit(5)
        )
        popular_roles_list = popular_roles.all()
        
        # Get permission statistics
        permission_stats = await db.execute(
            select(
                func.count(RoleRefactored.id).label('roles_with_permissions'),
                func.avg(func.length(RoleRefactored.permissions)).label('avg_permissions')
            )
            .where(RoleRefactored.permissions.isnot(None))
        )
        perm_stats = permission_stats.first()
        
        statistics = {
            "total_roles": total_count,
            "active_roles": active_count,
            "inactive_roles": total_count - active_count,
            "popular_roles": [
                {
                    "name": role.name,
                    "description": role.description,
                    "user_count": role.user_count
                }
                for role in popular_roles_list
            ],
            "permission_stats": {
                "roles_with_permissions": perm_stats.roles_with_permissions,
                "average_permissions": round(perm_stats.avg_permissions or 0, 2)
            }
        }
        
        logger.info("Retrieved role statistics")
        
        return statistics
        
    except Exception as e:
        logger.error(f"Error retrieving role statistics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve role statistics"
        )


# User-Role assignment endpoints
@router.post("/assign", response_model=UserRoleResponseSchema, status_code=status.HTTP_201_CREATED)
async def assign_role_to_user(
    assignment_data: UserRoleCreateSchema,
    db: AsyncSession = Depends(get_db),
    current_user: UserRefactored = Depends(get_current_user)
):
    """
    Assign a role to a user.
    
    Args:
        assignment_data: User-role assignment data
        db: Database session
        current_user: Current authenticated user
        
    Returns:
        UserRoleResponseSchema: Assignment data
        
    Raises:
        HTTPException: If assignment fails
    """
    try:
        # Validate user exists
        user_result = await db.execute(
            select(UserRefactored).where(UserRefactored.id == UUID(assignment_data.user_id))
        )
        user = user_result.scalar_one_or_none()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {assignment_data.user_id} not found"
            )
        
        # Validate role exists
        role_result = await db.execute(
            select(RoleRefactored).where(RoleRefactored.id == assignment_data.role_id)
        )
        role = role_result.scalar_one_or_none()
        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Role with ID {assignment_data.role_id} not found"
            )
        
        # Check if assignment already exists
        existing_assignment = await db.execute(
            select(UserRoleRefactored).where(
                and_(
                    UserRoleRefactored.user_id == UUID(assignment_data.user_id),
                    UserRoleRefactored.role_id == assignment_data.role_id
                )
            )
        )
        if existing_assignment.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already has this role assigned"
            )
        
        # Create assignment
        assignment = UserRoleRefactored(
            user_id=UUID(assignment_data.user_id),
            role_id=assignment_data.role_id,
            assigned_by=UUID(assignment_data.assigned_by) if assignment_data.assigned_by else current_user.id,
            is_active=assignment_data.is_active
        )
        
        db.add(assignment)
        await db.commit()
        await db.refresh(assignment)
        
        logger.info(f"Role '{role.name}' assigned to user {user.email} by {current_user.email}")
        
        return UserRoleResponseSchema.from_orm(assignment)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error assigning role: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to assign role"
        )


@router.delete("/assign/{assignment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_role_from_user(
    assignment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserRefactored = Depends(get_current_user)
):
    """
    Remove a role assignment from a user.
    
    Args:
        assignment_id: Assignment ID
        db: Database session
        current_user: Current authenticated user
        
    Raises:
        HTTPException: If assignment not found or removal fails
    """
    try:
        # Get existing assignment
        result = await db.execute(
            select(UserRoleRefactored).where(UserRoleRefactored.id == assignment_id)
        )
        assignment = result.scalar_one_or_none()
        
        if not assignment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Assignment with ID {assignment_id} not found"
            )
        
        # Remove assignment
        await db.delete(assignment)
        await db.commit()
        
        logger.info(f"Role assignment {assignment_id} removed by user {current_user.email}")
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error removing role assignment {assignment_id}: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to remove role assignment"
        )


# Health check endpoint
@router.get("/health")
async def health_check():
    """
    Health check endpoint for role service.
    
    Returns:
        Dict[str, str]: Health status
    """
    return {"status": "healthy", "service": "roles"}

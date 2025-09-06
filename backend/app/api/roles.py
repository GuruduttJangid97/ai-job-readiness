"""
Role API endpoints for AI Job Readiness Platform

This module provides REST API endpoints for role management including
role creation, updates, assignment, and permission management.

Key Features:
- CRUD operations for roles
- Role assignment to users
- Permission management
- Role statistics and reporting
- Comprehensive error handling and validation

Author: AI Job Readiness Team
Version: 1.0.0
"""

import uuid
from datetime import datetime
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import selectinload

from app.db.database import get_db
from app.models.role import Role, UserRole
from app.models.user import User
from app.schemas.role import (
    RoleCreate, RoleUpdate, RoleRead, RoleResponse, RoleListResponse,
    UserRoleAssignment, UserRoleAssignmentResponse, UserRoleListResponse,
    RolePermissionUpdate, RoleStats, RoleStatsResponse
)
from app.schemas.user import UserProfile
from app.core.security import get_current_user

# Create router for role endpoints
router = APIRouter(prefix="/roles", tags=["roles"])


@router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create_role(
    role_data: RoleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new role.
    
    This endpoint allows authorized users to create new roles with
    specified permissions and metadata.
    
    Args:
        role_data: Role creation data
        db: Database session
        current_user: Currently authenticated user
        
    Returns:
        RoleResponse: Created role information
        
    Raises:
        HTTPException: If role name already exists or user lacks permissions
    """
    # Check if user has permission to create roles
    if not current_user.is_superuser and not current_user.has_role("admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to create roles"
        )
    
    # Check if role name already exists
    existing_role = await db.execute(
        select(Role).where(Role.name == role_data.name)
    )
    if existing_role.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Role with name '{role_data.name}' already exists"
        )
    
    # Create new role
    role = Role(
        name=role_data.name,
        description=role_data.description,
        permissions=role_data.permissions,
        is_active=role_data.is_active
    )
    
    # Set permissions as JSON string
    if role_data.permissions:
        role.set_permissions_list(role_data.permissions)
    
    db.add(role)
    await db.commit()
    await db.refresh(role)
    
    return RoleResponse(
        success=True,
        message="Role created successfully",
        data=RoleRead.from_orm(role)
    )


@router.get("/", response_model=RoleListResponse)
async def get_roles(
    skip: int = Query(0, ge=0, description="Number of roles to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of roles to return"),
    active_only: bool = Query(True, description="Return only active roles"),
    search: Optional[str] = Query(None, description="Search term for role name or description"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get list of roles with pagination and filtering.
    
    This endpoint returns a paginated list of roles with optional
    filtering by active status and search terms.
    
    Args:
        skip: Number of roles to skip for pagination
        limit: Maximum number of roles to return
        active_only: Whether to return only active roles
        search: Search term for filtering
        db: Database session
        current_user: Currently authenticated user
        
    Returns:
        RoleListResponse: Paginated list of roles
    """
    # Build query
    query = select(Role)
    
    # Apply filters
    if active_only:
        query = query.where(Role.is_active == True)
    
    if search:
        search_term = f"%{search}%"
        query = query.where(
            or_(
                Role.name.ilike(search_term),
                Role.description.ilike(search_term)
            )
        )
    
    # Get total count
    count_query = select(func.count(Role.id))
    if active_only:
        count_query = count_query.where(Role.is_active == True)
    if search:
        search_term = f"%{search}%"
        count_query = count_query.where(
            or_(
                Role.name.ilike(search_term),
                Role.description.ilike(search_term)
            )
        )
    
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # Apply pagination and ordering
    query = query.order_by(Role.name).offset(skip).limit(limit)
    
    # Execute query
    result = await db.execute(query)
    roles = result.scalars().all()
    
    # Convert to response format
    role_data = [RoleRead.from_orm(role) for role in roles]
    
    return RoleListResponse(
        success=True,
        message=f"Retrieved {len(role_data)} roles",
        data=role_data,
        total=total,
        page=(skip // limit) + 1,
        per_page=limit,
        has_next=skip + limit < total,
        has_prev=skip > 0
    )


@router.get("/{role_id}", response_model=RoleResponse)
async def get_role(
    role_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific role by ID.
    
    Args:
        role_id: ID of the role to retrieve
        db: Database session
        current_user: Currently authenticated user
        
    Returns:
        RoleResponse: Role information
        
    Raises:
        HTTPException: If role not found
    """
    result = await db.execute(
        select(Role).where(Role.id == role_id)
    )
    role = result.scalar_one_or_none()
    
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role with ID {role_id} not found"
        )
    
    return RoleResponse(
        success=True,
        message="Role retrieved successfully",
        data=RoleRead.from_orm(role)
    )


@router.put("/{role_id}", response_model=RoleResponse)
async def update_role(
    role_id: int,
    role_data: RoleUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update an existing role.
    
    Args:
        role_id: ID of the role to update
        role_data: Updated role data
        db: Database session
        current_user: Currently authenticated user
        
    Returns:
        RoleResponse: Updated role information
        
    Raises:
        HTTPException: If role not found or user lacks permissions
    """
    # Check if user has permission to update roles
    if not current_user.is_superuser and not current_user.has_role("admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to update roles"
        )
    
    # Get existing role
    result = await db.execute(
        select(Role).where(Role.id == role_id)
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
            select(Role).where(Role.name == role_data.name)
        )
        if existing_role.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Role with name '{role_data.name}' already exists"
            )
    
    # Update role fields
    update_data = role_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        if field == "permissions" and value is not None:
            role.set_permissions_list(value)
        else:
            setattr(role, field, value)
    
    role.updated_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(role)
    
    return RoleResponse(
        success=True,
        message="Role updated successfully",
        data=RoleRead.from_orm(role)
    )


@router.delete("/{role_id}", response_model=RoleResponse)
async def delete_role(
    role_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a role.
    
    Args:
        role_id: ID of the role to delete
        db: Database session
        current_user: Currently authenticated user
        
    Returns:
        RoleResponse: Deletion confirmation
        
    Raises:
        HTTPException: If role not found or user lacks permissions
    """
    # Check if user has permission to delete roles
    if not current_user.is_superuser and not current_user.has_role("admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to delete roles"
        )
    
    # Get existing role
    result = await db.execute(
        select(Role).where(Role.id == role_id)
    )
    role = result.scalar_one_or_none()
    
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role with ID {role_id} not found"
        )
    
    # Check if role is assigned to any users
    user_roles_count = await db.execute(
        select(func.count(UserRole.id)).where(UserRole.role_id == role_id)
    )
    if user_roles_count.scalar() > 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete role that is assigned to users. Remove all assignments first."
        )
    
    await db.delete(role)
    await db.commit()
    
    return RoleResponse(
        success=True,
        message="Role deleted successfully",
        data=None
    )


@router.post("/assign", response_model=RoleResponse)
async def assign_role_to_user(
    assignment: UserRoleAssignment,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Assign a role to a user.
    
    Args:
        assignment: Role assignment data
        db: Database session
        current_user: Currently authenticated user
        
    Returns:
        RoleResponse: Assignment confirmation
        
    Raises:
        HTTPException: If user or role not found, or user lacks permissions
    """
    # Check if user has permission to assign roles
    if not current_user.is_superuser and not current_user.has_role("admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to assign roles"
        )
    
    # Verify user exists
    user_result = await db.execute(
        select(User).where(User.id == assignment.user_id)
    )
    user = user_result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {assignment.user_id} not found"
        )
    
    # Verify role exists and is active
    role_result = await db.execute(
        select(Role).where(Role.id == assignment.role_id)
    )
    role = role_result.scalar_one_or_none()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role with ID {assignment.role_id} not found"
        )
    
    if not role.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot assign inactive role"
        )
    
    # Check if assignment already exists
    existing_assignment = await db.execute(
        select(UserRole).where(
            and_(
                UserRole.user_id == assignment.user_id,
                UserRole.role_id == assignment.role_id,
                UserRole.is_active == True
            )
        )
    )
    if existing_assignment.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already has this role assigned"
        )
    
    # Create new assignment
    user_role = UserRole(
        user_id=assignment.user_id,
        role_id=assignment.role_id,
        assigned_by=assignment.assigned_by or current_user.id,
        is_active=True
    )
    
    db.add(user_role)
    await db.commit()
    await db.refresh(user_role)
    
    return RoleResponse(
        success=True,
        message=f"Role '{role.name}' assigned to user successfully",
        data=None
    )


@router.delete("/assign/{assignment_id}", response_model=RoleResponse)
async def remove_role_from_user(
    assignment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Remove a role assignment from a user.
    
    Args:
        assignment_id: ID of the role assignment to remove
        db: Database session
        current_user: Currently authenticated user
        
    Returns:
        RoleResponse: Removal confirmation
        
    Raises:
        HTTPException: If assignment not found or user lacks permissions
    """
    # Check if user has permission to remove role assignments
    if not current_user.is_superuser and not current_user.has_role("admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to remove role assignments"
        )
    
    # Get existing assignment
    result = await db.execute(
        select(UserRole).where(UserRole.id == assignment_id)
    )
    assignment = result.scalar_one_or_none()
    
    if not assignment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Role assignment with ID {assignment_id} not found"
        )
    
    # Deactivate assignment instead of deleting
    assignment.is_active = False
    await db.commit()
    
    return RoleResponse(
        success=True,
        message="Role assignment removed successfully",
        data=None
    )


@router.get("/user/{user_id}/roles", response_model=UserRoleListResponse)
async def get_user_roles(
    user_id: uuid.UUID,
    active_only: bool = Query(True, description="Return only active role assignments"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all roles assigned to a specific user.
    
    Args:
        user_id: ID of the user
        active_only: Whether to return only active assignments
        db: Database session
        current_user: Currently authenticated user
        
    Returns:
        UserRoleListResponse: List of user's role assignments
        
    Raises:
        HTTPException: If user not found
    """
    # Verify user exists
    user_result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = user_result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    
    # Build query
    query = select(UserRole).options(
        selectinload(UserRole.role)
    ).where(UserRole.user_id == user_id)
    
    if active_only:
        query = query.where(UserRole.is_active == True)
    
    # Execute query
    result = await db.execute(query)
    assignments = result.scalars().all()
    
    # Convert to response format
    assignment_data = [UserRoleAssignmentResponse.from_orm(assignment) for assignment in assignments]
    
    return UserRoleListResponse(
        success=True,
        message=f"Retrieved {len(assignment_data)} role assignments for user",
        data=assignment_data,
        total=len(assignment_data)
    )


@router.get("/stats", response_model=RoleStatsResponse)
async def get_role_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get role statistics and usage information.
    
    Args:
        db: Database session
        current_user: Currently authenticated user
        
    Returns:
        RoleStatsResponse: Role statistics
        
    Raises:
        HTTPException: If user lacks permissions
    """
    # Check if user has permission to view role statistics
    if not current_user.is_superuser and not current_user.has_role("admin"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions to view role statistics"
        )
    
    # Get total roles
    total_roles_result = await db.execute(select(func.count(Role.id)))
    total_roles = total_roles_result.scalar()
    
    # Get active roles
    active_roles_result = await db.execute(
        select(func.count(Role.id)).where(Role.is_active == True)
    )
    active_roles = active_roles_result.scalar()
    
    # Get total assignments
    total_assignments_result = await db.execute(select(func.count(UserRole.id)))
    total_assignments = total_assignments_result.scalar()
    
    # Get active assignments
    active_assignments_result = await db.execute(
        select(func.count(UserRole.id)).where(UserRole.is_active == True)
    )
    active_assignments = active_assignments_result.scalar()
    
    # Get most used roles
    most_used_roles_result = await db.execute(
        select(
            Role.name,
            func.count(UserRole.id).label('assignment_count')
        )
        .join(UserRole, Role.id == UserRole.role_id)
        .where(UserRole.is_active == True)
        .group_by(Role.id, Role.name)
        .order_by(func.count(UserRole.id).desc())
        .limit(10)
    )
    most_used_roles = [
        {"role_name": row[0], "assignment_count": row[1]}
        for row in most_used_roles_result.fetchall()
    ]
    
    stats = RoleStats(
        total_roles=total_roles,
        active_roles=active_roles,
        total_assignments=total_assignments,
        active_assignments=active_assignments,
        most_used_roles=most_used_roles
    )
    
    return RoleStatsResponse(
        success=True,
        message="Role statistics retrieved successfully",
        data=stats
    )

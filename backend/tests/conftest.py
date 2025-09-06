"""
Shared test configuration and fixtures.

This file contains common test setup, fixtures, and utilities
used across all test modules.
"""
import asyncio
import os
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

# Import common test utilities
from app.db.database import get_async_session_local, init_db
from app.models import User, Role, UserRole
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
import uuid


async def clear_test_data():
    """Clear all test data from the database."""
    async with get_async_session_local()() as db:
        # Delete in reverse order of dependencies
        await db.execute(delete(UserRole))
        await db.execute(delete(Role))
        await db.execute(delete(User))
        await db.commit()


async def create_test_user(
    db: AsyncSession,
    email: str = "test@example.com",
    first_name: str = "Test",
    last_name: str = "User",
    is_superuser: bool = False
) -> User:
    """Create a test user."""
    user = User(
        id=uuid.uuid4(),
        email=email,
        hashed_password="hashed_password_123",
        first_name=first_name,
        last_name=last_name,
        is_active=True,
        is_superuser=is_superuser,
        is_verified=True
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def create_test_role(
    db: AsyncSession,
    name: str = "test_role",
    description: str = "Test role",
    permissions: list = None
) -> Role:
    """Create a test role."""
    if permissions is None:
        permissions = ["read", "write"]
    
    role = Role(
        name=name,
        description=description,
        is_active=True
    )
    role.set_permissions_list(permissions)
    
    db.add(role)
    await db.commit()
    await db.refresh(role)
    return role


async def create_test_user_role(
    db: AsyncSession,
    user: User,
    role: Role,
    assigned_by: User
) -> UserRole:
    """Create a test user role assignment."""
    user_role = UserRole(
        user_id=user.id,
        role_id=role.id,
        assigned_by=assigned_by.id,
        is_active=True
    )
    db.add(user_role)
    await db.commit()
    await db.refresh(user_role)
    return user_role

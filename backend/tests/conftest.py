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
from app.models import User, Role, UserRole, Resume, Score
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
import uuid
import pytest


async def clear_test_data():
    """Clear all test data from the database."""
    async with get_async_session_local()() as db:
        # Delete in reverse order of dependencies
        await db.execute(delete(Score))
        await db.execute(delete(Resume))
        await db.execute(delete(UserRole))
        await db.execute(delete(Role))
        await db.execute(delete(User))
        await db.commit()


@pytest.fixture
async def db():
    """Database session fixture for tests."""
    async with get_async_session_local()() as session:
        try:
            yield session
        finally:
            await session.rollback()


@pytest.fixture
async def db_session():
    """Alternative database session fixture for tests."""
    async with get_async_session_local()() as session:
        try:
            yield session
        finally:
            await session.rollback()


@pytest.fixture(autouse=True)
async def setup_test_db():
    """Setup test database before each test."""
    await init_db()
    await clear_test_data()
    yield
    await clear_test_data()


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


async def create_test_resume(
    db: AsyncSession,
    user: User,
    title: str = "Test Resume",
    file_name: str = "test_resume.pdf",
    file_size: int = 1024000,
    file_type: str = "PDF"
) -> Resume:
    """Create a test resume."""
    resume = Resume(
        user_id=user.id,
        title=title,
        file_name=file_name,
        file_size=file_size,
        file_type=file_type,
        summary="Test resume summary",
        experience_years=5.0,
        education_level="Bachelor's Degree"
    )
    resume.set_skills_list(["Python", "JavaScript", "SQL"])
    resume.set_languages_list([
        {"name": "English", "level": "Native"},
        {"name": "Spanish", "level": "Intermediate"}
    ])
    
    db.add(resume)
    await db.commit()
    await db.refresh(resume)
    return resume


async def create_test_score(
    db: AsyncSession,
    user: User,
    resume: Resume,
    analysis_type: str = "overall",
    overall_score: float = 85.5,
    skill_score: float = 80.0,
    experience_score: float = 90.0,
    education_score: float = 85.0
) -> Score:
    """Create a test score."""
    score = Score(
        user_id=user.id,
        resume_id=resume.id,
        analysis_type=analysis_type,
        overall_score=overall_score,
        skill_score=skill_score,
        experience_score=experience_score,
        education_score=education_score
    )
    score.set_skill_matches_list(["Python", "JavaScript", "SQL"])
    score.set_skill_gaps_list(["Docker", "Kubernetes"])
    score.set_analysis_details_dict({"confidence": 0.95, "model_version": "v1.2"})
    
    db.add(score)
    await db.commit()
    await db.refresh(score)
    return score

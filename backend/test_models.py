#!/usr/bin/env python3
"""
Pytest-compatible sanity tests for model imports, object construction,
and database initialization.
"""

import os
import sys
import pytest

# Add the app directory to the Python path
sys.path.append(os.path.dirname(__file__))


@pytest.mark.asyncio
async def test_model_imports():
    """Models can be imported."""
    from app.models import User, Role, UserRole, Resume, Score  # noqa: F401

    # If import fails, pytest will error. Otherwise, pass explicitly.
    assert True


@pytest.mark.asyncio
async def test_model_creation():
    """Models can be instantiated without DB round-trips."""
    from app.models import User, Role, UserRole, Resume, Score

    user = User(
        email="test@example.com",
        hashed_password="test_hash",
        first_name="Test",
        last_name="User",
    )

    role = Role(name="test_role", description="Test role")
    user_role = UserRole(user_id=user.id, role_id=role.id)
    resume = Resume(user_id=user.id, title="Test Resume")
    score = Score(
        user_id=user.id,
        resume_id=resume.id,
        analysis_type="test",
        overall_score=85.0,
    )

    assert user is not None
    assert role is not None
    assert user_role is not None
    assert resume is not None
    assert score is not None


@pytest.mark.asyncio
async def test_database_connection():
    """init_db should succeed using an in-memory SQLite database."""
    # Force SQLite in-memory for this test to avoid external dependencies
    os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

    from app.db.database import init_db

    # Should not raise
    await init_db()
    assert True

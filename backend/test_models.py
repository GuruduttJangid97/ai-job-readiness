#!/usr/bin/env python3
"""
Comprehensive Model Tests for AI Job Readiness Platform

This test suite validates the core database models and their functionality.
It includes tests for model imports, object creation, relationships, and
database initialization to ensure the data layer is working correctly.

Test Coverage:
- Model imports and basic instantiation
- Object creation with proper validation
- Model relationships and foreign keys
- Database initialization and connection
- Model utility methods and properties

Author: AI Job Readiness Team
Version: 1.0.0
"""

import os
import sys
import pytest
import uuid
from datetime import datetime

# Add the app directory to the Python path
sys.path.append(os.path.dirname(__file__))


@pytest.mark.asyncio
async def test_model_imports():
    """
    Test that all models can be imported successfully.
    
    This test ensures that all model classes are properly defined
    and can be imported without errors. It's a basic sanity check
    for the model definitions.
    """
    from app.models import User, Role, UserRole, Resume, Score  # noqa: F401

    # If import fails, pytest will error. Otherwise, pass explicitly.
    assert True


@pytest.mark.asyncio
async def test_model_creation():
    """
    Test that models can be instantiated with proper data.
    
    This test validates that all model classes can be created
    with appropriate data and that the relationships between
    models work correctly.
    """
    from app.models import User, Role, UserRole, Resume, Score

    # Create a test user with comprehensive profile data
    user = User(
        email="test@example.com",
        hashed_password="test_hash",
        first_name="Test",
        last_name="User",
        phone="+1234567890",
        bio="Test user for model validation"
    )

    # Create a test role
    role = Role(
        name="test_role", 
        description="Test role for validation",
        permissions='["read", "write"]'
    )

    # Create user-role association
    user_role = UserRole(
        user_id=user.id, 
        role_id=role.id,
        is_active=True
    )

    # Create a test resume
    resume = Resume(
        user_id=user.id, 
        title="Test Resume",
        summary="Test resume for validation",
        experience_years=5.0,
        education_level="Bachelor's Degree"
    )

    # Create a test score
    score = Score(
        user_id=user.id,
        resume_id=resume.id,
        analysis_type="test_analysis",
        overall_score=85.0,
        skill_score=80.0,
        experience_score=90.0,
        education_score=85.0,
        recommendations="Test recommendations for improvement"
    )

    # Validate all objects were created successfully
    assert user is not None
    assert role is not None
    assert user_role is not None
    assert resume is not None
    assert score is not None

    # Validate user properties
    assert user.email == "test@example.com"
    assert user.full_name == "Test User"
    assert user.display_name == "Test User"

    # Validate role properties
    assert role.name == "test_role"
    assert role.description == "Test role for validation"
    assert role.get_permissions_list() == ["read", "write"]

    # Validate resume properties
    assert resume.title == "Test Resume"
    assert resume.experience_years == 5.0
    assert resume.education_level == "Bachelor's Degree"

    # Validate score properties
    assert score.overall_score == 85.0
    assert score.get_score_grade() == "B"
    assert score.get_score_level() == "Good"


@pytest.mark.asyncio
async def test_model_utility_methods():
    """
    Test model utility methods and computed properties.
    
    This test validates that the utility methods added to models
    work correctly and provide the expected functionality.
    """
    from app.models import User, Role, Resume, Score

    # Test User utility methods
    user = User(
        email="test@example.com",
        hashed_password="test_hash",
        first_name="John",
        last_name="Doe"
    )
    
    assert user.full_name == "John Doe"
    assert user.display_name == "John Doe"
    assert not user.is_admin()  # Should be False by default

    # Test Role utility methods
    role = Role(name="admin", permissions='["admin", "user_management"]')
    role.add_permission("read")
    assert role.has_permission("admin")
    assert role.has_permission("read")
    assert not role.has_permission("write")

    # Test Resume utility methods
    resume = Resume(
        user_id=user.id,
        title="Test Resume",
        skills='["Python", "JavaScript", "React"]',
        languages='[{"name": "English", "level": "Native"}]'
    )
    
    assert resume.get_skills_list() == ["Python", "JavaScript", "React"]
    assert len(resume.get_languages_list()) == 1
    assert resume.get_languages_list()[0]["name"] == "English"

    # Test Score utility methods
    score = Score(
        user_id=user.id,
        resume_id=resume.id,
        analysis_type="test",
        overall_score=92.5
    )
    
    assert score.get_score_grade() == "A-"
    assert score.get_score_level() == "Excellent"


@pytest.mark.asyncio
async def test_database_connection():
    """
    Test database initialization and connection.
    
    This test validates that the database can be initialized
    successfully using an in-memory SQLite database for testing.
    """
    # Force SQLite in-memory for this test to avoid external dependencies
    os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

    from app.db.database import init_db, check_db_connection

    # Test database initialization
    await init_db()
    assert True

    # Test database connection
    is_connected = await check_db_connection()
    assert is_connected is True


@pytest.mark.asyncio
async def test_model_relationships():
    """
    Test model relationships and foreign key constraints.
    
    This test validates that the relationships between models
    are properly defined and work as expected.
    """
    from app.models import User, Role, UserRole, Resume, Score

    # Create related objects
    user = User(
        email="relationship@test.com",
        hashed_password="test_hash",
        first_name="Relationship",
        last_name="Test"
    )

    role = Role(name="tester", description="Test role")
    user_role = UserRole(user_id=user.id, role_id=role.id)
    
    resume = Resume(user_id=user.id, title="Relationship Test Resume")
    score = Score(
        user_id=user.id,
        resume_id=resume.id,
        analysis_type="relationship_test",
        overall_score=75.0
    )

    # Validate relationships
    assert user_role.user_id == user.id
    assert user_role.role_id == role.id
    assert resume.user_id == user.id
    assert score.user_id == user.id
    assert score.resume_id == resume.id


@pytest.mark.asyncio
async def test_model_serialization():
    """
    Test model serialization to dictionary format.
    
    This test validates that models can be properly serialized
    to dictionary format for API responses.
    """
    from app.models import User, Role, Resume, Score

    # Create test objects
    user = User(
        email="serialize@test.com",
        hashed_password="test_hash",
        first_name="Serialize",
        last_name="Test"
    )

    role = Role(name="serializer", description="Serialization test role")
    resume = Resume(user_id=user.id, title="Serialization Test Resume")
    score = Score(
        user_id=user.id,
        resume_id=resume.id,
        analysis_type="serialization_test",
        overall_score=88.0
    )

    # Test serialization
    user_dict = user.to_dict()
    role_dict = role.to_dict()
    resume_dict = resume.to_dict()
    score_dict = score.to_dict()

    # Validate serialization
    assert isinstance(user_dict, dict)
    assert isinstance(role_dict, dict)
    assert isinstance(resume_dict, dict)
    assert isinstance(score_dict, dict)

    # Validate key fields are present
    assert "id" in user_dict
    assert "email" in user_dict
    assert "full_name" in user_dict
    assert "name" in role_dict
    assert "title" in resume_dict
    assert "overall_score" in score_dict

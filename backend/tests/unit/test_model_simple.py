"""
Simple unit tests for model creation and basic functionality.

This module tests the creation of all database models without complex
fixture dependencies to verify basic functionality.

Author: AI Job Readiness Team
Version: 1.0.0
"""

import pytest
import uuid
from datetime import datetime

from app.models.user import User
from app.models.role import Role, UserRole
from app.models.resume import Resume
from app.models.score import Score


class TestSimpleModelCreation:
    """Test simple model creation without database dependencies."""
    
    def test_user_creation(self):
        """Test creating a user."""
        user = User(
            email="test@example.com",
            hashed_password="hashed_password_123",
            is_active=True,
            is_superuser=False,
            is_verified=True
        )
        
        assert user.email == "test@example.com"
        assert user.hashed_password == "hashed_password_123"
        assert user.is_active is True
        assert user.is_superuser is False
        assert user.is_verified is True
        assert user.id is None  # Not saved to database yet
    
    def test_role_creation(self):
        """Test creating a role."""
        role = Role(
            name="test_role",
            description="Test role",
            is_active=True
        )
        role.set_permissions_list(["read", "write"])
        
        assert role.name == "test_role"
        assert role.description == "Test role"
        assert role.is_active is True
        assert role.get_permissions_list() == ["read", "write"]
        assert role.id is None  # Not saved to database yet
    
    def test_user_role_creation(self):
        """Test creating a user role assignment."""
        user_id = uuid.uuid4()
        role_id = 1
        
        user_role = UserRole(
            user_id=user_id,
            role_id=role_id,
            is_active=True
        )
        
        assert user_role.user_id == user_id
        assert user_role.role_id == role_id
        assert user_role.is_active is True
        assert user_role.id is None  # Not saved to database yet
    
    def test_resume_creation(self):
        """Test creating a resume."""
        user_id = uuid.uuid4()
        
        resume = Resume(
            user_id=user_id,
            title="Test Resume",
            file_name="test_resume.pdf",
            file_size=1024000,
            file_type="PDF"
        )
        resume.set_skills_list(["Python", "JavaScript"])
        resume.set_languages_list([
            {"name": "English", "level": "Native"}
        ])
        
        assert resume.user_id == user_id
        assert resume.title == "Test Resume"
        assert resume.file_name == "test_resume.pdf"
        assert resume.file_size == 1024000
        assert resume.file_type == "PDF"
        assert resume.get_skills_list() == ["Python", "JavaScript"]
        assert len(resume.get_languages_list()) == 1
        assert resume.id is None  # Not saved to database yet
    
    def test_score_creation(self):
        """Test creating a score."""
        user_id = uuid.uuid4()
        
        score = Score(
            user_id=user_id,
            resume_id=1,
            analysis_type="overall",
            overall_score=85.5,
            skill_score=80.0,
            experience_score=90.0
        )
        score.set_skill_matches_list(["Python", "JavaScript"])
        score.set_skill_gaps_list(["Docker"])
        
        assert score.user_id == user_id
        assert score.resume_id == 1
        assert score.analysis_type == "overall"
        assert score.overall_score == 85.5
        assert score.skill_score == 80.0
        assert score.experience_score == 90.0
        assert score.get_skill_matches_list() == ["Python", "JavaScript"]
        assert score.get_skill_gaps_list() == ["Docker"]
        assert score.id is None  # Not saved to database yet


class TestModelMethods:
    """Test model methods and properties."""
    
    def test_user_methods(self):
        """Test user methods."""
        user = User(
            email="test@example.com",
            hashed_password="hashed_password_123",
            first_name="John",
            last_name="Doe",
            is_active=True,
            is_superuser=False,
            is_verified=True
        )
        
        # Test string representations
        assert str(user) == "John Doe"
        assert "User" in repr(user)
        assert "test@example.com" in repr(user)
        
        # Test properties
        assert user.full_name == "John Doe"
        assert user.display_name == "John Doe"
        
        # Test role methods (empty initially)
        assert user.get_role_names() == []
        assert user.has_role("admin") is False
        assert user.is_admin() is False
        
        # Test admin check with superuser
        user.is_superuser = True
        assert user.is_admin() is True
    
    def test_role_methods(self):
        """Test role methods."""
        role = Role(
            name="admin",
            description="Administrator role",
            is_active=True
        )
        
        # Test string representations
        assert str(role) == "admin"
        assert "Role" in repr(role)
        assert "admin" in repr(role)
        
        # Test permission methods
        role.set_permissions_list(["read", "write", "delete"])
        assert role.get_permissions_list() == ["read", "write", "delete"]
        assert role.has_permission("read") is True
        assert role.has_permission("admin") is False
        
        # Test adding permission
        role.add_permission("admin")
        assert role.has_permission("admin") is True
        assert "admin" in role.get_permissions_list()
        
        # Test removing permission
        role.remove_permission("read")
        assert role.has_permission("read") is False
        assert "read" not in role.get_permissions_list()
    
    def test_resume_methods(self):
        """Test resume methods."""
        user_id = uuid.uuid4()
        resume = Resume(
            user_id=user_id,
            title="Test Resume",
            file_size=1024000
        )
        
        # Test string representations
        assert str(resume) == "Test Resume"
        assert "Resume" in repr(resume)
        assert "Test Resume" in repr(resume)
        
        # Test file size methods
        assert abs(resume.get_file_size_mb() - 1.0) < 0.1  # Allow for rounding
        
        # Test skills methods
        resume.set_skills_list(["Python", "JavaScript"])
        assert resume.get_skills_list() == ["Python", "JavaScript"]
        
        # Test languages methods
        languages = [{"name": "English", "level": "Native"}]
        resume.set_languages_list(languages)
        assert resume.get_languages_list() == languages
        
        # Test analysis methods
        assert resume.needs_analysis() is True  # No last_analyzed set
        resume.last_analyzed = datetime.utcnow()
        assert resume.needs_analysis() is False
    
    def test_score_methods(self):
        """Test score methods."""
        user_id = uuid.uuid4()
        score = Score(
            user_id=user_id,
            resume_id=1,
            analysis_type="overall",
            overall_score=85.5
        )
        
        # Test string representations
        assert "Score 85.5/100 for overall" in str(score)
        assert "Score" in repr(score)
        assert "85.5" in repr(score)
        
        # Test skill methods
        score.set_skill_matches_list(["Python", "JavaScript"])
        score.set_skill_gaps_list(["Docker"])
        assert score.get_skill_matches_list() == ["Python", "JavaScript"]
        assert score.get_skill_gaps_list() == ["Docker"]
        
        # Test analysis details methods
        details = {"confidence": 0.95}
        score.set_analysis_details_dict(details)
        assert score.get_analysis_details_dict() == details
        
        # Test grade methods
        assert score.get_score_grade() == "B"
        assert score.get_score_level() == "Excellent"  # 85.5 is >= 85
        
        # Test recent analysis
        score.analysis_date = datetime.utcnow()
        assert score.is_recent_analysis() is True


class TestModelToDict:
    """Test model to_dict methods."""
    
    def test_user_to_dict(self):
        """Test user to_dict method."""
        user = User(
            email="test@example.com",
            hashed_password="hashed_password_123",
            first_name="John",
            last_name="Doe",
            phone="+1234567890",
            bio="Test bio",
            is_active=True,
            is_superuser=False,
            is_verified=True
        )
        
        user_dict = user.to_dict()
        
        assert user_dict["email"] == "test@example.com"
        assert user_dict["first_name"] == "John"
        assert user_dict["last_name"] == "Doe"
        assert user_dict["full_name"] == "John Doe"
        assert user_dict["phone"] == "+1234567890"
        assert user_dict["bio"] == "Test bio"
        assert user_dict["is_active"] is True
        assert user_dict["is_superuser"] is False
        assert user_dict["is_verified"] is True
        assert "id" in user_dict
        assert "created_at" in user_dict
        assert "roles" in user_dict
    
    def test_role_to_dict(self):
        """Test role to_dict method."""
        role = Role(
            name="admin",
            description="Administrator role",
            is_active=True
        )
        role.set_permissions_list(["read", "write", "delete"])
        
        role_dict = role.to_dict()
        
        assert role_dict["name"] == "admin"
        assert role_dict["description"] == "Administrator role"
        assert role_dict["permissions"] == ["read", "write", "delete"]
        assert role_dict["is_active"] is True
        assert "id" in role_dict
        assert "created_at" in role_dict
    
    def test_resume_to_dict(self):
        """Test resume to_dict method."""
        user_id = uuid.uuid4()
        resume = Resume(
            user_id=user_id,
            title="Test Resume",
            file_name="test_resume.pdf",
            file_size=1024000,
            summary="Test summary"
        )
        resume.set_skills_list(["Python", "JavaScript"])
        
        resume_dict = resume.to_dict()
        
        assert resume_dict["user_id"] == str(user_id)
        assert resume_dict["title"] == "Test Resume"
        assert resume_dict["file_name"] == "test_resume.pdf"
        assert resume_dict["file_size"] == 1024000
        assert abs(resume_dict["file_size_mb"] - 1.0) < 0.1  # Allow for rounding
        assert resume_dict["summary"] == "Test summary"
        assert resume_dict["skills"] == ["Python", "JavaScript"]
        assert "id" in resume_dict
        assert "created_at" in resume_dict
        assert "needs_analysis" in resume_dict
    
    def test_score_to_dict(self):
        """Test score to_dict method."""
        user_id = uuid.uuid4()
        score = Score(
            user_id=user_id,
            resume_id=1,
            analysis_type="job_match",
            overall_score=85.5,
            skill_score=80.0
        )
        score.set_skill_matches_list(["Python", "JavaScript"])
        score.set_skill_gaps_list(["Docker"])
        
        score_dict = score.to_dict()
        
        assert score_dict["user_id"] == str(user_id)
        assert score_dict["resume_id"] == 1
        assert score_dict["analysis_type"] == "job_match"
        assert score_dict["overall_score"] == 85.5
        assert score_dict["skill_score"] == 80.0
        assert score_dict["skill_matches"] == ["Python", "JavaScript"]
        assert score_dict["skill_gaps"] == ["Docker"]
        assert "id" in score_dict
        assert "created_at" in score_dict
        assert "grade" in score_dict
        assert "level" in score_dict
        assert "is_recent" in score_dict

"""
Unit tests for model creation and basic functionality.

This module tests the creation of all database models and verifies
that they can be instantiated correctly with proper field validation.

Author: AI Job Readiness Team
Version: 1.0.0
"""

import pytest
import uuid
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.models.role import Role, UserRole
from app.models.resume import Resume
from app.models.score import Score


class TestUserModelCreation:
    """Test User model creation and basic functionality."""
    
    def test_user_creation_with_minimal_data(self):
        """Test creating a user with only required fields."""
        user = User(
            email="test@example.com",
            hashed_password="hashed_password_123",
            is_active=True,
            is_superuser=False,
            is_verified=False
        )
        
        assert user.email == "test@example.com"
        assert user.hashed_password == "hashed_password_123"
        assert user.is_active is True
        assert user.is_superuser is False
        assert user.is_verified is False
        # Note: ID is None until saved to database
        assert user.id is None
    
    def test_user_creation_with_all_fields(self):
        """Test creating a user with all optional fields."""
        user = User(
            email="complete@example.com",
            hashed_password="hashed_password_123",
            first_name="John",
            last_name="Doe",
            phone="+1234567890",
            bio="Software engineer with 5 years experience",
            profile_picture_url="https://example.com/profile.jpg",
            is_active=True,
            is_superuser=True,
            is_verified=True
        )
        
        assert user.email == "complete@example.com"
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.phone == "+1234567890"
        assert user.bio == "Software engineer with 5 years experience"
        assert user.profile_picture_url == "https://example.com/profile.jpg"
        assert user.is_active is True
        assert user.is_superuser is True
        assert user.is_verified is True
    
    def test_user_string_representations(self):
        """Test user string representations."""
        user = User(
            email="test@example.com",
            hashed_password="hashed_password_123",
            first_name="Jane",
            last_name="Smith",
            is_active=True,
            is_superuser=False,
            is_verified=True
        )
        
        # Test __repr__
        repr_str = repr(user)
        assert "User" in repr_str
        assert "test@example.com" in repr_str
        
        # Test __str__
        str_result = str(user)
        assert str_result == "Jane Smith"
        
        # Test with only first name
        user.first_name = "John"
        user.last_name = None
        assert str(user) == "John"
        
        # Test with no names
        user.first_name = None
        assert str(user) == "test@example.com"
    
    def test_user_properties(self):
        """Test user properties and methods."""
        user = User(
            email="test@example.com",
            hashed_password="hashed_password_123",
            first_name="Alice",
            last_name="Johnson",
            is_active=True,
            is_superuser=False,
            is_verified=True
        )
        
        # Test full_name property
        assert user.full_name == "Alice Johnson"
        
        # Test display_name property
        assert user.display_name == "Alice Johnson"
        
        # Test with partial name
        user.last_name = None
        assert user.full_name == "Alice"
        assert user.display_name == "Alice"
        
        # Test with no names
        user.first_name = None
        assert user.full_name == "test@example.com"
        assert user.display_name == "test@example.com"
    
    def test_user_role_methods(self):
        """Test user role-related methods."""
        user = User(
            email="test@example.com",
            hashed_password="hashed_password_123",
            is_active=True,
            is_superuser=False,
            is_verified=True
        )
        
        # Test empty role methods
        assert user.get_role_names() == []
        assert user.has_role("admin") is False
        assert user.is_admin() is False
        
        # Test superuser admin check
        user.is_superuser = True
        assert user.is_admin() is True
    
    def test_user_to_dict(self):
        """Test user to_dict method."""
        user = User(
            email="test@example.com",
            hashed_password="hashed_password_123",
            first_name="Test",
            last_name="User",
            phone="+1234567890",
            bio="Test bio",
            is_active=True,
            is_superuser=False,
            is_verified=True
        )
        
        user_dict = user.to_dict()
        
        assert user_dict["email"] == "test@example.com"
        assert user_dict["first_name"] == "Test"
        assert user_dict["last_name"] == "User"
        assert user_dict["full_name"] == "Test User"
        assert user_dict["phone"] == "+1234567890"
        assert user_dict["bio"] == "Test bio"
        assert user_dict["is_active"] is True
        assert user_dict["is_superuser"] is False
        assert user_dict["is_verified"] is True
        assert "id" in user_dict
        assert "created_at" in user_dict
        assert "roles" in user_dict


class TestRoleModelCreation:
    """Test Role model creation and basic functionality."""
    
    def test_role_creation_with_minimal_data(self):
        """Test creating a role with only required fields."""
        role = Role(
            name="test_role",
            is_active=True
        )
        
        assert role.name == "test_role"
        assert role.is_active is True
        assert role.id is None  # Will be set by database
        assert role.description is None
        assert role.permissions is None
    
    def test_role_creation_with_all_fields(self):
        """Test creating a role with all fields."""
        role = Role(
            name="admin",
            description="Administrator role with full access",
            permissions='["read", "write", "delete"]',
            is_active=True
        )
        
        assert role.name == "admin"
        assert role.description == "Administrator role with full access"
        assert role.permissions == '["read", "write", "delete"]'
        assert role.is_active is True
    
    def test_role_string_representations(self):
        """Test role string representations."""
        role = Role(
            name="moderator",
            description="Moderator role",
            is_active=True
        )
        
        # Test __repr__
        repr_str = repr(role)
        assert "Role" in repr_str
        assert "moderator" in repr_str
        
        # Test __str__
        assert str(role) == "moderator"
    
    def test_role_permissions_methods(self):
        """Test role permission management methods."""
        role = Role(
            name="test_role",
            is_active=True
        )
        
        # Test empty permissions
        assert role.get_permissions_list() == []
        assert role.has_permission("read") is False
        
        # Test setting permissions
        permissions = ["read", "write", "delete"]
        role.set_permissions_list(permissions)
        assert role.get_permissions_list() == permissions
        assert role.has_permission("read") is True
        assert role.has_permission("write") is True
        assert role.has_permission("admin") is False
        
        # Test adding permission
        role.add_permission("admin")
        assert role.has_permission("admin") is True
        assert "admin" in role.get_permissions_list()
        
        # Test removing permission
        role.remove_permission("read")
        assert role.has_permission("read") is False
        assert "read" not in role.get_permissions_list()
        
        # Test adding duplicate permission
        role.add_permission("admin")
        permissions_list = role.get_permissions_list()
        assert permissions_list.count("admin") == 1  # Should not duplicate
    
    def test_role_permissions_json_handling(self):
        """Test role permissions JSON serialization/deserialization."""
        role = Role(
            name="test_role",
            is_active=True
        )
        
        # Test with valid JSON
        role.permissions = '["read", "write"]'
        assert role.get_permissions_list() == ["read", "write"]
        
        # Test with invalid JSON
        role.permissions = "invalid json"
        assert role.get_permissions_list() == []
        
        # Test with None
        role.permissions = None
        assert role.get_permissions_list() == []
        
        # Test with empty string
        role.permissions = ""
        assert role.get_permissions_list() == []
    
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


class TestUserRoleModelCreation:
    """Test UserRole model creation and basic functionality."""
    
    def test_user_role_creation(self):
        """Test creating a user role assignment."""
        user_id = uuid.uuid4()
        role_id = 1
        assigned_by = uuid.uuid4()
        
        user_role = UserRole(
            user_id=user_id,
            role_id=role_id,
            assigned_by=assigned_by,
            is_active=True
        )
        
        assert user_role.user_id == user_id
        assert user_role.role_id == role_id
        assert user_role.assigned_by == assigned_by
        assert user_role.is_active is True
        assert user_role.id is None  # Will be set by database
    
    def test_user_role_creation_without_assigned_by(self):
        """Test creating a user role assignment without assigned_by."""
        user_id = uuid.uuid4()
        role_id = 1
        
        user_role = UserRole(
            user_id=user_id,
            role_id=role_id,
            is_active=True
        )
        
        assert user_role.user_id == user_id
        assert user_role.role_id == role_id
        assert user_role.assigned_by is None
        assert user_role.is_active is True
    
    def test_user_role_string_representations(self):
        """Test user role string representations."""
        user_id = uuid.uuid4()
        role_id = 1
        
        user_role = UserRole(
            user_id=user_id,
            role_id=role_id,
            is_active=True
        )
        
        # Test __repr__
        repr_str = repr(user_role)
        assert "UserRole" in repr_str
        assert str(user_id) in repr_str
        assert str(role_id) in repr_str
        
        # Test __str__
        str_result = str(user_role)
        assert "User" in str_result
        assert str(user_id) in str_result
        assert str(role_id) in str_result
    
    def test_user_role_expiration_methods(self):
        """Test user role expiration methods."""
        user_id = uuid.uuid4()
        role_id = 1
        
        user_role = UserRole(
            user_id=user_id,
            role_id=role_id,
            is_active=True
        )
        
        # Test is_expired (currently always returns False)
        assert user_role.is_expired() is False
    
    def test_user_role_to_dict(self):
        """Test user role to_dict method."""
        user_id = uuid.uuid4()
        role_id = 1
        assigned_by = uuid.uuid4()
        
        user_role = UserRole(
            user_id=user_id,
            role_id=role_id,
            assigned_by=assigned_by,
            is_active=True
        )
        
        user_role_dict = user_role.to_dict()
        
        assert user_role_dict["user_id"] == str(user_id)
        assert user_role_dict["role_id"] == role_id
        assert user_role_dict["assigned_by"] == str(assigned_by)
        assert user_role_dict["is_active"] is True
        assert "id" in user_role_dict
        assert "assigned_at" in user_role_dict
        assert "is_expired" in user_role_dict


class TestResumeModelCreation:
    """Test Resume model creation and basic functionality."""
    
    def test_resume_creation_with_minimal_data(self):
        """Test creating a resume with only required fields."""
        user_id = uuid.uuid4()
        
        resume = Resume(
            user_id=user_id,
            title="My Resume"
        )
        
        assert resume.user_id == user_id
        assert resume.title == "My Resume"
        assert resume.id is None  # Will be set by database
        # Note: Default values are set by SQLAlchemy, not Python
        assert resume.is_active is None  # Will be set by database
        assert resume.is_public is None  # Will be set by database
    
    def test_resume_creation_with_all_fields(self):
        """Test creating a resume with all fields."""
        user_id = uuid.uuid4()
        
        resume = Resume(
            user_id=user_id,
            title="Complete Resume",
            file_path="/uploads/resume.pdf",
            file_name="resume.pdf",
            file_size=1024000,
            file_type="PDF",
            summary="Experienced software engineer",
            experience_years=5.5,
            education_level="Bachelor's Degree",
            skills='["Python", "JavaScript", "SQL"]',
            languages='[{"name": "English", "level": "Native"}]',
            is_active=True,
            is_public=True
        )
        
        assert resume.user_id == user_id
        assert resume.title == "Complete Resume"
        assert resume.file_path == "/uploads/resume.pdf"
        assert resume.file_name == "resume.pdf"
        assert resume.file_size == 1024000
        assert resume.file_type == "PDF"
        assert resume.summary == "Experienced software engineer"
        assert resume.experience_years == 5.5
        assert resume.education_level == "Bachelor's Degree"
        assert resume.skills == '["Python", "JavaScript", "SQL"]'
        assert resume.languages == '[{"name": "English", "level": "Native"}]'
        assert resume.is_active is True
        assert resume.is_public is True
    
    def test_resume_string_representations(self):
        """Test resume string representations."""
        user_id = uuid.uuid4()
        
        resume = Resume(
            user_id=user_id,
            title="Test Resume"
        )
        
        # Test __repr__
        repr_str = repr(resume)
        assert "Resume" in repr_str
        assert "Test Resume" in repr_str
        assert str(user_id) in repr_str
        
        # Test __str__
        assert str(resume) == "Test Resume"
        
        # Test with file_name but no title
        resume.title = None
        resume.file_name = "resume.pdf"
        assert str(resume) == "resume.pdf"
        
        # Test with neither title nor file_name
        resume.file_name = None
        assert "Resume" in str(resume)
    
    def test_resume_skills_methods(self):
        """Test resume skills management methods."""
        user_id = uuid.uuid4()
        resume = Resume(
            user_id=user_id,
            title="Test Resume"
        )
        
        # Test empty skills
        assert resume.get_skills_list() == []
        
        # Test setting skills
        skills = ["Python", "JavaScript", "SQL"]
        resume.set_skills_list(skills)
        assert resume.get_skills_list() == skills
        
        # Test with invalid JSON
        resume.skills = "invalid json"
        assert resume.get_skills_list() == []
        
        # Test with None
        resume.skills = None
        assert resume.get_skills_list() == []
    
    def test_resume_languages_methods(self):
        """Test resume languages management methods."""
        user_id = uuid.uuid4()
        resume = Resume(
            user_id=user_id,
            title="Test Resume"
        )
        
        # Test empty languages
        assert resume.get_languages_list() == []
        
        # Test setting languages
        languages = [
            {"name": "English", "level": "Native"},
            {"name": "Spanish", "level": "Intermediate"}
        ]
        resume.set_languages_list(languages)
        assert resume.get_languages_list() == languages
        
        # Test with invalid JSON
        resume.languages = "invalid json"
        assert resume.get_languages_list() == []
        
        # Test with None
        resume.languages = None
        assert resume.get_languages_list() == []
    
    def test_resume_file_size_methods(self):
        """Test resume file size methods."""
        user_id = uuid.uuid4()
        resume = Resume(
            user_id=user_id,
            title="Test Resume"
        )
        
        # Test with no file size
        assert resume.get_file_size_mb() is None
        
        # Test with file size
        resume.file_size = 1024000  # 1MB in bytes
        assert abs(resume.get_file_size_mb() - 1.0) < 0.1  # Allow for rounding
        
        # Test with different file size
        resume.file_size = 1536000  # 1.5MB in bytes
        assert abs(resume.get_file_size_mb() - 1.5) < 0.1  # Allow for rounding
    
    def test_resume_analysis_methods(self):
        """Test resume analysis methods."""
        user_id = uuid.uuid4()
        resume = Resume(
            user_id=user_id,
            title="Test Resume"
        )
        
        # Test needs_analysis with no last_analyzed
        assert resume.needs_analysis() is True
        assert resume.needs_analysis_property is True
        
        # Test needs_analysis with recent analysis
        resume.last_analyzed = datetime.utcnow()
        assert resume.needs_analysis() is False
        assert resume.needs_analysis_property is False
        
        # Test is_recently_analyzed
        assert resume.is_recently_analyzed() is True
        assert resume.is_recently_analyzed(1) is True  # Within 1 hour
    
    def test_resume_to_dict(self):
        """Test resume to_dict method."""
        user_id = uuid.uuid4()
        resume = Resume(
            user_id=user_id,
            title="Test Resume",
            file_name="resume.pdf",
            file_size=1024000,
            summary="Test summary"
        )
        resume.set_skills_list(["Python", "JavaScript"])
        
        resume_dict = resume.to_dict()
        
        assert resume_dict["user_id"] == str(user_id)
        assert resume_dict["title"] == "Test Resume"
        assert resume_dict["file_name"] == "resume.pdf"
        assert resume_dict["file_size"] == 1024000
        assert abs(resume_dict["file_size_mb"] - 1.0) < 0.1  # Allow for rounding
        assert resume_dict["summary"] == "Test summary"
        assert resume_dict["skills"] == ["Python", "JavaScript"]
        # Note: is_active and is_public will be set by database defaults
        assert "is_active" in resume_dict
        assert "is_public" in resume_dict
        assert "id" in resume_dict
        assert "created_at" in resume_dict
        assert "needs_analysis" in resume_dict


class TestScoreModelCreation:
    """Test Score model creation and basic functionality."""
    
    def test_score_creation_with_minimal_data(self):
        """Test creating a score with only required fields."""
        user_id = uuid.uuid4()
        
        score = Score(
            user_id=user_id,
            resume_id=1,
            analysis_type="overall",
            overall_score=85.5
        )
        
        assert score.user_id == user_id
        assert score.resume_id == 1
        assert score.analysis_type == "overall"
        assert score.overall_score == 85.5
        assert score.id is None  # Will be set by database
        # Note: Default values are set by SQLAlchemy, not Python
        assert score.is_active is None  # Will be set by database
    
    def test_score_creation_with_all_fields(self):
        """Test creating a score with all fields."""
        user_id = uuid.uuid4()
        
        score = Score(
            user_id=user_id,
            resume_id=1,
            analysis_type="job_match",
            job_title="Software Engineer",
            company="Tech Corp",
            overall_score=92.5,
            skill_score=88.0,
            experience_score=95.0,
            education_score=90.0,
            skill_matches='["Python", "JavaScript"]',
            skill_gaps='["Docker", "Kubernetes"]',
            recommendations="Consider learning containerization technologies",
            analysis_details='{"confidence": 0.95}',
            is_active=True
        )
        
        assert score.user_id == user_id
        assert score.resume_id == 1
        assert score.analysis_type == "job_match"
        assert score.job_title == "Software Engineer"
        assert score.company == "Tech Corp"
        assert score.overall_score == 92.5
        assert score.skill_score == 88.0
        assert score.experience_score == 95.0
        assert score.education_score == 90.0
        assert score.skill_matches == '["Python", "JavaScript"]'
        assert score.skill_gaps == '["Docker", "Kubernetes"]'
        assert score.recommendations == "Consider learning containerization technologies"
        assert score.analysis_details == '{"confidence": 0.95}'
        assert score.is_active is True
    
    def test_score_string_representations(self):
        """Test score string representations."""
        user_id = uuid.uuid4()
        
        score = Score(
            user_id=user_id,
            resume_id=1,
            analysis_type="overall",
            overall_score=85.5
        )
        
        # Test __repr__
        repr_str = repr(score)
        assert "Score" in repr_str
        assert "85.5" in repr_str
        assert "overall" in repr_str
        assert str(user_id) in repr_str
        
        # Test __str__
        str_result = str(score)
        assert "Score 85.5/100 for overall" in str_result
    
    def test_score_skill_methods(self):
        """Test score skill management methods."""
        user_id = uuid.uuid4()
        score = Score(
            user_id=user_id,
            resume_id=1,
            analysis_type="overall",
            overall_score=85.5
        )
        
        # Test empty skill matches
        assert score.get_skill_matches_list() == []
        assert score.get_skill_gaps_list() == []
        
        # Test setting skill matches
        skill_matches = ["Python", "JavaScript", "SQL"]
        score.set_skill_matches_list(skill_matches)
        assert score.get_skill_matches_list() == skill_matches
        
        # Test setting skill gaps
        skill_gaps = ["Docker", "Kubernetes"]
        score.set_skill_gaps_list(skill_gaps)
        assert score.get_skill_gaps_list() == skill_gaps
        
        # Test with invalid JSON
        score.skill_matches = "invalid json"
        assert score.get_skill_matches_list() == []
        
        # Test with None
        score.skill_matches = None
        assert score.get_skill_matches_list() == []
    
    def test_score_analysis_details_methods(self):
        """Test score analysis details methods."""
        user_id = uuid.uuid4()
        score = Score(
            user_id=user_id,
            resume_id=1,
            analysis_type="overall",
            overall_score=85.5
        )
        
        # Test empty analysis details
        assert score.get_analysis_details_dict() == {}
        
        # Test setting analysis details
        details = {"confidence": 0.95, "model_version": "v1.2"}
        score.set_analysis_details_dict(details)
        assert score.get_analysis_details_dict() == details
        
        # Test with invalid JSON
        score.analysis_details = "invalid json"
        assert score.get_analysis_details_dict() == {}
        
        # Test with None
        score.analysis_details = None
        assert score.get_analysis_details_dict() == {}
    
    def test_score_grade_methods(self):
        """Test score grade and level methods."""
        # Test A+ grade
        score = Score(
            user_id=uuid.uuid4(),
            resume_id=1,
            analysis_type="overall",
            overall_score=98.0
        )
        assert score.get_score_grade() == "A+"
        assert score.get_score_level() == "Excellent"
        
        # Test A grade
        score.overall_score = 95.0
        assert score.get_score_grade() == "A"
        assert score.get_score_level() == "Excellent"
        
        # Test B grade
        score.overall_score = 85.0
        assert score.get_score_grade() == "B"
        assert score.get_score_level() == "Excellent"
        
        # Test C grade
        score.overall_score = 75.0
        assert score.get_score_grade() == "C"
        assert score.get_score_level() == "Good"
        
        # Test F grade
        score.overall_score = 30.0
        assert score.get_score_grade() == "F"
        assert score.get_score_level() == "Poor"
    
    def test_score_recent_analysis_method(self):
        """Test score recent analysis method."""
        user_id = uuid.uuid4()
        score = Score(
            user_id=user_id,
            resume_id=1,
            analysis_type="overall",
            overall_score=85.5
        )
        
        # Test with recent analysis date
        score.analysis_date = datetime.utcnow()
        assert score.is_recent_analysis() is True
        assert score.is_recent_analysis(30) is True  # Within 30 days
        
        # Test with no analysis date
        score.analysis_date = None
        assert score.is_recent_analysis() is False
    
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
        # Note: is_active will be set by database defaults
        assert "is_active" in score_dict
        assert "id" in score_dict
        assert "created_at" in score_dict
        assert "grade" in score_dict
        assert "level" in score_dict
        assert "is_recent" in score_dict

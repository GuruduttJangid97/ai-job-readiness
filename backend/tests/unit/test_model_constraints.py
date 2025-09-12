"""
Unit tests for model constraints and database integrity.

This module tests database constraints, unique constraints, foreign key
constraints, and data validation rules.

Author: AI Job Readiness Team
Version: 1.0.0
"""

import pytest
import uuid
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.user import User
from app.models.role import Role, UserRole
from app.models.resume import Resume
from app.models.score import Score


class TestUserConstraints:
    """Test User model constraints and validation."""
    
    @pytest.mark.asyncio
    async def test_user_email_unique_constraint(self, db):
        """Test that user email must be unique."""
        # Create first user
        user1 = User(
            email="test@example.com",
            hashed_password="hashed_password_123",
            is_active=True,
            is_superuser=False,
            is_verified=True
        )
        db.add(user1)
        await db.commit()
        await db.refresh(user1)
        
        # Try to create second user with same email
        user2 = User(
            email="test@example.com",  # Same email
            hashed_password="hashed_password_456",
            is_active=True,
            is_superuser=False,
            is_verified=True
        )
        db.add(user2)
        
        # Should raise IntegrityError due to unique constraint
        with pytest.raises(IntegrityError):
            await db.commit()
    
    @pytest.mark.asyncio
    async def test_user_email_required(self, db):
        """Test that user email is required."""
        user = User(
            email=None,  # No email
            hashed_password="hashed_password_123",
            is_active=True,
            is_superuser=False,
            is_verified=True
        )
        db.add(user)
        
        # Should raise IntegrityError due to NOT NULL constraint
        with pytest.raises(IntegrityError):
            await db.commit()
    
    @pytest.mark.asyncio
    async def test_user_hashed_password_required(self, db):
        """Test that user hashed_password is required."""
        user = User(
            email="test@example.com",
            hashed_password=None,  # No password
            is_active=True,
            is_superuser=False,
            is_verified=True
        )
        db.add(user)
        
        # Should raise IntegrityError due to NOT NULL constraint
        with pytest.raises(IntegrityError):
            await db.commit()
    
    @pytest.mark.asyncio
    async def test_user_boolean_field_defaults(self, db):
        """Test that boolean fields have correct defaults."""
        user = User(
            email="test@example.com",
            hashed_password="hashed_password_123"
            # Not setting boolean fields to test defaults
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        # Check default values
        assert user.is_active is True  # Default from FastAPI-Users
        assert user.is_superuser is False  # Default from FastAPI-Users
        assert user.is_verified is False  # Default from FastAPI-Users
    
    @pytest.mark.asyncio
    async def test_user_optional_fields_can_be_null(self, db):
        """Test that optional fields can be null."""
        user = User(
            email="test@example.com",
            hashed_password="hashed_password_123",
            first_name=None,
            last_name=None,
            phone=None,
            bio=None,
            profile_picture_url=None
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        # Should succeed with null optional fields
        assert user.first_name is None
        assert user.last_name is None
        assert user.phone is None
        assert user.bio is None
        assert user.profile_picture_url is None


class TestRoleConstraints:
    """Test Role model constraints and validation."""
    
    @pytest.mark.asyncio
    async def test_role_name_unique_constraint(self, db):
        """Test that role name must be unique."""
        # Create first role
        role1 = Role(
            name="admin",
            description="Administrator role",
            is_active=True
        )
        db.add(role1)
        await db.commit()
        await db.refresh(role1)
        
        # Try to create second role with same name
        role2 = Role(
            name="admin",  # Same name
            description="Another admin role",
            is_active=True
        )
        db.add(role2)
        
        # Should raise IntegrityError due to unique constraint
        with pytest.raises(IntegrityError):
            await db.commit()
    
    @pytest.mark.asyncio
    async def test_role_name_required(self, db):
        """Test that role name is required."""
        role = Role(
            name=None,  # No name
            description="Test role",
            is_active=True
        )
        db.add(role)
        
        # Should raise IntegrityError due to NOT NULL constraint
        with pytest.raises(IntegrityError):
            await db.commit()
    
    @pytest.mark.asyncio
    async def test_role_boolean_field_defaults(self, db):
        """Test that boolean fields have correct defaults."""
        role = Role(
            name="test_role"
            # Not setting is_active to test default
        )
        db.add(role)
        await db.commit()
        await db.refresh(role)
        
        # Check default value
        assert role.is_active is True  # Default value
    
    @pytest.mark.asyncio
    async def test_role_optional_fields_can_be_null(self, db):
        """Test that optional fields can be null."""
        role = Role(
            name="test_role",
            description=None,
            permissions=None
        )
        db.add(role)
        await db.commit()
        await db.refresh(role)
        
        # Should succeed with null optional fields
        assert role.description is None
        assert role.permissions is None


class TestUserRoleConstraints:
    """Test UserRole model constraints and validation."""
    
    @pytest.mark.asyncio
    async def test_user_role_user_id_required(self, db):
        """Test that user_id is required."""
        role = Role(
            name="test_role",
            is_active=True
        )
        db.add(role)
        await db.commit()
        await db.refresh(role)
        
        user_role = UserRole(
            user_id=None,  # No user_id
            role_id=role.id,
            is_active=True
        )
        db.add(user_role)
        
        # Should raise IntegrityError due to NOT NULL constraint
        with pytest.raises(IntegrityError):
            await db.commit()
    
    @pytest.mark.asyncio
    async def test_user_role_role_id_required(self, db):
        """Test that role_id is required."""
        user = User(
            email="test@example.com",
            hashed_password="hashed_password_123",
            is_active=True,
            is_superuser=False,
            is_verified=True
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        user_role = UserRole(
            user_id=user.id,
            role_id=None,  # No role_id
            is_active=True
        )
        db.add(user_role)
        
        # Should raise IntegrityError due to NOT NULL constraint
        with pytest.raises(IntegrityError):
            await db.commit()
    
    @pytest.mark.asyncio
    async def test_user_role_foreign_key_constraints(self, db):
        """Test that foreign key constraints work correctly."""
        # Try to create user_role with non-existent user_id
        user_role1 = UserRole(
            user_id=uuid.uuid4(),  # Non-existent user
            role_id=1,  # Non-existent role
            is_active=True
        )
        db.add(user_role1)
        
        # Should raise IntegrityError due to foreign key constraint
        with pytest.raises(IntegrityError):
            await db.commit()
    
    @pytest.mark.asyncio
    async def test_user_role_boolean_field_defaults(self, db):
        """Test that boolean fields have correct defaults."""
        user = User(
            email="test@example.com",
            hashed_password="hashed_password_123",
            is_active=True,
            is_superuser=False,
            is_verified=True
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        role = Role(
            name="test_role",
            is_active=True
        )
        db.add(role)
        await db.commit()
        await db.refresh(role)
        
        user_role = UserRole(
            user_id=user.id,
            role_id=role.id
            # Not setting is_active to test default
        )
        db.add(user_role)
        await db.commit()
        await db.refresh(user_role)
        
        # Check default value
        assert user_role.is_active is True  # Default value
    
    @pytest.mark.asyncio
    async def test_user_role_optional_fields_can_be_null(self, db):
        """Test that optional fields can be null."""
        user = User(
            email="test@example.com",
            hashed_password="hashed_password_123",
            is_active=True,
            is_superuser=False,
            is_verified=True
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        role = Role(
            name="test_role",
            is_active=True
        )
        db.add(role)
        await db.commit()
        await db.refresh(role)
        
        user_role = UserRole(
            user_id=user.id,
            role_id=role.id,
            assigned_by=None  # Optional field
        )
        db.add(user_role)
        await db.commit()
        await db.refresh(user_role)
        
        # Should succeed with null optional field
        assert user_role.assigned_by is None


class TestResumeConstraints:
    """Test Resume model constraints and validation."""
    
    @pytest.mark.asyncio
    async def test_resume_user_id_required(self, db):
        """Test that user_id is required."""
        resume = Resume(
            user_id=None,  # No user_id
            title="Test Resume"
        )
        db.add(resume)
        
        # Should raise IntegrityError due to NOT NULL constraint
        with pytest.raises(IntegrityError):
            await db.commit()
    
    @pytest.mark.asyncio
    async def test_resume_title_required(self, db):
        """Test that title is required."""
        user = User(
            email="test@example.com",
            hashed_password="hashed_password_123",
            is_active=True,
            is_superuser=False,
            is_verified=True
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        resume = Resume(
            user_id=user.id,
            title=None  # No title
        )
        db.add(resume)
        
        # Should raise IntegrityError due to NOT NULL constraint
        with pytest.raises(IntegrityError):
            await db.commit()
    
    @pytest.mark.asyncio
    async def test_resume_foreign_key_constraints(self, db):
        """Test that foreign key constraints work correctly."""
        # Try to create resume with non-existent user_id
        resume = Resume(
            user_id=uuid.uuid4(),  # Non-existent user
            title="Test Resume"
        )
        db.add(resume)
        
        # Should raise IntegrityError due to foreign key constraint
        with pytest.raises(IntegrityError):
            await db.commit()
    
    @pytest.mark.asyncio
    async def test_resume_boolean_field_defaults(self, db):
        """Test that boolean fields have correct defaults."""
        user = User(
            email="test@example.com",
            hashed_password="hashed_password_123",
            is_active=True,
            is_superuser=False,
            is_verified=True
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        resume = Resume(
            user_id=user.id,
            title="Test Resume"
            # Not setting boolean fields to test defaults
        )
        db.add(resume)
        await db.commit()
        await db.refresh(resume)
        
        # Check default values
        assert resume.is_active is True  # Default value
        assert resume.is_public is False  # Default value
    
    @pytest.mark.asyncio
    async def test_resume_optional_fields_can_be_null(self, db):
        """Test that optional fields can be null."""
        user = User(
            email="test@example.com",
            hashed_password="hashed_password_123",
            is_active=True,
            is_superuser=False,
            is_verified=True
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        resume = Resume(
            user_id=user.id,
            title="Test Resume",
            file_path=None,
            file_name=None,
            file_size=None,
            file_type=None,
            summary=None,
            experience_years=None,
            education_level=None,
            skills=None,
            languages=None,
            last_analyzed=None
        )
        db.add(resume)
        await db.commit()
        await db.refresh(resume)
        
        # Should succeed with null optional fields
        assert resume.file_path is None
        assert resume.file_name is None
        assert resume.file_size is None
        assert resume.file_type is None
        assert resume.summary is None
        assert resume.experience_years is None
        assert resume.education_level is None
        assert resume.skills is None
        assert resume.languages is None
        assert resume.last_analyzed is None


class TestScoreConstraints:
    """Test Score model constraints and validation."""
    
    @pytest.mark.asyncio
    async def test_score_user_id_required(self, db):
        """Test that user_id is required."""
        score = Score(
            user_id=None,  # No user_id
            resume_id=1,
            analysis_type="overall",
            overall_score=85.5
        )
        db.add(score)
        
        # Should raise IntegrityError due to NOT NULL constraint
        with pytest.raises(IntegrityError):
            await db.commit()
    
    @pytest.mark.asyncio
    async def test_score_resume_id_required(self, db):
        """Test that resume_id is required."""
        user = User(
            email="test@example.com",
            hashed_password="hashed_password_123",
            is_active=True,
            is_superuser=False,
            is_verified=True
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        score = Score(
            user_id=user.id,
            resume_id=None,  # No resume_id
            analysis_type="overall",
            overall_score=85.5
        )
        db.add(score)
        
        # Should raise IntegrityError due to NOT NULL constraint
        with pytest.raises(IntegrityError):
            await db.commit()
    
    @pytest.mark.asyncio
    async def test_score_analysis_type_required(self, db):
        """Test that analysis_type is required."""
        user = User(
            email="test@example.com",
            hashed_password="hashed_password_123",
            is_active=True,
            is_superuser=False,
            is_verified=True
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        score = Score(
            user_id=user.id,
            resume_id=1,
            analysis_type=None,  # No analysis_type
            overall_score=85.5
        )
        db.add(score)
        
        # Should raise IntegrityError due to NOT NULL constraint
        with pytest.raises(IntegrityError):
            await db.commit()
    
    @pytest.mark.asyncio
    async def test_score_overall_score_required(self, db):
        """Test that overall_score is required."""
        user = User(
            email="test@example.com",
            hashed_password="hashed_password_123",
            is_active=True,
            is_superuser=False,
            is_verified=True
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        score = Score(
            user_id=user.id,
            resume_id=1,
            analysis_type="overall",
            overall_score=None  # No overall_score
        )
        db.add(score)
        
        # Should raise IntegrityError due to NOT NULL constraint
        with pytest.raises(IntegrityError):
            await db.commit()
    
    @pytest.mark.asyncio
    async def test_score_foreign_key_constraints(self, db):
        """Test that foreign key constraints work correctly."""
        # Try to create score with non-existent user_id
        score = Score(
            user_id=uuid.uuid4(),  # Non-existent user
            resume_id=1,  # Non-existent resume
            analysis_type="overall",
            overall_score=85.5
        )
        db.add(score)
        
        # Should raise IntegrityError due to foreign key constraint
        with pytest.raises(IntegrityError):
            await db.commit()
    
    @pytest.mark.asyncio
    async def test_score_boolean_field_defaults(self, db):
        """Test that boolean fields have correct defaults."""
        user = User(
            email="test@example.com",
            hashed_password="hashed_password_123",
            is_active=True,
            is_superuser=False,
            is_verified=True
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        score = Score(
            user_id=user.id,
            resume_id=1,
            analysis_type="overall",
            overall_score=85.5
            # Not setting is_active to test default
        )
        db.add(score)
        await db.commit()
        await db.refresh(score)
        
        # Check default value
        assert score.is_active is True  # Default value
    
    @pytest.mark.asyncio
    async def test_score_optional_fields_can_be_null(self, db):
        """Test that optional fields can be null."""
        user = User(
            email="test@example.com",
            hashed_password="hashed_password_123",
            is_active=True,
            is_superuser=False,
            is_verified=True
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        score = Score(
            user_id=user.id,
            resume_id=1,
            analysis_type="overall",
            overall_score=85.5,
            job_title=None,
            company=None,
            skill_score=None,
            experience_score=None,
            education_score=None,
            skill_matches=None,
            skill_gaps=None,
            recommendations=None,
            analysis_details=None
        )
        db.add(score)
        await db.commit()
        await db.refresh(score)
        
        # Should succeed with null optional fields
        assert score.job_title is None
        assert score.company is None
        assert score.skill_score is None
        assert score.experience_score is None
        assert score.education_score is None
        assert score.skill_matches is None
        assert score.skill_gaps is None
        assert score.recommendations is None
        assert score.analysis_details is None


class TestCascadeDeletionConstraints:
    """Test cascade deletion constraints."""
    
    @pytest.mark.asyncio
    async def test_user_cascade_deletion(self, db):
        """Test that deleting a user cascades to related records."""
        # Create user
        user = User(
            email="test@example.com",
            hashed_password="hashed_password_123",
            is_active=True,
            is_superuser=False,
            is_verified=True
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        # Create role
        role = Role(
            name="test_role",
            is_active=True
        )
        db.add(role)
        await db.commit()
        await db.refresh(role)
        
        # Create user-role relationship
        user_role = UserRole(
            user_id=user.id,
            role_id=role.id,
            assigned_by=user.id,
            is_active=True
        )
        db.add(user_role)
        await db.commit()
        await db.refresh(user_role)
        
        # Create resume
        resume = Resume(
            user_id=user.id,
            title="Test Resume"
        )
        db.add(resume)
        await db.commit()
        await db.refresh(resume)
        
        # Create score
        score = Score(
            user_id=user.id,
            resume_id=resume.id,
            analysis_type="overall",
            overall_score=85.5
        )
        db.add(score)
        await db.commit()
        await db.refresh(score)
        
        # Verify all records exist
        result = await db.execute(select(UserRole).where(UserRole.user_id == user.id))
        user_roles = result.scalars().all()
        assert len(user_roles) == 1
        
        result = await db.execute(select(Resume).where(Resume.user_id == user.id))
        user_resumes = result.scalars().all()
        assert len(user_resumes) == 1
        
        result = await db.execute(select(Score).where(Score.user_id == user.id))
        user_scores = result.scalars().all()
        assert len(user_scores) == 1
        
        # Delete user
        await db.delete(user)
        await db.commit()
        
        # Verify cascade deletion
        result = await db.execute(select(UserRole).where(UserRole.user_id == user.id))
        user_roles = result.scalars().all()
        assert len(user_roles) == 0
        
        result = await db.execute(select(Resume).where(Resume.user_id == user.id))
        user_resumes = result.scalars().all()
        assert len(user_resumes) == 0
        
        result = await db.execute(select(Score).where(Score.user_id == user.id))
        user_scores = result.scalars().all()
        assert len(user_scores) == 0
        
        # Verify role still exists (not cascaded)
        result = await db.execute(select(Role).where(Role.id == role.id))
        role_still_exists = result.scalar_one_or_none()
        assert role_still_exists is not None
    
    @pytest.mark.asyncio
    async def test_resume_cascade_deletion(self, db):
        """Test that deleting a resume cascades to related scores."""
        # Create user
        user = User(
            email="test@example.com",
            hashed_password="hashed_password_123",
            is_active=True,
            is_superuser=False,
            is_verified=True
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        # Create resume
        resume = Resume(
            user_id=user.id,
            title="Test Resume"
        )
        db.add(resume)
        await db.commit()
        await db.refresh(resume)
        
        # Create scores for the resume
        score1 = Score(
            user_id=user.id,
            resume_id=resume.id,
            analysis_type="overall",
            overall_score=85.5
        )
        score2 = Score(
            user_id=user.id,
            resume_id=resume.id,
            analysis_type="job_match",
            overall_score=92.0
        )
        db.add_all([score1, score2])
        await db.commit()
        await db.refresh(score1)
        await db.refresh(score2)
        
        # Verify scores exist
        result = await db.execute(select(Score).where(Score.resume_id == resume.id))
        resume_scores = result.scalars().all()
        assert len(resume_scores) == 2
        
        # Delete resume
        await db.delete(resume)
        await db.commit()
        
        # Verify scores are deleted
        result = await db.execute(select(Score).where(Score.resume_id == resume.id))
        resume_scores = result.scalars().all()
        assert len(resume_scores) == 0
        
        # Verify user still exists (not cascaded)
        result = await db.execute(select(User).where(User.id == user.id))
        user_still_exists = result.scalar_one_or_none()
        assert user_still_exists is not None

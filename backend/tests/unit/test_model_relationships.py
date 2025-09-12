"""
Unit tests for model relationships and foreign key constraints.

This module tests the relationships between models and verifies
that foreign key constraints work correctly.

Author: AI Job Readiness Team
Version: 1.0.0
"""

import pytest
import uuid
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.user import User
from app.models.role import Role, UserRole
from app.models.resume import Resume
from app.models.score import Score


class TestUserRoleRelationships:
    """Test User-Role many-to-many relationships."""
    
    @pytest.mark.asyncio
    async def test_user_role_creation_with_relationships(self):
        """Test creating user-role relationships."""
        from app.db.database import get_async_session_local
        
        async with get_async_session_local()() as db:
            # Create a user
            user = User(
                email="test@example.com",
                hashed_password="hashed_password_123",
                first_name="Test",
                last_name="User",
                is_active=True,
                is_superuser=False,
                is_verified=True
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
        
        # Create a role
        role = Role(
            name="test_role",
            description="Test role",
            is_active=True
        )
        role.set_permissions_list(["read", "write"])
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
        
        # Verify relationships
        assert user_role.user_id == user.id
        assert user_role.role_id == role.id
        assert user_role.assigned_by == user.id
        assert user_role.is_active is True
    
    @pytest.mark.asyncio
    async def test_user_role_queries_with_relationships(self, db):
        """Test querying users and roles with their relationships."""
        # Create users
        user1 = User(
            email="user1@example.com",
            hashed_password="hashed_password_123",
            first_name="User",
            last_name="One",
            is_active=True,
            is_superuser=False,
            is_verified=True
        )
        user2 = User(
            email="user2@example.com",
            hashed_password="hashed_password_123",
            first_name="User",
            last_name="Two",
            is_active=True,
            is_superuser=False,
            is_verified=True
        )
        db.add_all([user1, user2])
        await db.commit()
        await db.refresh(user1)
        await db.refresh(user2)
        
        # Create roles
        admin_role = Role(
            name="admin",
            description="Administrator role",
            is_active=True
        )
        admin_role.set_permissions_list(["read", "write", "delete"])
        
        user_role_model = Role(
            name="user",
            description="Regular user role",
            is_active=True
        )
        user_role_model.set_permissions_list(["read"])
        
        db.add_all([admin_role, user_role_model])
        await db.commit()
        await db.refresh(admin_role)
        await db.refresh(user_role_model)
        
        # Create user-role assignments
        user1_admin = UserRole(
            user_id=user1.id,
            role_id=admin_role.id,
            assigned_by=user1.id,
            is_active=True
        )
        user2_user = UserRole(
            user_id=user2.id,
            role_id=user_role_model.id,
            assigned_by=user1.id,
            is_active=True
        )
        db.add_all([user1_admin, user2_user])
        await db.commit()
        await db.refresh(user1_admin)
        await db.refresh(user2_user)
        
        # Query users with roles
        result = await db.execute(
            select(User)
            .options(selectinload(User.roles).selectinload(UserRole.role))
            .where(User.id == user1.id)
        )
        user_with_roles = result.scalar_one()
        
        assert len(user_with_roles.roles) == 1
        assert user_with_roles.roles[0].role.name == "admin"
        assert user_with_roles.roles[0].role.description == "Administrator role"
        assert "read" in user_with_roles.roles[0].role.get_permissions_list()
        assert "write" in user_with_roles.roles[0].role.get_permissions_list()
        assert "delete" in user_with_roles.roles[0].role.get_permissions_list()
        
        # Test user role methods
        assert user_with_roles.has_role("admin") is True
        assert user_with_roles.has_role("user") is False
        assert user_with_roles.is_admin() is True
        assert "admin" in user_with_roles.get_role_names()
    
    @pytest.mark.asyncio
    async def test_user_role_cascade_deletion(self, db):
        """Test that user-role relationships are deleted when user is deleted."""
        # Create user and role
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
            description="Test role",
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
        
        # Verify relationship exists
        result = await db.execute(select(UserRole).where(UserRole.user_id == user.id))
        user_roles = result.scalars().all()
        assert len(user_roles) == 1
        
        # Delete user
        await db.delete(user)
        await db.commit()
        
        # Verify user-role relationship is deleted
        result = await db.execute(select(UserRole).where(UserRole.user_id == user.id))
        user_roles = result.scalars().all()
        assert len(user_roles) == 0
        
        # Verify role still exists
        result = await db.execute(select(Role).where(Role.id == role.id))
        role_still_exists = result.scalar_one_or_none()
        assert role_still_exists is not None


class TestUserResumeRelationships:
    """Test User-Resume one-to-many relationships."""
    
    @pytest.mark.asyncio
    async def test_user_resume_creation_with_relationship(self, db):
        """Test creating resume with user relationship."""
        # Create user
        user = User(
            email="test@example.com",
            hashed_password="hashed_password_123",
            first_name="Test",
            last_name="User",
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
            title="My Resume",
            file_name="resume.pdf",
            file_size=1024000,
            file_type="PDF",
            summary="Experienced software engineer",
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
        
        # Verify relationship
        assert resume.user_id == user.id
        assert resume.title == "My Resume"
        assert resume.file_name == "resume.pdf"
        assert resume.file_size == 1024000
        assert resume.file_type == "PDF"
        assert resume.summary == "Experienced software engineer"
        assert resume.experience_years == 5.0
        assert resume.education_level == "Bachelor's Degree"
        assert resume.get_skills_list() == ["Python", "JavaScript", "SQL"]
        assert len(resume.get_languages_list()) == 2
    
    @pytest.mark.asyncio
    async def test_user_multiple_resumes(self, db):
        """Test user having multiple resumes."""
        # Create user
        user = User(
            email="test@example.com",
            hashed_password="hashed_password_123",
            first_name="Test",
            last_name="User",
            is_active=True,
            is_superuser=False,
            is_verified=True
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        # Create multiple resumes
        resume1 = Resume(
            user_id=user.id,
            title="Software Engineer Resume",
            file_name="software_resume.pdf",
            file_type="PDF",
            summary="Software engineering experience"
        )
        
        resume2 = Resume(
            user_id=user.id,
            title="Data Scientist Resume",
            file_name="data_science_resume.pdf",
            file_type="PDF",
            summary="Data science experience"
        )
        
        resume3 = Resume(
            user_id=user.id,
            title="Manager Resume",
            file_name="manager_resume.pdf",
            file_type="PDF",
            summary="Management experience"
        )
        
        db.add_all([resume1, resume2, resume3])
        await db.commit()
        await db.refresh(resume1)
        await db.refresh(resume2)
        await db.refresh(resume3)
        
        # Query user with resumes
        result = await db.execute(
            select(User)
            .options(selectinload(User.resumes))
            .where(User.id == user.id)
        )
        user_with_resumes = result.scalar_one()
        
        assert len(user_with_resumes.resumes) == 3
        resume_titles = [resume.title for resume in user_with_resumes.resumes]
        assert "Software Engineer Resume" in resume_titles
        assert "Data Scientist Resume" in resume_titles
        assert "Manager Resume" in resume_titles
    
    @pytest.mark.asyncio
    async def test_user_resume_cascade_deletion(self, db):
        """Test that resumes are deleted when user is deleted."""
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
        
        # Create resumes
        resume1 = Resume(
            user_id=user.id,
            title="Resume 1",
            file_name="resume1.pdf"
        )
        resume2 = Resume(
            user_id=user.id,
            title="Resume 2",
            file_name="resume2.pdf"
        )
        
        db.add_all([resume1, resume2])
        await db.commit()
        await db.refresh(resume1)
        await db.refresh(resume2)
        
        # Verify resumes exist
        result = await db.execute(select(Resume).where(Resume.user_id == user.id))
        user_resumes = result.scalars().all()
        assert len(user_resumes) == 2
        
        # Delete user
        await db.delete(user)
        await db.commit()
        
        # Verify resumes are deleted
        result = await db.execute(select(Resume).where(Resume.user_id == user.id))
        user_resumes = result.scalars().all()
        assert len(user_resumes) == 0


class TestUserScoreRelationships:
    """Test User-Score one-to-many relationships."""
    
    @pytest.mark.asyncio
    async def test_user_score_creation_with_relationship(self, db):
        """Test creating score with user relationship."""
        # Create user
        user = User(
            email="test@example.com",
            hashed_password="hashed_password_123",
            first_name="Test",
            last_name="User",
            is_active=True,
            is_superuser=False,
            is_verified=True
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        # Create score
        score = Score(
            user_id=user.id,
            resume_id=1,  # This would normally reference a real resume
            analysis_type="overall",
            overall_score=85.5,
            skill_score=80.0,
            experience_score=90.0,
            education_score=85.0
        )
        score.set_skill_matches_list(["Python", "JavaScript", "SQL"])
        score.set_skill_gaps_list(["Docker", "Kubernetes"])
        score.set_analysis_details_dict({"confidence": 0.95, "model_version": "v1.2"})
        
        db.add(score)
        await db.commit()
        await db.refresh(score)
        
        # Verify relationship
        assert score.user_id == user.id
        assert score.resume_id == 1
        assert score.analysis_type == "overall"
        assert score.overall_score == 85.5
        assert score.skill_score == 80.0
        assert score.experience_score == 90.0
        assert score.education_score == 85.0
        assert score.get_skill_matches_list() == ["Python", "JavaScript", "SQL"]
        assert score.get_skill_gaps_list() == ["Docker", "Kubernetes"]
        assert score.get_analysis_details_dict() == {"confidence": 0.95, "model_version": "v1.2"}
    
    @pytest.mark.asyncio
    async def test_user_multiple_scores(self, db):
        """Test user having multiple scores."""
        # Create user
        user = User(
            email="test@example.com",
            hashed_password="hashed_password_123",
            first_name="Test",
            last_name="User",
            is_active=True,
            is_superuser=False,
            is_verified=True
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        # Create multiple scores
        score1 = Score(
            user_id=user.id,
            resume_id=1,
            analysis_type="overall",
            overall_score=85.5
        )
        
        score2 = Score(
            user_id=user.id,
            resume_id=1,
            analysis_type="job_match",
            overall_score=92.0,
            job_title="Software Engineer",
            company="Tech Corp"
        )
        
        score3 = Score(
            user_id=user.id,
            resume_id=2,
            analysis_type="skill_analysis",
            overall_score=78.5
        )
        
        db.add_all([score1, score2, score3])
        await db.commit()
        await db.refresh(score1)
        await db.refresh(score2)
        await db.refresh(score3)
        
        # Query user with scores
        result = await db.execute(
            select(User)
            .options(selectinload(User.scores))
            .where(User.id == user.id)
        )
        user_with_scores = result.scalar_one()
        
        assert len(user_with_scores.scores) == 3
        analysis_types = [score.analysis_type for score in user_with_scores.scores]
        assert "overall" in analysis_types
        assert "job_match" in analysis_types
        assert "skill_analysis" in analysis_types
    
    @pytest.mark.asyncio
    async def test_user_score_cascade_deletion(self, db):
        """Test that scores are deleted when user is deleted."""
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
        
        # Create scores
        score1 = Score(
            user_id=user.id,
            resume_id=1,
            analysis_type="overall",
            overall_score=85.5
        )
        score2 = Score(
            user_id=user.id,
            resume_id=1,
            analysis_type="job_match",
            overall_score=92.0
        )
        
        db.add_all([score1, score2])
        await db.commit()
        await db.refresh(score1)
        await db.refresh(score2)
        
        # Verify scores exist
        result = await db.execute(select(Score).where(Score.user_id == user.id))
        user_scores = result.scalars().all()
        assert len(user_scores) == 2
        
        # Delete user
        await db.delete(user)
        await db.commit()
        
        # Verify scores are deleted
        result = await db.execute(select(Score).where(Score.user_id == user.id))
        user_scores = result.scalars().all()
        assert len(user_scores) == 0


class TestResumeScoreRelationships:
    """Test Resume-Score one-to-many relationships."""
    
    @pytest.mark.asyncio
    async def test_resume_score_creation_with_relationship(self, db):
        """Test creating score with resume relationship."""
        # Create user
        user = User(
            email="test@example.com",
            hashed_password="hashed_password_123",
            first_name="Test",
            last_name="User",
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
            title="My Resume",
            file_name="resume.pdf",
            summary="Experienced software engineer"
        )
        db.add(resume)
        await db.commit()
        await db.refresh(resume)
        
        # Create score for the resume
        score = Score(
            user_id=user.id,
            resume_id=resume.id,
            analysis_type="overall",
            overall_score=85.5,
            skill_score=80.0,
            experience_score=90.0
        )
        db.add(score)
        await db.commit()
        await db.refresh(score)
        
        # Verify relationship
        assert score.user_id == user.id
        assert score.resume_id == resume.id
        assert score.analysis_type == "overall"
        assert score.overall_score == 85.5
    
    @pytest.mark.asyncio
    async def test_resume_multiple_scores(self, db):
        """Test resume having multiple scores."""
        # Create user
        user = User(
            email="test@example.com",
            hashed_password="hashed_password_123",
            first_name="Test",
            last_name="User",
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
            title="My Resume",
            file_name="resume.pdf"
        )
        db.add(resume)
        await db.commit()
        await db.refresh(resume)
        
        # Create multiple scores for the resume
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
            overall_score=92.0,
            job_title="Software Engineer"
        )
        
        score3 = Score(
            user_id=user.id,
            resume_id=resume.id,
            analysis_type="skill_analysis",
            overall_score=78.5
        )
        
        db.add_all([score1, score2, score3])
        await db.commit()
        await db.refresh(score1)
        await db.refresh(score2)
        await db.refresh(score3)
        
        # Query resume with scores
        result = await db.execute(
            select(Resume)
            .options(selectinload(Resume.scores))
            .where(Resume.id == resume.id)
        )
        resume_with_scores = result.scalar_one()
        
        assert len(resume_with_scores.scores) == 3
        analysis_types = [score.analysis_type for score in resume_with_scores.scores]
        assert "overall" in analysis_types
        assert "job_match" in analysis_types
        assert "skill_analysis" in analysis_types
    
    @pytest.mark.asyncio
    async def test_resume_score_cascade_deletion(self, db):
        """Test that scores are deleted when resume is deleted."""
        # Create user
        user = User(
            email="test@example.com",
            hashed_password="hashed_password_123",
            first_name="Test",
            last_name="User",
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
            title="My Resume",
            file_name="resume.pdf"
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


class TestComplexRelationships:
    """Test complex multi-model relationships."""
    
    @pytest.mark.asyncio
    async def test_complete_user_workflow(self, db):
        """Test complete user workflow with all relationships."""
        # Create user
        user = User(
            email="complete@example.com",
            hashed_password="hashed_password_123",
            first_name="Complete",
            last_name="User",
            is_active=True,
            is_superuser=False,
            is_verified=True
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        # Create role and assign to user
        role = Role(
            name="user",
            description="Regular user role",
            is_active=True
        )
        role.set_permissions_list(["read", "write"])
        db.add(role)
        await db.commit()
        await db.refresh(role)
        
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
            title="Complete Resume",
            file_name="complete_resume.pdf",
            file_size=1024000,
            file_type="PDF",
            summary="Complete user with full profile",
            experience_years=5.0,
            education_level="Bachelor's Degree"
        )
        resume.set_skills_list(["Python", "JavaScript", "SQL", "Docker"])
        resume.set_languages_list([
            {"name": "English", "level": "Native"},
            {"name": "Spanish", "level": "Intermediate"}
        ])
        db.add(resume)
        await db.commit()
        await db.refresh(resume)
        
        # Create scores for the resume
        overall_score = Score(
            user_id=user.id,
            resume_id=resume.id,
            analysis_type="overall",
            overall_score=88.5,
            skill_score=85.0,
            experience_score=90.0,
            education_score=90.0
        )
        overall_score.set_skill_matches_list(["Python", "JavaScript", "SQL"])
        overall_score.set_skill_gaps_list(["Kubernetes", "AWS"])
        
        job_match_score = Score(
            user_id=user.id,
            resume_id=resume.id,
            analysis_type="job_match",
            overall_score=92.0,
            job_title="Senior Software Engineer",
            company="Tech Corp",
            skill_score=90.0,
            experience_score=95.0
        )
        job_match_score.set_skill_matches_list(["Python", "JavaScript", "Docker"])
        job_match_score.set_skill_gaps_list(["Kubernetes", "AWS", "React"])
        
        db.add_all([overall_score, job_match_score])
        await db.commit()
        await db.refresh(overall_score)
        await db.refresh(job_match_score)
        
        # Query complete user with all relationships
        result = await db.execute(
            select(User)
            .options(
                selectinload(User.roles).selectinload(UserRole.role),
                selectinload(User.resumes),
                selectinload(User.scores)
            )
            .where(User.id == user.id)
        )
        complete_user = result.scalar_one()
        
        # Verify user data
        assert complete_user.email == "complete@example.com"
        assert complete_user.full_name == "Complete User"
        assert complete_user.is_active is True
        
        # Verify role relationship
        assert len(complete_user.roles) == 1
        assert complete_user.roles[0].role.name == "user"
        assert complete_user.has_role("user") is True
        assert complete_user.is_admin() is False
        
        # Verify resume relationship
        assert len(complete_user.resumes) == 1
        user_resume = complete_user.resumes[0]
        assert user_resume.title == "Complete Resume"
        assert user_resume.file_name == "complete_resume.pdf"
        assert user_resume.file_size == 1024000
        assert user_resume.file_type == "PDF"
        assert user_resume.summary == "Complete user with full profile"
        assert user_resume.experience_years == 5.0
        assert user_resume.education_level == "Bachelor's Degree"
        assert user_resume.get_skills_list() == ["Python", "JavaScript", "SQL", "Docker"]
        assert len(user_resume.get_languages_list()) == 2
        
        # Verify score relationships
        assert len(complete_user.scores) == 2
        score_types = [score.analysis_type for score in complete_user.scores]
        assert "overall" in score_types
        assert "job_match" in score_types
        
        # Verify resume-score relationship
        assert len(user_resume.scores) == 2
        resume_score_types = [score.analysis_type for score in user_resume.scores]
        assert "overall" in resume_score_types
        assert "job_match" in resume_score_types
        
        # Test score details
        overall_score_obj = next(score for score in complete_user.scores if score.analysis_type == "overall")
        assert overall_score_obj.overall_score == 88.5
        assert overall_score_obj.skill_score == 85.0
        assert overall_score_obj.experience_score == 90.0
        assert overall_score_obj.education_score == 90.0
        assert overall_score_obj.get_skill_matches_list() == ["Python", "JavaScript", "SQL"]
        assert overall_score_obj.get_skill_gaps_list() == ["Kubernetes", "AWS"]
        
        job_match_score_obj = next(score for score in complete_user.scores if score.analysis_type == "job_match")
        assert job_match_score_obj.overall_score == 92.0
        assert job_match_score_obj.job_title == "Senior Software Engineer"
        assert job_match_score_obj.company == "Tech Corp"
        assert job_match_score_obj.skill_score == 90.0
        assert job_match_score_obj.experience_score == 95.0
        assert job_match_score_obj.get_skill_matches_list() == ["Python", "JavaScript", "Docker"]
        assert job_match_score_obj.get_skill_gaps_list() == ["Kubernetes", "AWS", "React"]

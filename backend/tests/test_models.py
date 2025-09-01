import pytest
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.db.database import Base
from app.models import User, Role, UserRole, Resume, Score


@pytest.fixture
async def engine():
    """Create a test database engine"""
    # Use in-memory SQLite for testing
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
        future=True
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    await engine.dispose()


@pytest.fixture
async def session(engine):
    """Create a test database session"""
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        yield session


@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
    return {
        "email": "test@example.com",
        "hashed_password": "hashed_password_123",
        "first_name": "John",
        "last_name": "Doe",
        "phone": "+1234567890",
        "bio": "Test user bio",
        "is_active": True,
        "is_verified": True
    }


@pytest.fixture
def sample_role_data():
    """Sample role data for testing"""
    return {
        "name": "user",
        "description": "Regular user role",
        "permissions": '["read", "write"]',
        "is_active": True
    }


@pytest.fixture
def sample_resume_data():
    """Sample resume data for testing"""
    return {
        "title": "Software Engineer Resume",
        "file_path": "/uploads/resume.pdf",
        "file_name": "resume.pdf",
        "file_size": 1024000,
        "file_type": "PDF",
        "summary": "Experienced software engineer",
        "experience_years": 5.0,
        "education_level": "Bachelor's Degree",
        "skills": '["Python", "JavaScript", "SQL"]',
        "languages": '["English", "Spanish"]',
        "is_active": True,
        "is_public": False
    }


@pytest.fixture
def sample_score_data():
    """Sample score data for testing"""
    return {
        "analysis_type": "job_match",
        "job_title": "Software Engineer",
        "company": "Tech Corp",
        "overall_score": 85.5,
        "skill_score": 90.0,
        "experience_score": 80.0,
        "education_score": 85.0,
        "skill_matches": '["Python", "JavaScript"]',
        "skill_gaps": '["React", "Docker"]',
        "recommendations": "Consider learning React and Docker",
        "analysis_details": '{"matched_skills": 8, "total_skills": 10}',
        "is_active": True
    }


class TestUserModel:
    """Test cases for User model"""
    
    @pytest.mark.asyncio
    async def test_create_user(self, session: AsyncSession, sample_user_data: dict):
        """Test creating a user"""
        user = User(**sample_user_data)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        
        assert user.id is not None
        assert user.email == sample_user_data["email"]
        assert user.first_name == sample_user_data["first_name"]
        assert user.last_name == sample_user_data["last_name"]
        assert user.is_active == sample_user_data["is_active"]
        assert user.is_verified == sample_user_data["is_verified"]
        assert user.created_at is not None
    
    @pytest.mark.asyncio
    async def test_user_relationships(self, session: AsyncSession, sample_user_data: dict):
        """Test user relationships"""
        user = User(**sample_user_data)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        
        # Test that relationships are empty initially
        assert len(user.roles) == 0
        assert len(user.resumes) == 0
        assert len(user.scores) == 0


class TestRoleModel:
    """Test cases for Role model"""
    
    @pytest.mark.asyncio
    async def test_create_role(self, session: AsyncSession, sample_role_data: dict):
        """Test creating a role"""
        role = Role(**sample_role_data)
        session.add(role)
        await session.commit()
        await session.refresh(role)
        
        assert role.id is not None
        assert role.name == sample_role_data["name"]
        assert role.description == sample_role_data["description"]
        assert role.permissions == sample_role_data["permissions"]
        assert role.is_active == sample_role_data["is_active"]
        assert role.created_at is not None


class TestUserRoleModel:
    """Test cases for UserRole model"""
    
    @pytest.mark.asyncio
    async def test_create_user_role(self, session: AsyncSession, sample_user_data: dict, sample_role_data: dict):
        """Test creating a user-role association"""
        # Create user and role first
        user = User(**sample_user_data)
        role = Role(**sample_role_data)
        session.add_all([user, role])
        await session.commit()
        await session.refresh(user)
        await session.refresh(role)
        
        # Create user-role association
        user_role = UserRole(
            user_id=user.id,
            role_id=role.id,
            assigned_by=user.id
        )
        session.add(user_role)
        await session.commit()
        await session.refresh(user_role)
        
        assert user_role.id is not None
        assert user_role.user_id == user.id
        assert user_role.role_id == role.id
        assert user_role.assigned_at is not None


class TestResumeModel:
    """Test cases for Resume model"""
    
    @pytest.mark.asyncio
    async def test_create_resume(self, session: AsyncSession, sample_user_data: dict, sample_resume_data: dict):
        """Test creating a resume"""
        # Create user first
        user = User(**sample_user_data)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        
        # Create resume
        resume_data = {**sample_resume_data, "user_id": user.id}
        resume = Resume(**resume_data)
        session.add(resume)
        await session.commit()
        await session.refresh(resume)
        
        assert resume.id is not None
        assert resume.user_id == user.id
        assert resume.title == sample_resume_data["title"]
        assert resume.file_path == sample_resume_data["file_path"]
        assert resume.experience_years == sample_resume_data["experience_years"]
        assert resume.is_active == sample_resume_data["is_active"]
        assert resume.created_at is not None
    
    @pytest.mark.asyncio
    async def test_resume_user_relationship(self, session: AsyncSession, sample_user_data: dict, sample_resume_data: dict):
        """Test resume-user relationship"""
        # Create user and resume
        user = User(**sample_user_data)
        resume_data = {**sample_resume_data, "user_id": user.id}
        resume = Resume(**resume_data)
        session.add_all([user, resume])
        await session.commit()
        await session.refresh(user)
        await session.refresh(resume)
        
        # Test relationships
        assert resume.user.id == user.id
        assert len(user.resumes) == 1
        assert user.resumes[0].id == resume.id


class TestScoreModel:
    """Test cases for Score model"""
    
    @pytest.mark.asyncio
    async def test_create_score(self, session: AsyncSession, sample_user_data: dict, sample_resume_data: dict, sample_score_data: dict):
        """Test creating a score"""
        # Create user and resume first
        user = User(**sample_user_data)
        resume_data = {**sample_resume_data, "user_id": user.id}
        resume = Resume(**resume_data)
        session.add_all([user, resume])
        await session.commit()
        await session.refresh(user)
        await session.refresh(resume)
        
        # Create score
        score_data = {**sample_score_data, "user_id": user.id, "resume_id": resume.id}
        score = Score(**score_data)
        session.add(score)
        await session.commit()
        await session.refresh(score)
        
        assert score.id is not None
        assert score.user_id == user.id
        assert score.resume_id == resume.id
        assert score.overall_score == sample_score_data["overall_score"]
        assert score.analysis_type == sample_score_data["analysis_type"]
        assert score.analysis_date is not None
        assert score.created_at is not None
    
    @pytest.mark.asyncio
    async def test_score_relationships(self, session: AsyncSession, sample_user_data: dict, sample_resume_data: dict, sample_score_data: dict):
        """Test score relationships"""
        # Create user, resume, and score
        user = User(**sample_user_data)
        resume_data = {**sample_resume_data, "user_id": user.id}
        resume = Resume(**resume_data)
        score_data = {**sample_score_data, "user_id": user.id, "resume_id": resume.id}
        score = Score(**score_data)
        session.add_all([user, resume, score])
        await session.commit()
        await session.refresh(user)
        await session.refresh(resume)
        await session.refresh(score)
        
        # Test relationships
        assert score.user.id == user.id
        assert score.resume.id == resume.id
        assert len(user.scores) == 1
        assert len(resume.scores) == 1
        assert user.scores[0].id == score.id
        assert resume.scores[0].id == score.id


class TestModelRelationships:
    """Test cases for model relationships"""
    
    @pytest.mark.asyncio
    async def test_cascade_delete(self, session: AsyncSession, sample_user_data: dict, sample_resume_data: dict, sample_score_data: dict):
        """Test cascade delete functionality"""
        # Create user, resume, and score
        user = User(**sample_user_data)
        resume_data = {**sample_resume_data, "user_id": user.id}
        resume = Resume(**resume_data)
        score_data = {**sample_score_data, "user_id": user.id, "resume_id": resume.id}
        score = Score(**score_data)
        session.add_all([user, resume, score])
        await session.commit()
        
        # Verify all records exist
        assert await session.get(User, user.id) is not None
        assert await session.get(Resume, resume.id) is not None
        assert await session.get(Score, score.id) is not None
        
        # Delete user (should cascade to resume and score)
        await session.delete(user)
        await session.commit()
        
        # Verify cascade delete
        assert await session.get(User, user.id) is None
        assert await session.get(Resume, resume.id) is None
        assert await session.get(Score, score.id) is None


#!/usr/bin/env python3
"""
Basic test script to verify SQLAlchemy models work correctly.
This script tests model creation and basic functionality without complex async testing.
"""

import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.dirname(__file__))

def test_model_imports():
    """Test that all models can be imported"""
    try:
        from app.models import User, Role, UserRole, Resume, Score
        print("✅ All models imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Error importing models: {e}")
        return False

def test_model_creation():
    """Test that models can be created without database errors"""
    try:
        from app.models import User, Role, UserRole, Resume, Score
        import uuid
        
        # Test creating model instances (without saving to database)
        user = User(
            email="test@example.com",
            hashed_password="test_hash",
            first_name="Test",
            last_name="User"
        )
        
        role = Role(
            name="test_role",
            description="Test role"
        )
        
        user_role = UserRole(
            user_id=user.id,
            role_id=role.id
        )
        
        resume = Resume(
            user_id=user.id,
            title="Test Resume"
        )
        
        score = Score(
            user_id=user.id,
            resume_id=resume.id,
            analysis_type="test",
            overall_score=85.0
        )
        
        print("✅ All models can be created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error creating models: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_model_relationships():
    """Test that model relationships are properly defined"""
    try:
        from app.models import User, Role, UserRole, Resume, Score
        
        # Check that models have the expected attributes
        user_attrs = dir(User())
        role_attrs = dir(Role())
        user_role_attrs = dir(UserRole())
        resume_attrs = dir(Resume())
        score_attrs = dir(Score())
        
        # Check for relationship attributes
        assert 'roles' in user_attrs, "User should have 'roles' relationship"
        assert 'resumes' in user_attrs, "User should have 'resumes' relationship"
        assert 'scores' in user_attrs, "User should have 'scores' relationship"
        assert 'user_roles' in role_attrs, "Role should have 'user_roles' relationship"
        assert 'user' in user_role_attrs, "UserRole should have 'user' relationship"
        assert 'role' in user_role_attrs, "UserRole should have 'role' relationship"
        assert 'user' in resume_attrs, "Resume should have 'user' relationship"
        assert 'scores' in resume_attrs, "Resume should have 'scores' relationship"
        assert 'user' in score_attrs, "Score should have 'user' relationship"
        assert 'resume' in score_attrs, "Score should have 'resume' relationship"
        
        print("✅ All model relationships are properly defined")
        return True
        
    except Exception as e:
        print(f"❌ Error testing model relationships: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_model_metadata():
    """Test that models have proper metadata"""
    try:
        from app.models import User, Role, UserRole, Resume, Score
        from app.db.database import Base
        
        # Check table names
        assert User.__tablename__ == "users", f"User table name should be 'users', got {User.__tablename__}"
        assert Role.__tablename__ == "roles", f"Role table name should be 'roles', got {Role.__tablename__}"
        assert UserRole.__tablename__ == "user_roles", f"UserRole table name should be 'user_roles', got {UserRole.__tablename__}"
        assert Resume.__tablename__ == "resumes", f"Resume table name should be 'resumes', got {Resume.__tablename__}"
        assert Score.__tablename__ == "scores", f"Score table name should be 'scores', got {Score.__tablename__}"
        
        # Check that models inherit from Base
        assert issubclass(User, Base), "User should inherit from Base"
        assert issubclass(Role, Base), "Role should inherit from Base"
        assert issubclass(UserRole, Base), "UserRole should inherit from Base"
        assert issubclass(Resume, Base), "Resume should inherit from Base"
        assert issubclass(Score, Base), "Score should inherit from Base"
        
        # Check that models have __table__ attribute
        assert hasattr(User, '__table__'), "User should have __table__ attribute"
        assert hasattr(Role, '__table__'), "Role should have __table__ attribute"
        assert hasattr(UserRole, '__table__'), "UserRole should have __table__ attribute"
        assert hasattr(Resume, '__table__'), "Resume should have __table__ attribute"
        assert hasattr(Score, '__table__'), "Score should have __table__ attribute"
        
        print("✅ All model metadata is properly configured")
        return True
        
    except Exception as e:
        print(f"❌ Error testing model metadata: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🧪 Testing SQLAlchemy Models (Basic)...")
    print("=" * 50)
    
    # Test 1: Model imports
    print("\n1. Testing model imports...")
    import_success = test_model_imports()
    
    # Test 2: Model creation
    print("\n2. Testing model creation...")
    creation_success = test_model_creation()
    
    # Test 3: Model relationships
    print("\n3. Testing model relationships...")
    relationship_success = test_model_relationships()
    
    # Test 4: Model metadata
    print("\n4. Testing model metadata...")
    metadata_success = test_model_metadata()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print(f"   Model Imports: {'✅ PASS' if import_success else '❌ FAIL'}")
    print(f"   Model Creation: {'✅ PASS' if creation_success else '❌ FAIL'}")
    print(f"   Model Relationships: {'✅ PASS' if relationship_success else '❌ FAIL'}")
    print(f"   Model Metadata: {'✅ PASS' if metadata_success else '❌ FAIL'}")
    
    if all([import_success, creation_success, relationship_success, metadata_success]):
        print("\n🎉 All basic model tests passed! Models are ready for use.")
        return 0
    else:
        print("\n💥 Some model tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

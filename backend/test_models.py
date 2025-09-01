#!/usr/bin/env python3
"""
Simple script to test that all models can be imported and created without errors.
This is useful for debugging model issues before running tests or migrations.
"""

import asyncio
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.dirname(__file__))

async def test_model_imports():
    """Test that all models can be imported"""
    try:
        from app.models import User, Role, UserRole, Resume, Score
        print("✅ All models imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Error importing models: {e}")
        return False

async def test_model_creation():
    """Test that models can be created without database errors"""
    try:
        from app.models import User, Role, UserRole, Resume, Score
        from app.db.database import Base
        
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
        return False

async def test_database_connection():
    """Test database connection and table creation"""
    try:
        from app.db.database import init_db
        
        print("🔄 Testing database connection...")
        await init_db()
        print("✅ Database connection and table creation successful")
        return True
        
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        print("Note: This is expected if no database is running")
        return False

async def main():
    """Main test function"""
    print("🧪 Testing SQLAlchemy Models...")
    print("=" * 50)
    
    # Test 1: Model imports
    print("\n1. Testing model imports...")
    import_success = await test_model_imports()
    
    # Test 2: Model creation
    print("\n2. Testing model creation...")
    creation_success = await test_model_creation()
    
    # Test 3: Database connection (optional)
    print("\n3. Testing database connection...")
    db_success = await test_database_connection()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print(f"   Model Imports: {'✅ PASS' if import_success else '❌ FAIL'}")
    print(f"   Model Creation: {'✅ PASS' if creation_success else '❌ FAIL'}")
    print(f"   Database Connection: {'✅ PASS' if db_success else '⚠️  SKIP'}")
    
    if import_success and creation_success:
        print("\n🎉 All core model tests passed! Models are ready for use.")
        return 0
    else:
        print("\n💥 Some model tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)

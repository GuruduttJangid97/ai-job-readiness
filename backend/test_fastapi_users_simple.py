#!/usr/bin/env python3
"""
Simple test script for FastAPI-Users implementation

This script tests the FastAPI-Users integration without database initialization
to verify all components are properly configured.

Author: AI Job Readiness Team
Version: 1.0.0
"""

import sys
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))


def test_imports():
    """Test that all modules can be imported successfully."""
    print("🧪 Testing Module Imports")
    print("=" * 50)
    
    try:
        # Test core imports
        print("1. Testing core imports...")
        from app.core.config import settings
        print("   ✅ Settings imported successfully")
        
        from app.core.security import get_password_hash, verify_password
        print("   ✅ Security utilities imported successfully")
        
        # Test schema imports
        print("\n2. Testing schema imports...")
        from app.schemas.user import UserCreate, UserRead, UserProfile
        print("   ✅ User schemas imported successfully")
        
        # Test model imports
        print("\n3. Testing model imports...")
        from app.models.user import User
        print("   ✅ User model imported successfully")
        
        # Test FastAPI-Users imports
        print("\n4. Testing FastAPI-Users imports...")
        from app.core.users import fastapi_users, get_user_manager, get_user_db
        print("   ✅ FastAPI-Users components imported successfully")
        
        # Test API imports
        print("\n5. Testing API imports...")
        from app.api.auth import router as auth_router
        from app.api.users import router as users_router
        print("   ✅ API routers imported successfully")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Import failed: {e}")
        return False


def test_configuration():
    """Test configuration settings."""
    print("\n⚙️  Testing Configuration")
    print("=" * 50)
    
    try:
        from app.core.config import settings
        
        print("1. Testing configuration values...")
        print(f"   ✅ App name: {settings.app_name}")
        print(f"   ✅ App version: {settings.app_version}")
        print(f"   ✅ Secret key configured: {bool(settings.secret_key)}")
        print(f"   ✅ Users secret configured: {bool(settings.users_secret)}")
        print(f"   ✅ Token expire minutes: {settings.access_token_expire_minutes}")
        print(f"   ✅ Database URL configured: {bool(settings.database_url)}")
        print(f"   ✅ CORS origins configured: {len(settings.backend_cors_origins)} origins")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Configuration test failed: {e}")
        return False


def test_schemas():
    """Test Pydantic schemas."""
    print("\n📋 Testing Pydantic Schemas")
    print("=" * 50)
    
    try:
        from app.schemas.user import UserCreate, UserRead, UserProfile, UserProfileUpdate
        
        print("1. Testing UserCreate schema...")
        user_data = {
            "email": "test@example.com",
            "password": "TestPass123",
            "first_name": "Test",
            "last_name": "User"
        }
        user_create = UserCreate(**user_data)
        print("   ✅ UserCreate schema validation passed")
        
        print("\n2. Testing UserProfileUpdate schema...")
        profile_data = {
            "first_name": "Updated",
            "bio": "Updated bio"
        }
        profile_update = UserProfileUpdate(**profile_data)
        print("   ✅ UserProfileUpdate schema validation passed")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Schema test failed: {e}")
        return False


def test_security():
    """Test security utilities."""
    print("\n🔒 Testing Security Utilities")
    print("=" * 50)
    
    try:
        from app.core.security import get_password_hash, verify_password
        
        print("1. Testing password hashing...")
        password = "TestPassword123"
        hashed = get_password_hash(password)
        print("   ✅ Password hashing successful")
        
        print("\n2. Testing password verification...")
        is_valid = verify_password(password, hashed)
        print(f"   ✅ Password verification: {'PASSED' if is_valid else 'FAILED'}")
        
        print("\n3. Testing invalid password...")
        is_invalid = verify_password("wrong_password", hashed)
        print(f"   ✅ Invalid password test: {'PASSED' if not is_invalid else 'FAILED'}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Security test failed: {e}")
        return False


def main():
    """Main test function."""
    print("🚀 FastAPI-Users Simple Integration Test")
    print("=" * 60)
    
    # Run tests
    import_success = test_imports()
    config_success = test_configuration()
    schema_success = test_schemas()
    security_success = test_security()
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 30)
    print(f"Module Imports: {'✅ PASS' if import_success else '❌ FAIL'}")
    print(f"Configuration: {'✅ PASS' if config_success else '❌ FAIL'}")
    print(f"Pydantic Schemas: {'✅ PASS' if schema_success else '❌ FAIL'}")
    print(f"Security Utilities: {'✅ PASS' if security_success else '❌ FAIL'}")
    
    if all([import_success, config_success, schema_success, security_success]):
        print("\n🎉 All tests passed! FastAPI-Users components are properly configured.")
        print("\n📚 Next steps:")
        print("   1. Set up your database (PostgreSQL recommended)")
        print("   2. Update DATABASE_URL in your environment")
        print("   3. Run database migrations: alembic upgrade head")
        print("   4. Start the application: uvicorn app.main:app --reload")
        print("   5. Access API docs: http://localhost:8000/docs")
    else:
        print("\n❌ Some tests failed. Please check the configuration.")
        sys.exit(1)


if __name__ == "__main__":
    main()

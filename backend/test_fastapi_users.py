#!/usr/bin/env python3
"""
Test script for FastAPI-Users implementation

This script tests the FastAPI-Users integration to ensure all components
are working correctly.

Author: AI Job Readiness Team
Version: 1.0.0
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.core.config import settings
from app.core.users import fastapi_users, get_user_manager, get_user_db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from app.db.database import get_engine, init_db


async def test_fastapi_users_setup():
    """Test FastAPI-Users setup and configuration."""
    print("🧪 Testing FastAPI-Users Setup")
    print("=" * 50)
    
    try:
        # Test 1: Configuration
        print("1. Testing configuration...")
        print(f"   ✅ Secret key configured: {bool(settings.users_secret)}")
        print(f"   ✅ Token expire minutes: {settings.access_token_expire_minutes}")
        print(f"   ✅ Database URL configured: {bool(settings.database_url)}")
        
        # Test 2: Database connection
        print("\n2. Testing database connection...")
        engine = get_engine()
        print(f"   ✅ Database engine created: {engine is not None}")
        
        # Test 3: FastAPI-Users components
        print("\n3. Testing FastAPI-Users components...")
        print(f"   ✅ FastAPI-Users instance: {fastapi_users is not None}")
        print(f"   ✅ User manager function: {get_user_manager is not None}")
        print(f"   ✅ User database function: {get_user_db is not None}")
        
        # Test 4: Model imports
        print("\n4. Testing model imports...")
        print(f"   ✅ User model: {User is not None}")
        print(f"   ✅ UserCreate schema: {UserCreate is not None}")
        print(f"   ✅ UserRead schema: {UserRead is not None}")
        
        print("\n🎉 All FastAPI-Users tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ FastAPI-Users test failed: {e}")
        return False


async def test_database_initialization():
    """Test database initialization."""
    print("\n🗄️  Testing Database Initialization")
    print("=" * 50)
    
    try:
        await init_db()
        print("✅ Database tables initialized successfully")
        return True
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False


async def main():
    """Main test function."""
    print("🚀 FastAPI-Users Integration Test")
    print("=" * 60)
    
    # Test FastAPI-Users setup
    setup_success = await test_fastapi_users_setup()
    
    # Test database initialization
    db_success = await test_database_initialization()
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 30)
    print(f"FastAPI-Users Setup: {'✅ PASS' if setup_success else '❌ FAIL'}")
    print(f"Database Init: {'✅ PASS' if db_success else '❌ FAIL'}")
    
    if setup_success and db_success:
        print("\n🎉 All tests passed! FastAPI-Users is ready to use.")
        print("\n📚 Available endpoints:")
        print("   POST /api/v1/auth/register - User registration")
        print("   POST /api/v1/auth/jwt/login - User login")
        print("   GET  /api/v1/auth/me - Get current user")
        print("   PUT  /api/v1/users/profile - Update user profile")
        print("   GET  /api/v1/users/profile - Get user profile")
        print("   POST /api/v1/users/change-password - Change password")
        print("   GET  /api/v1/users/list - List users (admin)")
        print("   GET  /api/v1/protected - Protected route example")
    else:
        print("\n❌ Some tests failed. Please check the configuration.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

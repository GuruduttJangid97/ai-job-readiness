#!/usr/bin/env python3
"""
Simple Test Script for Role and User Models

This script tests the Role model and many-to-many relationship with User model
using existing data in the database.

Usage:
    python simple_test.py

Author: AI Job Readiness Team
Version: 1.0.0
"""

import asyncio
import sys
import os
from typing import List, Dict, Any

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.db.database import get_async_session_local, init_db
from app.models.user import User
from app.models.role import Role, UserRole


class SimpleRoleTester:
    """Simple tester for Role and User model system using existing data."""
    
    def __init__(self):
        self.session: AsyncSession = None
    
    async def setup(self):
        """Initialize database and create test session."""
        print("🔧 Setting up test environment...")
        
        # Initialize database
        await init_db()
        
        # Create session
        async_session = get_async_session_local()
        self.session = async_session()
        
        print("✅ Test environment ready")
    
    async def cleanup(self):
        """Clean up and close session."""
        if self.session:
            await self.session.close()
        print("✅ Test cleanup completed")
    
    async def test_existing_data(self):
        """Test with existing data in the database."""
        print("\n🧪 Testing with existing data...")
        
        # Test 1: Get all roles
        print("  📊 Testing role retrieval...")
        result = await self.session.execute(select(Role))
        roles = result.scalars().all()
        print(f"    ✅ Found {len(roles)} roles:")
        for role in roles:
            print(f"      - {role.name}: {role.description}")
            print(f"        Permissions: {role.get_permissions_list()}")
        
        # Test 2: Get all users
        print("\n  👥 Testing user retrieval...")
        result = await self.session.execute(select(User))
        users = result.scalars().all()
        print(f"    ✅ Found {len(users)} users:")
        for user in users:
            print(f"      - {user.email} ({user.full_name})")
        
        # Test 3: Get users with their roles
        print("\n  🔗 Testing user-role relationships...")
        result = await self.session.execute(
            select(User)
            .options(selectinload(User.roles).selectinload(UserRole.role))
            .limit(5)  # Limit to first 5 users for demo
        )
        users_with_roles = result.scalars().all()
        
        for user in users_with_roles:
            role_names = [ur.role.name for ur in user.roles if ur.is_active]
            print(f"      - {user.email}: {role_names}")
            
            # Test user role methods
            print(f"        - Has 'admin' role: {user.has_role('admin')}")
            print(f"        - Is admin: {user.is_admin()}")
            print(f"        - Full name: {user.full_name}")
        
        # Test 4: Role statistics
        print("\n  📈 Testing role statistics...")
        result = await self.session.execute(
            select(
                Role.name,
                Role.description,
                func.count(UserRole.id).label('user_count'),
                Role.is_active
            )
            .outerjoin(UserRole, Role.id == UserRole.role_id)
            .where(UserRole.is_active == True)
            .group_by(Role.id, Role.name, Role.description, Role.is_active)
            .order_by(func.count(UserRole.id).desc())
        )
        
        role_stats = result.fetchall()
        print("    Role Statistics:")
        print("    Role Name        | Description           | User Count | Active")
        print("    " + "-" * 65)
        for stat in role_stats:
            print(f"    {stat[0]:<15} | {stat[1]:<20} | {stat[2]:<10} | {stat[3]}")
        
        # Test 5: Permission management
        print("\n  🔐 Testing permission management...")
        if roles:
            test_role = roles[0]  # Use first role
            print(f"    Testing with role: {test_role.name}")
            print(f"    Current permissions: {test_role.get_permissions_list()}")
            
            # Test permission checking
            if test_role.get_permissions_list():
                test_permission = test_role.get_permissions_list()[0]
                print(f"    Has '{test_permission}': {test_role.has_permission(test_permission)}")
            
            # Test adding a permission
            test_role.add_permission("test:permission")
            await self.session.commit()
            await self.session.refresh(test_role)
            print(f"    After adding 'test:permission': {test_role.get_permissions_list()}")
            
            # Test removing the permission
            test_role.remove_permission("test:permission")
            await self.session.commit()
            await self.session.refresh(test_role)
            print(f"    After removing 'test:permission': {test_role.get_permissions_list()}")
        
        # Test 6: Serialization
        print("\n  📄 Testing serialization...")
        if roles:
            role_dict = roles[0].to_dict()
            print(f"    Role serialization ({roles[0].name}):")
            print(f"      - ID: {role_dict['id']}")
            print(f"      - Name: {role_dict['name']}")
            print(f"      - Active: {role_dict['is_active']}")
            print(f"      - Permissions: {role_dict['permissions']}")
        
        if users:
            user_dict = users[0].to_dict()
            print(f"    User serialization ({users[0].email}):")
            print(f"      - ID: {user_dict['id']}")
            print(f"      - Email: {user_dict['email']}")
            print(f"      - Full Name: {user_dict['full_name']}")
            print(f"      - Active: {user_dict['is_active']}")
            print(f"      - Roles: {user_dict['roles']}")
        
        print("\n  ✅ All tests completed successfully!")
    
    async def run_tests(self):
        """Run all tests."""
        print("🚀 Starting Simple Role System Tests")
        print("=" * 50)
        
        try:
            await self.setup()
            await self.test_existing_data()
            
            print("\n" + "=" * 50)
            print("🎉 All tests passed successfully!")
            print("✅ Role model and User-Role relationship working correctly")
            
        except Exception as e:
            print(f"\n❌ Test failed with error: {e}")
            import traceback
            traceback.print_exc()
            raise
        
        finally:
            await self.cleanup()


async def main():
    """Main function to run the tests."""
    tester = SimpleRoleTester()
    await tester.run_tests()


if __name__ == "__main__":
    asyncio.run(main())

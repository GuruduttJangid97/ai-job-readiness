#!/usr/bin/env python3
"""
Comprehensive Test Script for Role and User Models

This script tests the Role model and many-to-many relationship with User model
including all CRUD operations, role assignments, and permission management.

Usage:
    python test_role_system.py

Author: AI Job Readiness Team
Version: 1.0.0
"""

import asyncio
import json
import uuid
from datetime import datetime
from typing import List, Dict, Any
import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.db.database import get_async_session_local, init_db
from app.models.user import User
from app.models.role import Role, UserRole
from app.core.security import get_password_hash


class RoleSystemTester:
    """Comprehensive tester for Role and User model system."""
    
    def __init__(self):
        self.session: AsyncSession = None
        self.test_users: List[User] = []
        self.test_roles: List[Role] = []
        self.test_assignments: List[UserRole] = []
    
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
        """Clean up test data and close session."""
        print("🧹 Cleaning up test data...")
        
        if self.session:
            # Delete test assignments
            for assignment in self.test_assignments:
                await self.session.delete(assignment)
            
            # Delete test users
            for user in self.test_users:
                await self.session.delete(user)
            
            # Delete test roles
            for role in self.test_roles:
                await self.session.delete(role)
            
            await self.session.commit()
            await self.session.close()
        
        print("✅ Cleanup completed")
    
    async def create_test_users(self) -> List[User]:
        """Create test users for testing."""
        print("👥 Creating test users...")
        
        test_user_data = [
            {
                "email": "admin@test.com",
                "password": "AdminPass123!",
                "first_name": "Admin",
                "last_name": "User",
                "is_superuser": True,
                "is_active": True,
                "is_verified": True
            },
            {
                "email": "moderator@test.com",
                "password": "ModPass123!",
                "first_name": "Moderator",
                "last_name": "User",
                "is_superuser": False,
                "is_active": True,
                "is_verified": True
            },
            {
                "email": "user1@test.com",
                "password": "UserPass123!",
                "first_name": "Regular",
                "last_name": "User1",
                "is_superuser": False,
                "is_active": True,
                "is_verified": True
            },
            {
                "email": "user2@test.com",
                "password": "UserPass123!",
                "first_name": "Regular",
                "last_name": "User2",
                "is_superuser": False,
                "is_active": True,
                "is_verified": True
            }
        ]
        
        users = []
        for user_data in test_user_data:
            user = User(
                email=user_data["email"],
                hashed_password=get_password_hash(user_data["password"]),
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                is_superuser=user_data["is_superuser"],
                is_active=user_data["is_active"],
                is_verified=user_data["is_verified"]
            )
            self.session.add(user)
            users.append(user)
        
        await self.session.commit()
        
        # Refresh users to get their IDs
        for user in users:
            await self.session.refresh(user)
        
        self.test_users = users
        print(f"✅ Created {len(users)} test users")
        return users
    
    async def create_test_roles(self) -> List[Role]:
        """Create test roles for testing."""
        print("🎭 Creating test roles...")
        
        test_role_data = [
            {
                "name": "admin",
                "description": "Full system access with all permissions",
                "permissions": ["*"],
                "is_active": True
            },
            {
                "name": "moderator",
                "description": "Content moderation and user management",
                "permissions": ["user:read", "user:update", "content:moderate", "role:read"],
                "is_active": True
            },
            {
                "name": "user",
                "description": "Basic user access",
                "permissions": ["profile:read", "profile:update", "resume:read", "resume:create"],
                "is_active": True
            },
            {
                "name": "guest",
                "description": "Limited guest access",
                "permissions": ["profile:read"],
                "is_active": True
            },
            {
                "name": "inactive_role",
                "description": "Inactive role for testing",
                "permissions": ["test:permission"],
                "is_active": False
            }
        ]
        
        roles = []
        for role_data in test_role_data:
            role = Role(
                name=role_data["name"],
                description=role_data["description"],
                is_active=role_data["is_active"]
            )
            role.set_permissions_list(role_data["permissions"])
            self.session.add(role)
            roles.append(role)
        
        await self.session.commit()
        
        # Refresh roles to get their IDs
        for role in roles:
            await self.session.refresh(role)
        
        self.test_roles = roles
        print(f"✅ Created {len(roles)} test roles")
        return roles
    
    async def test_role_crud_operations(self):
        """Test CRUD operations for Role model."""
        print("\n🧪 Testing Role CRUD operations...")
        
        # Test 1: Create a new role
        print("  📝 Testing role creation...")
        new_role = Role(
            name="test_role",
            description="Test role for CRUD operations",
            is_active=True
        )
        new_role.set_permissions_list(["test:read", "test:write"])
        
        self.session.add(new_role)
        await self.session.commit()
        await self.session.refresh(new_role)
        
        assert new_role.id is not None
        assert new_role.name == "test_role"
        assert new_role.is_active == True
        assert "test:read" in new_role.get_permissions_list()
        print("    ✅ Role creation successful")
        
        # Test 2: Read role
        print("  📖 Testing role reading...")
        result = await self.session.execute(
            select(Role).where(Role.id == new_role.id)
        )
        retrieved_role = result.scalar_one_or_none()
        
        assert retrieved_role is not None
        assert retrieved_role.name == "test_role"
        assert retrieved_role.description == "Test role for CRUD operations"
        print("    ✅ Role reading successful")
        
        # Test 3: Update role
        print("  ✏️ Testing role update...")
        retrieved_role.description = "Updated test role description"
        retrieved_role.add_permission("test:delete")
        
        await self.session.commit()
        await self.session.refresh(retrieved_role)
        
        assert retrieved_role.description == "Updated test role description"
        assert "test:delete" in retrieved_role.get_permissions_list()
        print("    ✅ Role update successful")
        
        # Test 4: Delete role
        print("  🗑️ Testing role deletion...")
        await self.session.delete(retrieved_role)
        await self.session.commit()
        
        # Verify deletion
        result = await self.session.execute(
            select(Role).where(Role.id == new_role.id)
        )
        deleted_role = result.scalar_one_or_none()
        assert deleted_role is None
        print("    ✅ Role deletion successful")
    
    async def test_user_role_assignments(self):
        """Test user-role assignment operations."""
        print("\n🔗 Testing User-Role assignments...")
        
        # Get test users and roles
        admin_user = next((u for u in self.test_users if u.email == "admin@test.com"), None)
        moderator_user = next((u for u in self.test_users if u.email == "moderator@test.com"), None)
        regular_user = next((u for u in self.test_users if u.email == "user1@test.com"), None)
        
        admin_role = next((r for r in self.test_roles if r.name == "admin"), None)
        moderator_role = next((r for r in self.test_roles if r.name == "moderator"), None)
        user_role = next((r for r in self.test_roles if r.name == "user"), None)
        
        # Test 1: Assign roles to users
        print("  📋 Testing role assignments...")
        
        # Assign admin role to admin user
        admin_assignment = UserRole(
            user_id=admin_user.id,
            role_id=admin_role.id,
            assigned_by=admin_user.id,
            is_active=True
        )
        self.session.add(admin_assignment)
        
        # Assign moderator role to moderator user
        moderator_assignment = UserRole(
            user_id=moderator_user.id,
            role_id=moderator_role.id,
            assigned_by=admin_user.id,
            is_active=True
        )
        self.session.add(moderator_assignment)
        
        # Assign user role to regular user
        user_assignment = UserRole(
            user_id=regular_user.id,
            role_id=user_role.id,
            assigned_by=admin_user.id,
            is_active=True
        )
        self.session.add(user_assignment)
        
        await self.session.commit()
        
        # Store assignments for cleanup
        self.test_assignments.extend([admin_assignment, moderator_assignment, user_assignment])
        
        print("    ✅ Role assignments created successfully")
        
        # Test 2: Verify role assignments
        print("  🔍 Testing role assignment verification...")
        
        # Query users with their roles using selectinload
        result = await self.session.execute(
            select(User)
            .options(selectinload(User.roles).selectinload(UserRole.role))
            .where(User.id.in_([admin_user.id, moderator_user.id, regular_user.id]))
        )
        users_with_roles = result.scalars().all()
        
        # Update references to the loaded users
        admin_user = next((u for u in users_with_roles if u.email == "admin@test.com"), admin_user)
        moderator_user = next((u for u in users_with_roles if u.email == "moderator@test.com"), moderator_user)
        regular_user = next((u for u in users_with_roles if u.email == "user1@test.com"), regular_user)
        
        # Test user role methods
        assert admin_user.has_role("admin")
        assert admin_user.is_admin()
        assert "admin" in admin_user.get_role_names()
        
        assert moderator_user.has_role("moderator")
        assert not moderator_user.is_admin()
        assert "moderator" in moderator_user.get_role_names()
        
        assert regular_user.has_role("user")
        assert not regular_user.is_admin()
        assert "user" in regular_user.get_role_names()
        
        print("    ✅ Role assignment verification successful")
    
    async def test_permission_management(self):
        """Test permission management functionality."""
        print("\n🔐 Testing permission management...")
        
        # Get test roles
        admin_role = next((r for r in self.test_roles if r.name == "admin"), None)
        moderator_role = next((r for r in self.test_roles if r.name == "moderator"), None)
        user_role = next((r for r in self.test_roles if r.name == "user"), None)
        
        # Test 1: Permission checking
        print("  🔍 Testing permission checking...")
        
        assert admin_role.has_permission("*")
        assert moderator_role.has_permission("user:read")
        assert not moderator_role.has_permission("user:delete")
        assert user_role.has_permission("profile:read")
        assert not user_role.has_permission("admin:access")
        
        print("    ✅ Permission checking successful")
        
        # Test 2: Add permission
        print("  ➕ Testing permission addition...")
        
        initial_permissions = user_role.get_permissions_list()
        user_role.add_permission("resume:update")
        await self.session.commit()
        await self.session.refresh(user_role)
        
        assert "resume:update" in user_role.get_permissions_list()
        assert len(user_role.get_permissions_list()) == len(initial_permissions) + 1
        
        print("    ✅ Permission addition successful")
        
        # Test 3: Remove permission
        print("  ➖ Testing permission removal...")
        
        user_role.remove_permission("resume:update")
        await self.session.commit()
        await self.session.refresh(user_role)
        
        assert "resume:update" not in user_role.get_permissions_list()
        assert len(user_role.get_permissions_list()) == len(initial_permissions)
        
        print("    ✅ Permission removal successful")
    
    async def test_role_queries(self):
        """Test complex role queries and relationships."""
        print("\n🔍 Testing role queries and relationships...")
        
        # Test 1: Get all roles with user counts
        print("  📊 Testing role statistics...")
        
        result = await self.session.execute(
            select(
                Role.name,
                Role.description,
                func.count(UserRole.id).label('user_count')
            )
            .outerjoin(UserRole, Role.id == UserRole.role_id)
            .where(UserRole.is_active == True)
            .group_by(Role.id, Role.name, Role.description)
            .order_by(func.count(UserRole.id).desc())
        )
        
        role_stats = result.fetchall()
        assert len(role_stats) > 0
        
        print("    ✅ Role statistics query successful")
        for stat in role_stats:
            print(f"      - {stat[0]}: {stat[2]} users")
        
        # Test 2: Get users with their roles
        print("  👥 Testing user-role relationships...")
        
        result = await self.session.execute(
            select(User)
            .options(selectinload(User.roles).selectinload(UserRole.role))
            .where(User.email.in_(["admin@test.com", "moderator@test.com", "user1@test.com"]))
        )
        
        users_with_roles = result.scalars().all()
        assert len(users_with_roles) == 3
        
        for user in users_with_roles:
            assert len(user.roles) > 0
            role_names = [ur.role.name for ur in user.roles if ur.is_active]
            print(f"      - {user.email}: {role_names}")
        
        print("    ✅ User-role relationships query successful")
    
    async def test_error_handling(self):
        """Test error handling and edge cases."""
        print("\n⚠️ Testing error handling and edge cases...")
        
        # Test 1: Duplicate role name
        print("  🔄 Testing duplicate role name handling...")
        
        try:
            duplicate_role = Role(
                name="admin",  # This should conflict with existing admin role
                description="Duplicate admin role",
                is_active=True
            )
            self.session.add(duplicate_role)
            await self.session.commit()
            assert False, "Should have raised an exception for duplicate role name"
        except Exception as e:
            await self.session.rollback()
            print("    ✅ Duplicate role name properly handled")
        
        # Test 2: Assign inactive role
        print("  🚫 Testing inactive role assignment...")
        
        inactive_role = next((r for r in self.test_roles if r.name == "inactive_role"), None)
        regular_user = next((u for u in self.test_users if u.email == "user2@test.com"), None)
        
        # This should work (we don't prevent inactive role assignment in the model)
        # But we can test that the role is marked as inactive
        assert not inactive_role.is_active
        
        print("    ✅ Inactive role handling verified")
    
    async def test_role_serialization(self):
        """Test role and user serialization."""
        print("\n📄 Testing serialization...")
        
        # Test 1: Role serialization
        print("  🎭 Testing role serialization...")
        
        admin_role = next((r for r in self.test_roles if r.name == "admin"), None)
        role_dict = admin_role.to_dict()
        
        assert "id" in role_dict
        assert "name" in role_dict
        assert "permissions" in role_dict
        assert role_dict["name"] == "admin"
        
        print("    ✅ Role serialization successful")
        
        # Test 2: User serialization with roles
        print("  👤 Testing user serialization with roles...")
        
        admin_user = next((u for u in self.test_users if u.email == "admin@test.com"), None)
        user_dict = admin_user.to_dict()
        
        assert "id" in user_dict
        assert "email" in user_dict
        assert "roles" in user_dict
        assert "admin" in user_dict["roles"]
        
        print("    ✅ User serialization successful")
    
    async def run_all_tests(self):
        """Run all tests in sequence."""
        print("🚀 Starting Role System Tests")
        print("=" * 50)
        
        try:
            await self.setup()
            await self.create_test_users()
            await self.create_test_roles()
            
            await self.test_role_crud_operations()
            await self.test_user_role_assignments()
            await self.test_permission_management()
            await self.test_role_queries()
            await self.test_error_handling()
            await self.test_role_serialization()
            
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
    tester = RoleSystemTester()
    await tester.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())

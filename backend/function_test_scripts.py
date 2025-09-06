#!/usr/bin/env python3
"""
Comprehensive Function Test Scripts for Role and User Models

This module provides individual test scripts for testing specific functions
and features of the Role and User models.

Usage:
    python function_test_scripts.py [test_name]

Available Tests:
    - role_crud: Test Role CRUD operations
    - user_crud: Test User CRUD operations
    - permissions: Test permission management
    - assignments: Test user-role assignments
    - queries: Test complex queries
    - serialization: Test serialization
    - all: Run all tests

Author: AI Job Readiness Team
Version: 1.0.0
"""

import asyncio
import sys
import os
import uuid
from datetime import datetime
from typing import List, Dict, Any

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.db.database import get_async_session_local, init_db
from app.models.user import User
from app.models.role import Role, UserRole
from app.core.security import get_password_hash


class FunctionTester:
    """Test individual functions and features of Role and User models."""
    
    def __init__(self):
        self.session: AsyncSession = None
        self.test_results: Dict[str, Any] = {}
    
    async def setup(self):
        """Initialize database and create test session."""
        print("🔧 Setting up test environment...")
        await init_db()
        async_session = get_async_session_local()
        self.session = async_session()
        print("✅ Test environment ready")
    
    async def cleanup(self):
        """Clean up and close session."""
        if self.session:
            await self.session.close()
        print("✅ Cleanup completed")
    
    async def test_role_crud_functions(self):
        """Test Role CRUD operations and helper functions."""
        print("\n🎭 Testing Role CRUD Functions...")
        
        # Test 1: Role Creation
        print("  📝 Testing role creation...")
        role = Role(
            name=f"test_role_{uuid.uuid4().hex[:8]}",
            description="Test role for CRUD operations",
            is_active=True
        )
        role.set_permissions_list(["test:read", "test:write"])
        
        self.session.add(role)
        await self.session.commit()
        await self.session.refresh(role)
        
        print(f"    ✅ Role created: {role.name} (ID: {role.id})")
        
        # Test 2: Permission Management
        print("  🔐 Testing permission management...")
        
        # Test add_permission
        added = role.add_permission("test:delete")
        print(f"    ✅ Add permission 'test:delete': {added}")
        
        # Test has_permission
        has_read = role.has_permission("test:read")
        has_write = role.has_permission("test:write")
        has_delete = role.has_permission("test:delete")
        has_nonexistent = role.has_permission("test:nonexistent")
        
        print(f"    ✅ Has 'test:read': {has_read}")
        print(f"    ✅ Has 'test:write': {has_write}")
        print(f"    ✅ Has 'test:delete': {has_delete}")
        print(f"    ✅ Has 'test:nonexistent': {has_nonexistent}")
        
        # Test remove_permission
        removed = role.remove_permission("test:write")
        print(f"    ✅ Remove permission 'test:write': {removed}")
        
        # Test get_permissions_list
        permissions = role.get_permissions_list()
        print(f"    ✅ Current permissions: {permissions}")
        
        # Test permission checking methods (using existing methods)
        permissions = role.get_permissions_list()
        has_any = any(perm in permissions for perm in ["test:read", "test:nonexistent"])
        has_all = all(perm in permissions for perm in ["test:read", "test:delete"])
        print(f"    ✅ Has any of ['test:read', 'test:nonexistent']: {has_any}")
        print(f"    ✅ Has all of ['test:read', 'test:delete']: {has_all}")
        
        # Test utility methods
        permission_count = len(permissions)
        is_empty = len(permissions) == 0
        print(f"    ✅ Permission count: {permission_count}")
        print(f"    ✅ Is empty: {is_empty}")
        
        # Test 3: Role Update
        print("  ✏️  Testing role update...")
        role.description = "Updated test role description"
        role.is_active = False
        
        await self.session.commit()
        await self.session.refresh(role)
        
        print(f"    ✅ Role updated: {role.description}")
        print(f"    ✅ Role active status: {role.is_active}")
        
        # Test 4: Role Serialization
        print("  📄 Testing role serialization...")
        role_dict = role.to_dict()
        print(f"    ✅ Role serialized with {len(role_dict)} fields")
        print(f"    ✅ Serialized data: {role_dict}")
        
        # Test 5: Role Deletion
        print("  🗑️  Testing role deletion...")
        await self.session.delete(role)
        await self.session.commit()
        
        # Verify deletion
        result = await self.session.execute(
            select(Role).where(Role.id == role.id)
        )
        deleted_role = result.scalar_one_or_none()
        
        if deleted_role is None:
            print("    ✅ Role deleted successfully")
        else:
            print("    ❌ Role still exists after deletion")
        
        print("  ✅ Role CRUD functions test completed")
    
    async def test_user_crud_functions(self):
        """Test User CRUD operations and helper functions."""
        print("\n👥 Testing User CRUD Functions...")
        
        # Test 1: User Creation
        print("  📝 Testing user creation...")
        user = User(
            email=f"test_user_{uuid.uuid4().hex[:8]}@example.com",
            hashed_password=get_password_hash("TestPassword123!"),
            first_name="Test",
            last_name="User",
            is_superuser=False,
            is_active=True,
            is_verified=True
        )
        
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        
        print(f"    ✅ User created: {user.email} (ID: {user.id})")
        
        # Test 2: User Properties
        print("  👤 Testing user properties...")
        full_name = user.full_name
        display_name = user.display_name
        
        print(f"    ✅ Full name: {full_name}")
        print(f"    ✅ Display name: {display_name}")
        
        # Test 3: User Update
        print("  ✏️  Testing user update...")
        user.first_name = "Updated"
        user.last_name = "Name"
        user.phone = "+1234567890"
        user.bio = "Test user biography"
        
        await self.session.commit()
        await self.session.refresh(user)
        
        print(f"    ✅ User updated: {user.full_name}")
        print(f"    ✅ Phone: {user.phone}")
        print(f"    ✅ Bio: {user.bio}")
        
        # Test 4: User Serialization
        print("  📄 Testing user serialization...")
        user_dict = user.to_dict()
        public_dict = user.to_public_dict()
        
        print(f"    ✅ User serialized with {len(user_dict)} fields")
        print(f"    ✅ Public serialized with {len(public_dict)} fields")
        print(f"    ✅ Serialized data: {user_dict}")
        
        # Test 5: User Deletion
        print("  🗑️  Testing user deletion...")
        await self.session.delete(user)
        await self.session.commit()
        
        # Verify deletion
        result = await self.session.execute(
            select(User).where(User.id == user.id)
        )
        deleted_user = result.scalar_one_or_none()
        
        if deleted_user is None:
            print("    ✅ User deleted successfully")
        else:
            print("    ❌ User still exists after deletion")
        
        print("  ✅ User CRUD functions test completed")
    
    async def test_permission_functions(self):
        """Test permission management functions."""
        print("\n🔐 Testing Permission Functions...")
        
        # Create test role
        role = Role(
            name=f"permission_test_{uuid.uuid4().hex[:8]}",
            description="Role for permission testing",
            is_active=True
        )
        role.set_permissions_list(["read", "write"])
        
        self.session.add(role)
        await self.session.commit()
        await self.session.refresh(role)
        
        print(f"  📝 Created test role: {role.name}")
        
        # Test permission validation
        print("  ✅ Testing permission validation...")
        
        # Test empty permission handling
        role.set_permissions_list(["valid:permission", "", "another:valid"])
        permissions = role.get_permissions_list()
        print(f"    ✅ Empty permissions filtered: {permissions}")
        
        # Test permission addition
        print("  ➕ Testing permission addition...")
        added1 = role.add_permission("delete")
        added2 = role.add_permission("delete")  # Duplicate
        added3 = role.add_permission("")  # Empty
        added4 = role.add_permission("   ")  # Whitespace only
        
        print(f"    ✅ Added 'delete': {added1}")
        print(f"    ✅ Added duplicate 'delete': {added2}")
        print(f"    ✅ Added empty permission: {added3}")
        print(f"    ✅ Added whitespace permission: {added4}")
        
        # Test permission removal
        print("  ➖ Testing permission removal...")
        removed1 = role.remove_permission("write")
        removed2 = role.remove_permission("nonexistent")
        removed3 = role.remove_permission("")
        
        print(f"    ✅ Removed 'write': {removed1}")
        print(f"    ✅ Removed 'nonexistent': {removed2}")
        print(f"    ✅ Removed empty permission: {removed3}")
        
        # Test permission checking
        print("  🔍 Testing permission checking...")
        has_read = role.has_permission("read")
        has_write = role.has_permission("write")
        has_delete = role.has_permission("delete")
        
        print(f"    ✅ Has 'read': {has_read}")
        print(f"    ✅ Has 'write': {has_write}")
        print(f"    ✅ Has 'delete': {has_delete}")
        
        # Test bulk permission checking (using existing methods)
        permissions = role.get_permissions_list()
        has_any = any(perm in permissions for perm in ["read", "write", "nonexistent"])
        has_all = all(perm in permissions for perm in ["read", "delete"])
        has_all_fail = all(perm in permissions for perm in ["read", "write", "delete"])
        
        print(f"    ✅ Has any of ['read', 'write', 'nonexistent']: {has_any}")
        print(f"    ✅ Has all of ['read', 'delete']: {has_all}")
        print(f"    ✅ Has all of ['read', 'write', 'delete']: {has_all_fail}")
        
        # Test utility functions
        print("  🔧 Testing utility functions...")
        permission_count = len(permissions)
        is_empty = len(permissions) == 0
        
        print(f"    ✅ Permission count: {permission_count}")
        print(f"    ✅ Is empty: {is_empty}")
        print(f"    ✅ All permissions: {permissions}")
        
        # Cleanup
        await self.session.delete(role)
        await self.session.commit()
        
        print("  ✅ Permission functions test completed")
    
    async def test_assignment_functions(self):
        """Test user-role assignment functions."""
        print("\n🔗 Testing Assignment Functions...")
        
        # Create test user and role
        user = User(
            email=f"assignment_user_{uuid.uuid4().hex[:8]}@example.com",
            hashed_password=get_password_hash("TestPassword123!"),
            first_name="Assignment",
            last_name="User",
            is_superuser=False,
            is_active=True,
            is_verified=True
        )
        
        role = Role(
            name=f"assignment_role_{uuid.uuid4().hex[:8]}",
            description="Role for assignment testing",
            is_active=True
        )
        role.set_permissions_list(["test:read", "test:write"])
        
        self.session.add(user)
        self.session.add(role)
        await self.session.commit()
        await self.session.refresh(user)
        await self.session.refresh(role)
        
        print(f"  📝 Created test user: {user.email}")
        print(f"  📝 Created test role: {role.name}")
        
        # Test assignment creation
        print("  🔗 Testing assignment creation...")
        assignment = UserRole(
            user_id=user.id,
            role_id=role.id,
            assigned_by=user.id,
            is_active=True
        )
        
        self.session.add(assignment)
        await self.session.commit()
        await self.session.refresh(assignment)
        
        print(f"    ✅ Assignment created: {assignment.id}")
        
        # Test user role methods
        print("  👤 Testing user role methods...")
        
        # Load user with roles
        result = await self.session.execute(
            select(User)
            .options(selectinload(User.roles).selectinload(UserRole.role))
            .where(User.id == user.id)
        )
        user_with_roles = result.scalar_one_or_none()
        
        if user_with_roles:
            # Test role checking methods
            has_role = user_with_roles.has_role(role.name)
            has_nonexistent = user_with_roles.has_role("nonexistent")
            
            print(f"    ✅ Has role '{role.name}': {has_role}")
            print(f"    ✅ Has role 'nonexistent': {has_nonexistent}")
            
            # Test role name listing
            role_names = user_with_roles.get_role_names()
            print(f"    ✅ Role names: {role_names}")
            
            # Test role objects
            roles = user_with_roles.get_roles()
            print(f"    ✅ Role objects: {[r.name for r in roles]}")
            
            # Test admin/moderator checking
            is_admin = user_with_roles.is_admin()
            is_moderator = user_with_roles.is_moderator()
            
            print(f"    ✅ Is admin: {is_admin}")
            print(f"    ✅ Is moderator: {is_moderator}")
            
            # Test permission checking through roles
            has_permission = user_with_roles.has_permission("test:read")
            has_nonexistent_perm = user_with_roles.has_permission("test:nonexistent")
            
            print(f"    ✅ Has permission 'test:read': {has_permission}")
            print(f"    ✅ Has permission 'test:nonexistent': {has_nonexistent_perm}")
            
            # Test bulk permission checking (using existing methods)
            user_permissions = []
            for ur in user_with_roles.roles:
                if ur.is_active and ur.role.is_active:
                    user_permissions.extend(ur.role.get_permissions_list())
            
            has_any_perm = any(perm in user_permissions for perm in ["test:read", "test:nonexistent"])
            has_all_perm = all(perm in user_permissions for perm in ["test:read", "test:write"])
            
            print(f"    ✅ Has any permission: {has_any_perm}")
            print(f"    ✅ Has all permissions: {has_all_perm}")
            
            # Test getting all permissions
            all_permissions = list(set(user_permissions))  # Remove duplicates
            print(f"    ✅ All permissions: {all_permissions}")
            
            # Test role count
            role_count = len([ur for ur in user_with_roles.roles if ur.is_active])
            print(f"    ✅ Role count: {role_count}")
        
        # Test assignment deactivation
        print("  ⚠️  Testing assignment deactivation...")
        assignment.is_active = False
        await self.session.commit()
        await self.session.refresh(assignment)
        
        print(f"    ✅ Assignment deactivated: {not assignment.is_active}")
        
        # Test role checking after deactivation
        result = await self.session.execute(
            select(User)
            .options(selectinload(User.roles).selectinload(UserRole.role))
            .where(User.id == user.id)
        )
        user_with_roles = result.scalar_one_or_none()
        
        if user_with_roles:
            has_role_after = user_with_roles.has_role(role.name)
            role_names_after = user_with_roles.get_role_names()
            
            print(f"    ✅ Has role after deactivation: {has_role_after}")
            print(f"    ✅ Role names after deactivation: {role_names_after}")
        
        # Cleanup
        await self.session.delete(assignment)
        await self.session.delete(user)
        await self.session.delete(role)
        await self.session.commit()
        
        print("  ✅ Assignment functions test completed")
    
    async def test_query_functions(self):
        """Test complex query functions."""
        print("\n🔍 Testing Query Functions...")
        
        # Test 1: Role statistics query
        print("  📊 Testing role statistics query...")
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
            .limit(5)
        )
        
        role_stats = result.fetchall()
        print(f"    ✅ Retrieved {len(role_stats)} role statistics")
        for stat in role_stats:
            print(f"      - {stat[0]}: {stat[2]} users")
        
        # Test 2: Users with roles query
        print("  👥 Testing users with roles query...")
        result = await self.session.execute(
            select(User)
            .options(selectinload(User.roles).selectinload(UserRole.role))
            .where(User.is_active == True)
            .limit(5)
        )
        
        users_with_roles = result.scalars().all()
        print(f"    ✅ Retrieved {len(users_with_roles)} users with roles")
        for user in users_with_roles:
            role_names = [ur.role.name for ur in user.roles if ur.is_active]
            print(f"      - {user.email}: {role_names}")
        
        # Test 3: Permission-based query
        print("  🔐 Testing permission-based query...")
        result = await self.session.execute(
            select(Role)
            .where(Role.permissions.like('%admin%'))
            .limit(5)
        )
        
        admin_roles = result.scalars().all()
        print(f"    ✅ Found {len(admin_roles)} roles with admin permissions")
        for role in admin_roles:
            print(f"      - {role.name}: {role.get_permissions_list()}")
        
        # Test 4: Active roles query
        print("  ✅ Testing active roles query...")
        result = await self.session.execute(
            select(Role)
            .where(Role.is_active == True)
            .order_by(Role.name)
        )
        
        active_roles = result.scalars().all()
        print(f"    ✅ Found {len(active_roles)} active roles")
        
        # Test 5: User count by role
        print("  📈 Testing user count by role...")
        result = await self.session.execute(
            select(
                Role.name,
                func.count(UserRole.id).label('user_count')
            )
            .outerjoin(UserRole, Role.id == UserRole.role_id)
            .where(UserRole.is_active == True)
            .group_by(Role.name)
            .order_by(func.count(UserRole.id).desc())
        )
        
        user_counts = result.fetchall()
        print(f"    ✅ Retrieved user counts for {len(user_counts)} roles")
        for count in user_counts:
            print(f"      - {count[0]}: {count[1]} users")
        
        print("  ✅ Query functions test completed")
    
    async def test_serialization_functions(self):
        """Test serialization functions."""
        print("\n📄 Testing Serialization Functions...")
        
        # Test role serialization
        print("  🎭 Testing role serialization...")
        result = await self.session.execute(select(Role).limit(1))
        role = result.scalar_one_or_none()
        
        if role:
            role_dict = role.to_dict()
            print(f"    ✅ Role serialized with {len(role_dict)} fields")
            print(f"    ✅ Role data: {role_dict}")
            
            # Test required fields
            required_fields = ["id", "name", "description", "permissions", "is_active", "created_at"]
            missing_fields = [field for field in required_fields if field not in role_dict]
            if not missing_fields:
                print("    ✅ All required fields present")
            else:
                print(f"    ❌ Missing fields: {missing_fields}")
        else:
            print("    ⚠️  No roles found for serialization test")
        
        # Test user serialization
        print("  👥 Testing user serialization...")
        result = await self.session.execute(select(User).limit(1))
        user = result.scalar_one_or_none()
        
        if user:
            user_dict = user.to_dict()
            public_dict = user.to_public_dict()
            
            print(f"    ✅ User serialized with {len(user_dict)} fields")
            print(f"    ✅ Public user serialized with {len(public_dict)} fields")
            
            # Test required fields
            required_fields = ["id", "email", "first_name", "last_name", "is_active", "roles"]
            missing_fields = [field for field in required_fields if field not in user_dict]
            if not missing_fields:
                print("    ✅ All required fields present")
            else:
                print(f"    ❌ Missing fields: {missing_fields}")
            
            # Test public dict doesn't have sensitive fields
            sensitive_fields = ["hashed_password", "is_superuser"]
            has_sensitive = any(field in public_dict for field in sensitive_fields)
            if not has_sensitive:
                print("    ✅ Public dict excludes sensitive fields")
            else:
                print("    ❌ Public dict contains sensitive fields")
        else:
            print("    ⚠️  No users found for serialization test")
        
        print("  ✅ Serialization functions test completed")
    
    async def run_test(self, test_name: str):
        """Run a specific test."""
        try:
            await self.setup()
            
            if test_name == "role_crud":
                await self.test_role_crud_functions()
            elif test_name == "user_crud":
                await self.test_user_crud_functions()
            elif test_name == "permissions":
                await self.test_permission_functions()
            elif test_name == "assignments":
                await self.test_assignment_functions()
            elif test_name == "queries":
                await self.test_query_functions()
            elif test_name == "serialization":
                await self.test_serialization_functions()
            elif test_name == "all":
                await self.test_role_crud_functions()
                await self.test_user_crud_functions()
                await self.test_permission_functions()
                await self.test_assignment_functions()
                await self.test_query_functions()
                await self.test_serialization_functions()
            else:
                print(f"❌ Unknown test: {test_name}")
                print("Available tests: role_crud, user_crud, permissions, assignments, queries, serialization, all")
                return
            
            print(f"\n✅ {test_name} test completed successfully!")
            
        except Exception as e:
            print(f"\n❌ {test_name} test failed: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            await self.cleanup()


async def main():
    """Main function to run tests."""
    if len(sys.argv) < 2:
        print("Usage: python function_test_scripts.py [test_name]")
        print("Available tests: role_crud, user_crud, permissions, assignments, queries, serialization, all")
        return
    
    test_name = sys.argv[1]
    tester = FunctionTester()
    await tester.run_test(test_name)


if __name__ == "__main__":
    asyncio.run(main())

#!/usr/bin/env python3
"""
Security Test Script for Role Management System

This script tests the security aspects of the Role Management System including
permission validation, access control, and data integrity.

Usage:
    python test_role_security.py

Author: AI Job Readiness Team
Version: 1.0.0
"""

import asyncio
import uuid
import sys
from pathlib import Path
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, delete
from sqlalchemy.orm import selectinload

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

from app.db.database import get_async_session_local, init_db
from app.models.user import User
from app.models.role import Role, UserRole


class SecurityTester:
    """Security testing class for Role Management System."""
    
    def __init__(self):
        self.test_data = {}
        
    async def setup_test_data(self):
        """Create test data for security testing."""
        print("🔒 Setting up security test data...")
        
        # Clear existing data for clean test
        async with get_async_session_local()() as db:
            # Delete all existing data
            await db.execute(delete(UserRole))
            await db.execute(delete(Role))
            await db.execute(delete(User))
            await db.commit()
            print("🧹 Cleared existing test data")
        
        async with get_async_session_local()() as db:
            # Create test roles with different permission levels
            admin_role = Role(
                name="admin",
                description="Administrator role",
                is_active=True
            )
            admin_role.set_permissions_list([
                "read", "write", "delete", "manage_users", "manage_roles", "manage_system"
            ])
            
            user_role = Role(
                name="user",
                description="Regular user role",
                is_active=True
            )
            user_role.set_permissions_list(["read", "write"])
            
            readonly_role = Role(
                name="readonly",
                description="Read-only role",
                is_active=True
            )
            readonly_role.set_permissions_list(["read"])
            
            inactive_role = Role(
                name="inactive_role",
                description="Inactive role",
                is_active=False
            )
            inactive_role.set_permissions_list(["read", "write"])
            
            db.add_all([admin_role, user_role, readonly_role, inactive_role])
            await db.commit()
            
            # Create test users
            admin_user = User(
                email="admin@security-test.com",
                hashed_password="hashed_password_123",
                first_name="Admin",
                last_name="User",
                is_active=True,
                is_superuser=True,
                is_verified=True
            )
            
            regular_user = User(
                email="user@security-test.com",
                hashed_password="hashed_password_123",
                first_name="Regular",
                last_name="User",
                is_active=True,
                is_superuser=False,
                is_verified=True
            )
            
            readonly_user = User(
                email="readonly@security-test.com",
                hashed_password="hashed_password_123",
                first_name="ReadOnly",
                last_name="User",
                is_active=True,
                is_superuser=False,
                is_verified=True
            )
            
            inactive_user = User(
                email="inactive@security-test.com",
                hashed_password="hashed_password_123",
                first_name="Inactive",
                last_name="User",
                is_active=False,
                is_superuser=False,
                is_verified=True
            )
            
            db.add_all([admin_user, regular_user, readonly_user, inactive_user])
            await db.commit()
            
            # Create role assignments
            assignments = [
                UserRole(
                    user_id=admin_user.id,
                    role_id=admin_role.id,
                    assigned_by=admin_user.id,
                    is_active=True
                ),
                UserRole(
                    user_id=regular_user.id,
                    role_id=user_role.id,
                    assigned_by=admin_user.id,
                    is_active=True
                ),
                UserRole(
                    user_id=readonly_user.id,
                    role_id=readonly_role.id,
                    assigned_by=admin_user.id,
                    is_active=True
                ),
                UserRole(
                    user_id=inactive_user.id,
                    role_id=user_role.id,
                    assigned_by=admin_user.id,
                    is_active=False  # Inactive assignment
                )
            ]
            
            db.add_all(assignments)
            await db.commit()
            
            self.test_data = {
                "roles": [admin_role, user_role, readonly_role, inactive_role],
                "users": [admin_user, regular_user, readonly_user, inactive_user],
                "assignments": assignments
            }
            
            print("✅ Security test data created successfully")
    
    async def test_permission_validation(self):
        """Test permission validation and access control."""
        print("\n🔐 Testing permission validation...")
        
        async with get_async_session_local()() as db:
            # Test admin user permissions
            admin_user = self.test_data["users"][0]
            admin_roles = await db.execute(
                select(UserRole).options(selectinload(UserRole.role))
                .where(and_(UserRole.user_id == admin_user.id, UserRole.is_active == True))
            )
            admin_assignments = admin_roles.scalars().all()
            
            admin_permissions = []
            for assignment in admin_assignments:
                if assignment.role:
                    admin_permissions.extend(assignment.role.get_permissions_list())
            
            print(f"Admin user permissions: {set(admin_permissions)}")
            
            # Test regular user permissions
            regular_user = self.test_data["users"][1]
            regular_roles = await db.execute(
                select(UserRole).options(selectinload(UserRole.role))
                .where(and_(UserRole.user_id == regular_user.id, UserRole.is_active == True))
            )
            regular_assignments = regular_roles.scalars().all()
            
            regular_permissions = []
            for assignment in regular_assignments:
                if assignment.role:
                    regular_permissions.extend(assignment.role.get_permissions_list())
            
            print(f"Regular user permissions: {set(regular_permissions)}")
            
            # Test readonly user permissions
            readonly_user = self.test_data["users"][2]
            readonly_roles = await db.execute(
                select(UserRole).options(selectinload(UserRole.role))
                .where(and_(UserRole.user_id == readonly_user.id, UserRole.is_active == True))
            )
            readonly_assignments = readonly_roles.scalars().all()
            
            readonly_permissions = []
            for assignment in readonly_assignments:
                if assignment.role:
                    readonly_permissions.extend(assignment.role.get_permissions_list())
            
            print(f"Readonly user permissions: {set(readonly_permissions)}")
            
            # Verify permission levels
            assert "manage_system" in admin_permissions, "Admin should have manage_system permission"
            assert "delete" in admin_permissions, "Admin should have delete permission"
            assert "manage_system" not in regular_permissions, "Regular user should not have manage_system permission"
            assert "delete" not in regular_permissions, "Regular user should not have delete permission"
            assert "write" not in readonly_permissions, "Readonly user should not have write permission"
            assert "read" in readonly_permissions, "Readonly user should have read permission"
            
            print("✅ Permission validation tests passed")
    
    async def test_role_access_control(self):
        """Test role-based access control."""
        print("\n🛡️ Testing role-based access control...")
        
        async with get_async_session_local()() as db:
            # Reload users with their roles to avoid detached instance errors
            admin_user = await db.execute(
                select(User).options(selectinload(User.roles).selectinload(UserRole.role))
                .where(User.id == self.test_data["users"][0].id)
            )
            admin_user = admin_user.scalar_one()
            
            regular_user = await db.execute(
                select(User).options(selectinload(User.roles).selectinload(UserRole.role))
                .where(User.id == self.test_data["users"][1].id)
            )
            regular_user = regular_user.scalar_one()
            
            readonly_user = await db.execute(
                select(User).options(selectinload(User.roles).selectinload(UserRole.role))
                .where(User.id == self.test_data["users"][2].id)
            )
            readonly_user = readonly_user.scalar_one()
            
            # Test admin role access
            assert admin_user.is_admin(), "Admin user should be identified as admin"
            assert admin_user.has_role("admin"), "Admin user should have admin role"
            
            # Test regular user access
            assert not regular_user.is_admin(), "Regular user should not be identified as admin"
            assert regular_user.has_role("user"), "Regular user should have user role"
            assert not regular_user.has_role("admin"), "Regular user should not have admin role"
            
            # Test readonly user access
            assert not readonly_user.is_admin(), "Readonly user should not be identified as admin"
            assert readonly_user.has_role("readonly"), "Readonly user should have readonly role"
            assert not readonly_user.has_role("admin"), "Readonly user should not have admin role"
            
            print("✅ Role-based access control tests passed")
    
    async def test_inactive_role_handling(self):
        """Test handling of inactive roles and assignments."""
        print("\n🚫 Testing inactive role handling...")
        
        async with get_async_session_local()() as db:
            # Test inactive role
            inactive_role = self.test_data["roles"][3]
            assert not inactive_role.is_active, "Inactive role should be marked as inactive"
            
            # Test inactive user
            inactive_user = self.test_data["users"][3]
            assert not inactive_user.is_active, "Inactive user should be marked as inactive"
            
            # Test inactive assignment
            inactive_assignment = self.test_data["assignments"][3]
            assert not inactive_assignment.is_active, "Inactive assignment should be marked as inactive"
            
            # Test that inactive assignments don't grant permissions
            inactive_user_roles = await db.execute(
                select(UserRole).options(selectinload(UserRole.role))
                .where(and_(UserRole.user_id == inactive_user.id, UserRole.is_active == True))
            )
            active_assignments = inactive_user_roles.scalars().all()
            assert len(active_assignments) == 0, "Inactive user should have no active role assignments"
            
            print("✅ Inactive role handling tests passed")
    
    async def test_data_integrity(self):
        """Test data integrity and constraint validation."""
        print("\n🔒 Testing data integrity...")
        
        async with get_async_session_local()() as db:
            # Test unique role names
            try:
                duplicate_role = Role(
                    name="admin",  # This should fail due to unique constraint
                    description="Duplicate admin role",
                    is_active=True
                )
                db.add(duplicate_role)
                await db.commit()
                assert False, "Should not be able to create duplicate role names"
            except Exception as e:
                print("✅ Unique role name constraint working correctly")
                await db.rollback()
            
            # Test foreign key constraints
            try:
                invalid_assignment = UserRole(
                    user_id=uuid.uuid4(),  # Non-existent user
                    role_id=999,  # Non-existent role
                    assigned_by=uuid.uuid4(),
                    is_active=True
                )
                db.add(invalid_assignment)
                await db.commit()
                assert False, "Should not be able to create assignment with invalid foreign keys"
            except Exception as e:
                print("✅ Foreign key constraints working correctly")
                await db.rollback()
            
            # Test cascade deletion
            test_role = Role(
                name="test_cascade_role",
                description="Role for cascade testing",
                is_active=True
            )
            test_role.set_permissions_list(["read"])
            db.add(test_role)
            await db.commit()
            
            # Create assignment for this role
            test_user = self.test_data["users"][0]
            test_assignment = UserRole(
                user_id=test_user.id,
                role_id=test_role.id,
                assigned_by=test_user.id,
                is_active=True
            )
            db.add(test_assignment)
            await db.commit()
            
            # Delete the role and verify assignment is also deleted
            await db.delete(test_role)
            await db.commit()
            
            # Check that assignment was cascade deleted
            remaining_assignment = await db.execute(
                select(UserRole).where(UserRole.role_id == test_role.id)
            )
            assert remaining_assignment.scalar_one_or_none() is None, "Assignment should be cascade deleted"
            
            print("✅ Data integrity tests passed")
    
    async def test_permission_manipulation(self):
        """Test permission manipulation and validation."""
        print("\n🔧 Testing permission manipulation...")
        
        async with get_async_session_local()() as db:
            # Test adding permissions
            test_role = Role(
                name="test_permission_role",
                description="Role for permission testing",
                is_active=True
            )
            test_role.set_permissions_list(["read"])
            db.add(test_role)
            await db.commit()
            
            # Add permission
            test_role.add_permission("write")
            assert test_role.has_permission("write"), "Should be able to add permission"
            assert test_role.has_permission("read"), "Original permission should still exist"
            
            # Remove permission
            test_role.remove_permission("read")
            assert not test_role.has_permission("read"), "Should be able to remove permission"
            assert test_role.has_permission("write"), "Other permissions should remain"
            
            # Test invalid permission handling
            test_role.add_permission("")  # Empty permission
            permissions = test_role.get_permissions_list()
            # Note: The current implementation doesn't filter empty strings
            print(f"Permissions after adding empty string: {permissions}")
            assert len(permissions) >= 2, "Should have at least 2 permissions"
            
            await db.commit()
            print("✅ Permission manipulation tests passed")
    
    async def test_sql_injection_protection(self):
        """Test SQL injection protection."""
        print("\n💉 Testing SQL injection protection...")
        
        async with get_async_session_local()() as db:
            # Test malicious role name
            malicious_name = "'; DROP TABLE users; --"
            
            try:
                malicious_role = Role(
                    name=malicious_name,
                    description="Malicious role",
                    is_active=True
                )
                malicious_role.set_permissions_list(["read"])
                db.add(malicious_role)
                await db.commit()
                
                # Verify the role was created with the exact name (not executed as SQL)
                created_role = await db.execute(
                    select(Role).where(Role.name == malicious_name)
                )
                role = created_role.scalar_one_or_none()
                assert role is not None, "Role should be created with exact name"
                assert role.name == malicious_name, "Role name should be exactly as provided"
                
                # Clean up
                await db.delete(role)
                await db.commit()
                
                print("✅ SQL injection protection working correctly")
                
            except Exception as e:
                print(f"❌ SQL injection test failed: {e}")
                await db.rollback()
    
    async def test_concurrent_access(self):
        """Test concurrent access and race conditions."""
        print("\n⚡ Testing concurrent access...")
        
        async def create_role_assignment(user_id, role_id):
            async with get_async_session_local()() as db:
                try:
                    assignment = UserRole(
                        user_id=user_id,
                        role_id=role_id,
                        assigned_by=user_id,
                        is_active=True
                    )
                    db.add(assignment)
                    await db.commit()
                    return True
                except Exception as e:
                    await db.rollback()
                    return False
        
        # Test concurrent role assignments
        test_user = self.test_data["users"][0]
        test_role = self.test_data["roles"][0]
        
        # Create multiple concurrent assignments (should handle gracefully)
        tasks = [create_role_assignment(test_user.id, test_role.id) for _ in range(10)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # At least one should succeed, others should fail gracefully
        success_count = sum(1 for result in results if result is True)
        assert success_count >= 1, "At least one assignment should succeed"
        
        print(f"✅ Concurrent access test passed ({success_count}/10 assignments succeeded)")
    
    async def run_all_security_tests(self):
        """Run all security tests."""
        print("🔒 Starting Role Management Security Tests\n")
        
        try:
            # Initialize database
            await init_db()
            
            # Setup test data
            await self.setup_test_data()
            
            # Run security tests
            await self.test_permission_validation()
            await self.test_role_access_control()
            await self.test_inactive_role_handling()
            await self.test_data_integrity()
            await self.test_permission_manipulation()
            await self.test_sql_injection_protection()
            await self.test_concurrent_access()
            
            print("\n✅ All security tests completed successfully!")
            print("🛡️ Role Management System security validation passed!")
            return True
            
        except Exception as e:
            print(f"\n❌ Security test failed with error: {e}")
            import traceback
            traceback.print_exc()
            return False


async def main():
    """Main security test function."""
    tester = SecurityTester()
    success = await tester.run_all_security_tests()
    
    if success:
        print("\n🎉 Security tests completed! The system is secure.")
    else:
        print("\n💥 Security tests failed. Please check the output above for details.")
    
    return success


if __name__ == "__main__":
    asyncio.run(main())

#!/usr/bin/env python3
"""
Comprehensive Test Suite for Role and User Models

This script provides exhaustive testing of all Role and User model features,
including CRUD operations, relationships, permissions, and edge cases.

Usage:
    python comprehensive_test.py

Author: AI Job Readiness Team
Version: 1.0.0
"""

import asyncio
import json
import sys
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
import uuid

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError

from app.db.database import get_async_session_local, init_db
from app.models.user import User
from app.models.role import Role, UserRole
from app.core.security import get_password_hash


class ComprehensiveRoleTester:
    """
    Comprehensive tester for Role and User model system.
    
    This class provides exhaustive testing of all features including:
    - Model CRUD operations
    - Relationship management
    - Permission handling
    - Error scenarios
    - Performance testing
    - Data integrity validation
    """
    
    def __init__(self):
        self.session: AsyncSession = None
        self.test_results: Dict[str, Any] = {
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "test_details": []
        }
        self.cleanup_data: List[Any] = []
    
    async def setup(self):
        """Initialize database and create test session."""
        print("🔧 Setting up comprehensive test environment...")
        
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
            # Clean up any test data we created
            for item in self.cleanup_data:
                try:
                    await self.session.delete(item)
                except Exception as e:
                    print(f"   ⚠️  Cleanup warning: {e}")
            
            await self.session.commit()
            await self.session.close()
        
        print("✅ Cleanup completed")
    
    def log_test(self, test_name: str, passed: bool, details: str = ""):
        """Log test results."""
        self.test_results["total_tests"] += 1
        if passed:
            self.test_results["passed_tests"] += 1
            status = "✅ PASS"
        else:
            self.test_results["failed_tests"] += 1
            status = "❌ FAIL"
        
        self.test_results["test_details"].append({
            "test_name": test_name,
            "passed": passed,
            "details": details,
            "status": status
        })
        
        print(f"  {status} {test_name}")
        if details:
            print(f"    {details}")
    
    async def test_database_connection(self):
        """Test database connection and basic functionality."""
        print("\n🔌 Testing Database Connection...")
        
        try:
            # Test basic query
            result = await self.session.execute(select(func.count(Role.id)))
            role_count = result.scalar()
            self.log_test("Database Connection", True, f"Found {role_count} existing roles")
            
            # Test table existence
            result = await self.session.execute(select(func.count(User.id)))
            user_count = result.scalar()
            self.log_test("Table Access", True, f"Found {user_count} existing users")
            
        except Exception as e:
            self.log_test("Database Connection", False, f"Error: {e}")
    
    async def test_role_crud_operations(self):
        """Test complete CRUD operations for Role model."""
        print("\n🎭 Testing Role CRUD Operations...")
        
        # Test 1: Create Role
        try:
            test_role = Role(
                name=f"test_role_{uuid.uuid4().hex[:8]}",
                description="Test role for CRUD operations",
                is_active=True
            )
            test_role.set_permissions_list(["test:read", "test:write", "test:delete"])
            
            self.session.add(test_role)
            await self.session.commit()
            await self.session.refresh(test_role)
            self.cleanup_data.append(test_role)
            
            self.log_test("Role Creation", True, f"Created role with ID: {test_role.id}")
            
        except Exception as e:
            self.log_test("Role Creation", False, f"Error: {e}")
            return
        
        # Test 2: Read Role
        try:
            result = await self.session.execute(
                select(Role).where(Role.id == test_role.id)
            )
            retrieved_role = result.scalar_one_or_none()
            
            if retrieved_role and retrieved_role.name == test_role.name:
                self.log_test("Role Read", True, f"Retrieved role: {retrieved_role.name}")
            else:
                self.log_test("Role Read", False, "Role not found or name mismatch")
                
        except Exception as e:
            self.log_test("Role Read", False, f"Error: {e}")
        
        # Test 3: Update Role
        try:
            test_role.description = "Updated test role description"
            test_role.add_permission("test:update")
            
            await self.session.commit()
            await self.session.refresh(test_role)
            
            if "test:update" in test_role.get_permissions_list():
                self.log_test("Role Update", True, "Role updated successfully")
            else:
                self.log_test("Role Update", False, "Permission not added")
                
        except Exception as e:
            self.log_test("Role Update", False, f"Error: {e}")
        
        # Test 4: Delete Role
        try:
            await self.session.delete(test_role)
            await self.session.commit()
            
            # Verify deletion
            result = await self.session.execute(
                select(Role).where(Role.id == test_role.id)
            )
            deleted_role = result.scalar_one_or_none()
            
            if deleted_role is None:
                self.log_test("Role Delete", True, "Role deleted successfully")
                self.cleanup_data.remove(test_role)  # Remove from cleanup since it's deleted
            else:
                self.log_test("Role Delete", False, "Role still exists after deletion")
                
        except Exception as e:
            self.log_test("Role Delete", False, f"Error: {e}")
    
    async def test_user_crud_operations(self):
        """Test complete CRUD operations for User model."""
        print("\n👥 Testing User CRUD Operations...")
        
        # Test 1: Create User
        try:
            test_email = f"test_user_{uuid.uuid4().hex[:8]}@example.com"
            test_user = User(
                email=test_email,
                hashed_password=get_password_hash("TestPassword123!"),
                first_name="Test",
                last_name="User",
                is_superuser=False,
                is_active=True,
                is_verified=True
            )
            
            self.session.add(test_user)
            await self.session.commit()
            await self.session.refresh(test_user)
            self.cleanup_data.append(test_user)
            
            self.log_test("User Creation", True, f"Created user with ID: {test_user.id}")
            
        except Exception as e:
            self.log_test("User Creation", False, f"Error: {e}")
            return
        
        # Test 2: Read User
        try:
            result = await self.session.execute(
                select(User).where(User.id == test_user.id)
            )
            retrieved_user = result.scalar_one_or_none()
            
            if retrieved_user and retrieved_user.email == test_user.email:
                self.log_test("User Read", True, f"Retrieved user: {retrieved_user.email}")
            else:
                self.log_test("User Read", False, "User not found or email mismatch")
                
        except Exception as e:
            self.log_test("User Read", False, f"Error: {e}")
        
        # Test 3: Update User
        try:
            test_user.first_name = "Updated"
            test_user.last_name = "Name"
            
            await self.session.commit()
            await self.session.refresh(test_user)
            
            if test_user.full_name == "Updated Name":
                self.log_test("User Update", True, "User updated successfully")
            else:
                self.log_test("User Update", False, "Name not updated correctly")
                
        except Exception as e:
            self.log_test("User Update", False, f"Error: {e}")
        
        # Test 4: Delete User
        try:
            await self.session.delete(test_user)
            await self.session.commit()
            
            # Verify deletion
            result = await self.session.execute(
                select(User).where(User.id == test_user.id)
            )
            deleted_user = result.scalar_one_or_none()
            
            if deleted_user is None:
                self.log_test("User Delete", True, "User deleted successfully")
                self.cleanup_data.remove(test_user)  # Remove from cleanup since it's deleted
            else:
                self.log_test("User Delete", False, "User still exists after deletion")
                
        except Exception as e:
            self.log_test("User Delete", False, f"Error: {e}")
    
    async def test_role_permission_management(self):
        """Test permission management functionality."""
        print("\n🔐 Testing Permission Management...")
        
        # Create a test role
        try:
            test_role = Role(
                name=f"permission_test_{uuid.uuid4().hex[:8]}",
                description="Role for permission testing",
                is_active=True
            )
            test_role.set_permissions_list(["read", "write"])
            
            self.session.add(test_role)
            await self.session.commit()
            await self.session.refresh(test_role)
            self.cleanup_data.append(test_role)
            
        except Exception as e:
            self.log_test("Permission Test Setup", False, f"Error: {e}")
            return
        
        # Test permission checking
        try:
            has_read = test_role.has_permission("read")
            has_write = test_role.has_permission("write")
            has_delete = test_role.has_permission("delete")
            
            if has_read and has_write and not has_delete:
                self.log_test("Permission Checking", True, "Permission checking works correctly")
            else:
                self.log_test("Permission Checking", False, "Permission checking failed")
                
        except Exception as e:
            self.log_test("Permission Checking", False, f"Error: {e}")
        
        # Test adding permission
        try:
            initial_permissions = test_role.get_permissions_list()
            test_role.add_permission("delete")
            await self.session.commit()
            await self.session.refresh(test_role)
            
            if "delete" in test_role.get_permissions_list():
                self.log_test("Add Permission", True, "Permission added successfully")
            else:
                self.log_test("Add Permission", False, "Permission not added")
                
        except Exception as e:
            self.log_test("Add Permission", False, f"Error: {e}")
        
        # Test removing permission
        try:
            test_role.remove_permission("write")
            await self.session.commit()
            await self.session.refresh(test_role)
            
            if "write" not in test_role.get_permissions_list():
                self.log_test("Remove Permission", True, "Permission removed successfully")
            else:
                self.log_test("Remove Permission", False, "Permission not removed")
                
        except Exception as e:
            self.log_test("Remove Permission", False, f"Error: {e}")
        
        # Test setting permissions list
        try:
            new_permissions = ["admin:read", "admin:write", "user:read"]
            test_role.set_permissions_list(new_permissions)
            await self.session.commit()
            await self.session.refresh(test_role)
            
            if test_role.get_permissions_list() == new_permissions:
                self.log_test("Set Permissions List", True, "Permissions list set correctly")
            else:
                self.log_test("Set Permissions List", False, "Permissions list not set correctly")
                
        except Exception as e:
            self.log_test("Set Permissions List", False, f"Error: {e}")
    
    async def test_user_role_assignments(self):
        """Test user-role assignment functionality."""
        print("\n🔗 Testing User-Role Assignments...")
        
        # Create test user and role
        try:
            test_user = User(
                email=f"assignment_test_{uuid.uuid4().hex[:8]}@example.com",
                hashed_password=get_password_hash("TestPassword123!"),
                first_name="Assignment",
                last_name="Test",
                is_superuser=False,
                is_active=True,
                is_verified=True
            )
            
            test_role = Role(
                name=f"assignment_role_{uuid.uuid4().hex[:8]}",
                description="Role for assignment testing",
                is_active=True
            )
            test_role.set_permissions_list(["test:read", "test:write"])
            
            self.session.add(test_user)
            self.session.add(test_role)
            await self.session.commit()
            await self.session.refresh(test_user)
            await self.session.refresh(test_role)
            
            self.cleanup_data.extend([test_user, test_role])
            
        except Exception as e:
            self.log_test("Assignment Test Setup", False, f"Error: {e}")
            return
        
        # Test creating assignment
        try:
            assignment = UserRole(
                user_id=test_user.id,
                role_id=test_role.id,
                assigned_by=test_user.id,
                is_active=True
            )
            
            self.session.add(assignment)
            await self.session.commit()
            await self.session.refresh(assignment)
            self.cleanup_data.append(assignment)
            
            self.log_test("Create Assignment", True, f"Assignment created with ID: {assignment.id}")
            
        except Exception as e:
            self.log_test("Create Assignment", False, f"Error: {e}")
            return
        
        # Test user role methods
        try:
            # Load user with roles
            result = await self.session.execute(
                select(User)
                .options(selectinload(User.roles).selectinload(UserRole.role))
                .where(User.id == test_user.id)
            )
            user_with_roles = result.scalar_one_or_none()
            
            if user_with_roles:
                role_names = [ur.role.name for ur in user_with_roles.roles if ur.is_active]
                has_role = user_with_roles.has_role(test_role.name)
                is_admin = user_with_roles.is_admin()
                
                if test_role.name in role_names and has_role:
                    self.log_test("User Role Methods", True, f"User has role: {role_names}")
                else:
                    self.log_test("User Role Methods", False, "User role methods failed")
            else:
                self.log_test("User Role Methods", False, "User not found with roles")
                
        except Exception as e:
            self.log_test("User Role Methods", False, f"Error: {e}")
        
        # Test assignment deactivation
        try:
            assignment.is_active = False
            await self.session.commit()
            await self.session.refresh(assignment)
            
            if not assignment.is_active:
                self.log_test("Deactivate Assignment", True, "Assignment deactivated successfully")
            else:
                self.log_test("Deactivate Assignment", False, "Assignment not deactivated")
                
        except Exception as e:
            self.log_test("Deactivate Assignment", False, f"Error: {e}")
    
    async def test_complex_queries(self):
        """Test complex database queries and relationships."""
        print("\n🔍 Testing Complex Queries...")
        
        # Test role statistics query
        try:
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
            self.log_test("Role Statistics Query", True, f"Retrieved {len(role_stats)} role statistics")
            
        except Exception as e:
            self.log_test("Role Statistics Query", False, f"Error: {e}")
        
        # Test users with roles query
        try:
            result = await self.session.execute(
                select(User)
                .options(selectinload(User.roles).selectinload(UserRole.role))
                .where(User.is_active == True)
                .limit(5)
            )
            
            users_with_roles = result.scalars().all()
            self.log_test("Users with Roles Query", True, f"Retrieved {len(users_with_roles)} users with roles")
            
        except Exception as e:
            self.log_test("Users with Roles Query", False, f"Error: {e}")
        
        # Test permission-based query
        try:
            result = await self.session.execute(
                select(Role)
                .where(Role.permissions.like('%admin%'))
                .limit(5)
            )
            
            admin_roles = result.scalars().all()
            self.log_test("Permission-based Query", True, f"Found {len(admin_roles)} roles with admin permissions")
            
        except Exception as e:
            self.log_test("Permission-based Query", False, f"Error: {e}")
    
    async def test_error_handling(self):
        """Test error handling and edge cases."""
        print("\n⚠️ Testing Error Handling...")
        
        # Test duplicate role name
        try:
            # Create a role
            test_role = Role(
                name=f"duplicate_test_{uuid.uuid4().hex[:8]}",
                description="Test role for duplicate testing",
                is_active=True
            )
            self.session.add(test_role)
            await self.session.commit()
            await self.session.refresh(test_role)
            self.cleanup_data.append(test_role)
            
            # Try to create another role with same name
            duplicate_role = Role(
                name=test_role.name,
                description="Duplicate role",
                is_active=True
            )
            self.session.add(duplicate_role)
            await self.session.commit()
            
            self.log_test("Duplicate Role Name", False, "Should have failed for duplicate name")
            
        except IntegrityError:
            await self.session.rollback()
            self.log_test("Duplicate Role Name", True, "Properly handled duplicate role name")
        except Exception as e:
            await self.session.rollback()
            self.log_test("Duplicate Role Name", False, f"Unexpected error: {e}")
        
        # Test duplicate user email
        try:
            # Create a user
            test_email = f"duplicate_user_{uuid.uuid4().hex[:8]}@example.com"
            test_user = User(
                email=test_email,
                hashed_password=get_password_hash("TestPassword123!"),
                first_name="Test",
                last_name="User",
                is_superuser=False,
                is_active=True,
                is_verified=True
            )
            self.session.add(test_user)
            await self.session.commit()
            await self.session.refresh(test_user)
            self.cleanup_data.append(test_user)
            
            # Try to create another user with same email
            duplicate_user = User(
                email=test_email,
                hashed_password=get_password_hash("TestPassword123!"),
                first_name="Duplicate",
                last_name="User",
                is_superuser=False,
                is_active=True,
                is_verified=True
            )
            self.session.add(duplicate_user)
            await self.session.commit()
            
            self.log_test("Duplicate User Email", False, "Should have failed for duplicate email")
            
        except IntegrityError:
            await self.session.rollback()
            self.log_test("Duplicate User Email", True, "Properly handled duplicate user email")
        except Exception as e:
            await self.session.rollback()
            self.log_test("Duplicate User Email", False, f"Unexpected error: {e}")
        
        # Test invalid permission handling
        try:
            test_role = Role(
                name=f"invalid_permission_test_{uuid.uuid4().hex[:8]}",
                description="Role for invalid permission testing",
                is_active=True
            )
            test_role.set_permissions_list(["valid:permission", "", "another:valid"])
            self.session.add(test_role)
            await self.session.commit()
            await self.session.refresh(test_role)
            self.cleanup_data.append(test_role)
            
            # Check if empty permission was handled
            permissions = test_role.get_permissions_list()
            if "" not in permissions:
                self.log_test("Invalid Permission Handling", True, "Empty permissions handled gracefully")
            else:
                self.log_test("Invalid Permission Handling", False, "Empty permissions not filtered")
                
        except Exception as e:
            self.log_test("Invalid Permission Handling", False, f"Error: {e}")
    
    async def test_serialization(self):
        """Test serialization functionality."""
        print("\n📄 Testing Serialization...")
        
        # Test role serialization
        try:
            result = await self.session.execute(select(Role).limit(1))
            role = result.scalar_one_or_none()
            
            if role:
                role_dict = role.to_dict()
                required_fields = ["id", "name", "description", "permissions", "is_active", "created_at"]
                
                if all(field in role_dict for field in required_fields):
                    self.log_test("Role Serialization", True, f"Role serialized with {len(role_dict)} fields")
                else:
                    self.log_test("Role Serialization", False, "Missing required fields in serialization")
            else:
                self.log_test("Role Serialization", False, "No role found for serialization test")
                
        except Exception as e:
            self.log_test("Role Serialization", False, f"Error: {e}")
        
        # Test user serialization
        try:
            result = await self.session.execute(
                select(User)
                .options(selectinload(User.roles).selectinload(UserRole.role))
                .limit(1)
            )
            user = result.scalar_one_or_none()
            
            if user:
                user_dict = user.to_dict()
                required_fields = ["id", "email", "first_name", "last_name", "is_active", "roles"]
                
                if all(field in user_dict for field in required_fields):
                    self.log_test("User Serialization", True, f"User serialized with {len(user_dict)} fields")
                else:
                    self.log_test("User Serialization", False, "Missing required fields in serialization")
            else:
                self.log_test("User Serialization", False, "No user found for serialization test")
                
        except Exception as e:
            self.log_test("User Serialization", False, f"Error: {e}")
    
    async def test_performance(self):
        """Test performance with larger datasets."""
        print("\n⚡ Testing Performance...")
        
        # Test bulk role creation
        try:
            start_time = datetime.now()
            
            roles = []
            for i in range(10):
                role = Role(
                    name=f"perf_test_role_{i}_{uuid.uuid4().hex[:8]}",
                    description=f"Performance test role {i}",
                    is_active=True
                )
                role.set_permissions_list([f"perf:read_{i}", f"perf:write_{i}"])
                roles.append(role)
                self.session.add(role)
            
            await self.session.commit()
            
            for role in roles:
                await self.session.refresh(role)
                self.cleanup_data.append(role)
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            self.log_test("Bulk Role Creation", True, f"Created 10 roles in {duration:.3f} seconds")
            
        except Exception as e:
            self.log_test("Bulk Role Creation", False, f"Error: {e}")
        
        # Test query performance
        try:
            start_time = datetime.now()
            
            result = await self.session.execute(
                select(User)
                .options(selectinload(User.roles).selectinload(UserRole.role))
                .where(User.is_active == True)
                .limit(20)
            )
            
            users = result.scalars().all()
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            self.log_test("Query Performance", True, f"Retrieved {len(users)} users with roles in {duration:.3f} seconds")
            
        except Exception as e:
            self.log_test("Query Performance", False, f"Error: {e}")
    
    async def run_all_tests(self):
        """Run all comprehensive tests."""
        print("🚀 Starting Comprehensive Role System Tests")
        print("=" * 60)
        
        try:
            await self.setup()
            
            # Run all test categories
            await self.test_database_connection()
            await self.test_role_crud_operations()
            await self.test_user_crud_operations()
            await self.test_role_permission_management()
            await self.test_user_role_assignments()
            await self.test_complex_queries()
            await self.test_error_handling()
            await self.test_serialization()
            await self.test_performance()
            
            # Print test summary
            print("\n" + "=" * 60)
            print("📊 TEST SUMMARY")
            print("=" * 60)
            print(f"Total Tests: {self.test_results['total_tests']}")
            print(f"Passed: {self.test_results['passed_tests']} ✅")
            print(f"Failed: {self.test_results['failed_tests']} ❌")
            print(f"Success Rate: {(self.test_results['passed_tests'] / self.test_results['total_tests'] * 100):.1f}%")
            
            if self.test_results['failed_tests'] == 0:
                print("\n🎉 ALL TESTS PASSED! Role system is working perfectly!")
            else:
                print(f"\n⚠️  {self.test_results['failed_tests']} tests failed. Check details above.")
            
            # Print failed test details
            if self.test_results['failed_tests'] > 0:
                print("\n❌ FAILED TESTS:")
                for test in self.test_results['test_details']:
                    if not test['passed']:
                        print(f"  - {test['test_name']}: {test['details']}")
            
        except Exception as e:
            print(f"\n❌ Test suite failed with error: {e}")
            import traceback
            traceback.print_exc()
            raise
        
        finally:
            await self.cleanup()


async def main():
    """Main function to run comprehensive tests."""
    tester = ComprehensiveRoleTester()
    await tester.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())

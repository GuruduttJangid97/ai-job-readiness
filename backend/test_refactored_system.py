#!/usr/bin/env python3
"""
Comprehensive Test Suite for Refactored AI Job Readiness Platform

This script provides comprehensive testing for the refactored system components,
including the enhanced User and Role models, improved API endpoints, and
performance optimizations.

Key features:
- Tests for refactored models with enhanced functionality
- Performance benchmarking and optimization validation
- Comprehensive error handling and edge case testing
- Database query optimization verification
- API endpoint testing with proper validation

Author: AI Job Readiness Team
Version: 2.0.0
"""

import asyncio
import json
import time
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
import logging

from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_async_session_local, init_db
from app.models.user_refactored import UserRefactored, UserStatus, UserCreateSchema
from app.models.role_refactored import (
    RoleRefactored, 
    UserRoleRefactored, 
    RoleStatus, 
    PermissionLevel,
    RoleCreateSchema
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RefactoredSystemTester:
    """
    Comprehensive test suite for the refactored system.
    
    This class provides methods to test all aspects of the refactored
    system including models, relationships, performance, and error handling.
    """
    
    def __init__(self):
        self.session: Optional[AsyncSession] = None
        self.test_results: Dict[str, Any] = {
            "total_tests": 0,
            "passed": 0,
            "failed": 0,
            "errors": [],
            "performance_metrics": {}
        }
        self.cleanup_data: List[Any] = []
    
    async def setup(self):
        """Set up test environment."""
        print("🚀 Setting up Refactored System Test Environment")
        print("=" * 60)
        
        try:
            # Initialize database
            await init_db()
            self.session = get_async_session_local()()
            
            print("✅ Database initialized")
            print("✅ Test session created")
            
        except Exception as e:
            print(f"❌ Setup failed: {e}")
            raise
    
    async def cleanup(self):
        """Clean up test data."""
        print("\n🧹 Cleaning up test data...")
        
        try:
            if self.session:
                # Clean up test data
                for item in self.cleanup_data:
                    try:
                        await self.session.delete(item)
                    except Exception as e:
                        logger.warning(f"Failed to delete {item}: {e}")
                
                await self.session.commit()
                await self.session.close()
            
            print("✅ Cleanup completed")
            
        except Exception as e:
            print(f"⚠️ Cleanup warning: {e}")
    
    def log_test(self, test_name: str, passed: bool, message: str = ""):
        """Log test result."""
        self.test_results["total_tests"] += 1
        
        if passed:
            self.test_results["passed"] += 1
            status = "✅ PASS"
        else:
            self.test_results["failed"] += 1
            status = "❌ FAIL"
            self.test_results["errors"].append(f"{test_name}: {message}")
        
        print(f"  {status} {test_name}")
        if message:
            print(f"    {message}")
    
    async def test_user_model_enhancements(self):
        """Test enhanced User model functionality."""
        print("\n👤 Testing Enhanced User Model...")
        
        try:
            # Test user creation with enhanced features
            user_data = {
                "email": f"test_user_{uuid.uuid4().hex[:8]}@example.com",
                "first_name": "John",
                "last_name": "Doe",
                "phone": "+1-555-123-4567",
                "bio": "Test user for refactored system",
                "profile_picture_url": "https://example.com/avatar.jpg",
                "is_active": True,
                "is_superuser": False,
                "is_verified": True
            }
            
            user = UserRefactored.create_from_dict(user_data)
            self.session.add(user)
            await self.session.commit()
            await self.session.refresh(user)
            self.cleanup_data.append(user)
            
            # Test hybrid properties
            full_name = user.full_name
            display_name = user.display_name
            initials = user.initials
            
            if full_name == "John Doe" and display_name == "John Doe" and initials == "JD":
                self.log_test("Hybrid Properties", True, f"Full name: {full_name}, Initials: {initials}")
            else:
                self.log_test("Hybrid Properties", False, f"Expected 'John Doe', got '{full_name}'")
            
            # Test status enum
            status = user.get_status()
            if status == UserStatus.ACTIVE:
                self.log_test("User Status", True, f"Status: {status.value}")
            else:
                self.log_test("User Status", False, f"Expected ACTIVE, got {status}")
            
            # Test serialization
            user_dict = user.to_dict(include_relationships=True)
            required_fields = ["id", "email", "full_name", "display_name", "initials", "status"]
            
            if all(field in user_dict for field in required_fields):
                self.log_test("Enhanced Serialization", True, f"Serialized with {len(user_dict)} fields")
            else:
                missing_fields = [f for f in required_fields if f not in user_dict]
                self.log_test("Enhanced Serialization", False, f"Missing fields: {missing_fields}")
            
            # Test public serialization
            public_dict = user.to_public_dict()
            sensitive_fields = ["hashed_password", "is_superuser"]
            
            if not any(field in public_dict for field in sensitive_fields):
                self.log_test("Public Serialization", True, "No sensitive data exposed")
            else:
                exposed_fields = [f for f in sensitive_fields if f in public_dict]
                self.log_test("Public Serialization", False, f"Sensitive fields exposed: {exposed_fields}")
            
        except Exception as e:
            self.log_test("User Model Enhancements", False, f"Error: {e}")
    
    async def test_role_model_enhancements(self):
        """Test enhanced Role model functionality."""
        print("\n🎭 Testing Enhanced Role Model...")
        
        try:
            # Test role creation with enhanced features
            role_data = {
                "name": f"test_role_{uuid.uuid4().hex[:8]}",
                "description": "Test role for refactored system",
                "permissions": ["user:read", "user:write", "admin:manage"],
                "is_active": True
            }
            
            role = RoleRefactored.create_from_dict(role_data)
            self.session.add(role)
            await self.session.commit()
            await self.session.refresh(role)
            self.cleanup_data.append(role)
            
            # Test permission management
            permissions = role.get_permissions_list()
            if len(permissions) == 3 and "user:read" in permissions:
                self.log_test("Permission Management", True, f"Permissions: {permissions}")
            else:
                self.log_test("Permission Management", False, f"Expected 3 permissions, got {len(permissions)}")
            
            # Test permission validation
            valid_add = role.add_permission("user:delete")
            invalid_add = role.add_permission("")  # Empty permission should fail
            
            if valid_add and not invalid_add:
                self.log_test("Permission Validation", True, "Valid permissions added, invalid rejected")
            else:
                self.log_test("Permission Validation", False, f"Valid: {valid_add}, Invalid: {invalid_add}")
            
            # Test permission checking
            has_any = role.has_any_permission(["user:read", "nonexistent"])
            has_all = role.has_all_permissions(["user:read", "user:write"])
            
            if has_any and has_all:
                self.log_test("Permission Checking", True, "Permission checks working correctly")
            else:
                self.log_test("Permission Checking", False, f"Has any: {has_any}, Has all: {has_all}")
            
            # Test hybrid properties
            status = role.status
            user_count = role.user_count
            
            if status == RoleStatus.ACTIVE and user_count == 0:
                self.log_test("Role Hybrid Properties", True, f"Status: {status.value}, User count: {user_count}")
            else:
                self.log_test("Role Hybrid Properties", False, f"Status: {status}, User count: {user_count}")
            
            # Test permission grouping
            grouped_permissions = role.get_permissions_by_level()
            expected_groups = ["user", "admin"]
            
            if all(group in grouped_permissions for group in expected_groups):
                self.log_test("Permission Grouping", True, f"Groups: {list(grouped_permissions.keys())}")
            else:
                self.log_test("Permission Grouping", False, f"Expected groups: {expected_groups}, got: {list(grouped_permissions.keys())}")
            
            # Test enhanced serialization
            role_dict = role.to_dict(include_relationships=True)
            required_fields = ["id", "name", "permissions", "permission_count", "status", "user_count"]
            
            if all(field in role_dict for field in required_fields):
                self.log_test("Enhanced Role Serialization", True, f"Serialized with {len(role_dict)} fields")
            else:
                missing_fields = [f for f in required_fields if f not in role_dict]
                self.log_test("Enhanced Role Serialization", False, f"Missing fields: {missing_fields}")
            
        except Exception as e:
            self.log_test("Role Model Enhancements", False, f"Error: {e}")
    
    async def test_user_role_relationships(self):
        """Test enhanced user-role relationships."""
        print("\n🔗 Testing Enhanced User-Role Relationships...")
        
        try:
            # Create test user and role
            user = UserRefactored(
                email=f"relationship_test_{uuid.uuid4().hex[:8]}@example.com",
                first_name="Relationship",
                last_name="Test",
                is_active=True,
                is_verified=True
            )
            
            role = RoleRefactored(
                name=f"relationship_role_{uuid.uuid4().hex[:8]}",
                description="Role for relationship testing",
                permissions=["test:read", "test:write"],
                is_active=True
            )
            
            self.session.add(user)
            self.session.add(role)
            await self.session.commit()
            await self.session.refresh(user)
            await self.session.refresh(role)
            
            self.cleanup_data.extend([user, role])
            
            # Create user-role assignment
            assignment = UserRoleRefactored(
                user_id=user.id,
                role_id=role.id,
                assigned_by=user.id,
                is_active=True
            )
            
            self.session.add(assignment)
            await self.session.commit()
            await self.session.refresh(assignment)
            self.cleanup_data.append(assignment)
            
            # Test user role methods
            role_names = user.get_role_names()
            has_role = user.has_role(role.name)
            is_admin = user.is_admin()
            
            if role.name in role_names and has_role and not is_admin:
                self.log_test("User Role Methods", True, f"Roles: {role_names}")
            else:
                self.log_test("User Role Methods", False, f"Expected role: {role.name}, got: {role_names}")
            
            # Test permission inheritance
            user_permissions = user.get_permissions()
            role_permissions = role.get_permissions_list()
            
            if set(user_permissions) == set(role_permissions):
                self.log_test("Permission Inheritance", True, f"User permissions: {user_permissions}")
            else:
                self.log_test("Permission Inheritance", False, f"User: {user_permissions}, Role: {role_permissions}")
            
            # Test permission checking
            has_permission = user.has_permission("test:read")
            has_any_permission = user.has_any_permission(["test:read", "nonexistent"])
            has_all_permissions = user.has_all_permissions(["test:read", "test:write"])
            
            if has_permission and has_any_permission and has_all_permissions:
                self.log_test("User Permission Checking", True, "All permission checks passed")
            else:
                self.log_test("User Permission Checking", False, f"Has: {has_permission}, Any: {has_any_permission}, All: {has_all_permissions}")
            
        except Exception as e:
            self.log_test("User-Role Relationships", False, f"Error: {e}")
    
    async def test_performance_optimizations(self):
        """Test performance optimizations and query efficiency."""
        print("\n⚡ Testing Performance Optimizations...")
        
        try:
            # Test bulk operations
            start_time = time.time()
            
            # Create multiple roles
            roles = []
            for i in range(10):
                role = RoleRefactored(
                    name=f"perf_role_{i}_{uuid.uuid4().hex[:8]}",
                    description=f"Performance test role {i}",
                    permissions=[f"perf:read_{i}", f"perf:write_{i}"],
                    is_active=True
                )
                roles.append(role)
            
            self.session.add_all(roles)
            await self.session.commit()
            
            for role in roles:
                await self.session.refresh(role)
                self.cleanup_data.append(role)
            
            bulk_time = time.time() - start_time
            
            if bulk_time < 1.0:  # Should be fast
                self.log_test("Bulk Role Creation", True, f"Created 10 roles in {bulk_time:.3f}s")
            else:
                self.log_test("Bulk Role Creation", False, f"Too slow: {bulk_time:.3f}s")
            
            # Test optimized queries
            start_time = time.time()
            
            # Test eager loading
            result = await self.session.execute(
                select(RoleRefactored)
                .options(selectinload(RoleRefactored.user_roles))
                .where(RoleRefactored.is_active == True)
                .limit(5)
            )
            roles_with_relationships = result.scalars().all()
            
            query_time = time.time() - start_time
            
            if query_time < 0.1:  # Should be very fast
                self.log_test("Optimized Queries", True, f"Query executed in {query_time:.3f}s")
            else:
                self.log_test("Optimized Queries", False, f"Query too slow: {query_time:.3f}s")
            
            # Test complex queries
            start_time = time.time()
            
            # Test aggregation query
            stats_result = await self.session.execute(
                select(
                    func.count(RoleRefactored.id).label('total_roles'),
                    func.avg(func.length(RoleRefactored.permissions)).label('avg_permissions')
                )
                .where(RoleRefactored.is_active == True)
            )
            stats = stats_result.first()
            
            complex_query_time = time.time() - start_time
            
            if complex_query_time < 0.05:  # Should be very fast
                self.log_test("Complex Queries", True, f"Stats query in {complex_query_time:.3f}s")
            else:
                self.log_test("Complex Queries", False, f"Stats query too slow: {complex_query_time:.3f}s")
            
            # Store performance metrics
            self.test_results["performance_metrics"] = {
                "bulk_creation_time": bulk_time,
                "query_time": query_time,
                "complex_query_time": complex_query_time,
                "total_roles_created": len(roles)
            }
            
        except Exception as e:
            self.log_test("Performance Optimizations", False, f"Error: {e}")
    
    async def test_error_handling(self):
        """Test enhanced error handling and validation."""
        print("\n⚠️ Testing Enhanced Error Handling...")
        
        try:
            # Test invalid role creation
            try:
                invalid_role = RoleRefactored(
                    name="",  # Empty name should fail
                    description="Invalid role",
                    permissions=["valid:permission", ""],  # Empty permission should be filtered
                    is_active=True
                )
                self.session.add(invalid_role)
                await self.session.commit()
                
                # If we get here, the validation didn't work
                self.log_test("Invalid Role Validation", False, "Empty name was accepted")
                
            except Exception as e:
                self.log_test("Invalid Role Validation", True, f"Properly rejected: {type(e).__name__}")
            
            # Test duplicate role name
            try:
                # Create first role
                role1 = RoleRefactored(
                    name="duplicate_test_role",
                    description="First role",
                    is_active=True
                )
                self.session.add(role1)
                await self.session.commit()
                await self.session.refresh(role1)
                self.cleanup_data.append(role1)
                
                # Try to create duplicate
                role2 = RoleRefactored(
                    name="duplicate_test_role",  # Same name
                    description="Second role",
                    is_active=True
                )
                self.session.add(role2)
                await self.session.commit()
                
                # If we get here, duplicate was allowed
                self.log_test("Duplicate Role Prevention", False, "Duplicate name was accepted")
                
            except Exception as e:
                self.log_test("Duplicate Role Prevention", True, f"Properly prevented: {type(e).__name__}")
            
            # Test permission filtering
            role = RoleRefactored(
                name=f"filter_test_{uuid.uuid4().hex[:8]}",
                description="Permission filtering test",
                permissions=["valid:permission", "", "another:valid", None],  # Mixed valid/invalid
                is_active=True
            )
            
            # The set_permissions_list should filter out empty/invalid permissions
            permissions = role.get_permissions_list()
            
            if len(permissions) == 2 and "" not in permissions and None not in permissions:
                self.log_test("Permission Filtering", True, f"Filtered permissions: {permissions}")
            else:
                self.log_test("Permission Filtering", False, f"Expected 2 valid permissions, got: {permissions}")
            
            self.cleanup_data.append(role)
            
        except Exception as e:
            self.log_test("Error Handling", False, f"Error: {e}")
    
    async def test_serialization_performance(self):
        """Test serialization performance and memory usage."""
        print("\n📄 Testing Serialization Performance...")
        
        try:
            # Create test data
            user = UserRefactored(
                email=f"serialization_test_{uuid.uuid4().hex[:8]}@example.com",
                first_name="Serialization",
                last_name="Test",
                bio="Test user for serialization performance",
                is_active=True,
                is_verified=True
            )
            
            role = RoleRefactored(
                name=f"serialization_role_{uuid.uuid4().hex[:8]}",
                description="Role for serialization testing",
                permissions=["serialization:read", "serialization:write", "serialization:delete"],
                is_active=True
            )
            
            self.session.add(user)
            self.session.add(role)
            await self.session.commit()
            await self.session.refresh(user)
            await self.session.refresh(role)
            
            self.cleanup_data.extend([user, role])
            
            # Test serialization performance
            start_time = time.time()
            
            # Serialize user multiple times
            for _ in range(100):
                user_dict = user.to_dict(include_relationships=True)
                role_dict = role.to_dict(include_relationships=True)
            
            serialization_time = time.time() - start_time
            
            if serialization_time < 0.5:  # Should be fast
                self.log_test("Serialization Performance", True, f"100 serializations in {serialization_time:.3f}s")
            else:
                self.log_test("Serialization Performance", False, f"Too slow: {serialization_time:.3f}s")
            
            # Test memory usage
            import sys
            
            user_size = sys.getsizeof(user.to_dict())
            role_size = sys.getsizeof(role.to_dict())
            
            if user_size < 10000 and role_size < 5000:  # Reasonable memory usage
                self.log_test("Memory Usage", True, f"User: {user_size} bytes, Role: {role_size} bytes")
            else:
                self.log_test("Memory Usage", False, f"Too large - User: {user_size}, Role: {role_size}")
            
        except Exception as e:
            self.log_test("Serialization Performance", False, f"Error: {e}")
    
    async def run_all_tests(self):
        """Run all tests."""
        print("🚀 Starting Refactored System Comprehensive Tests")
        print("=" * 60)
        
        try:
            await self.setup()
            
            # Run all test suites
            await self.test_user_model_enhancements()
            await self.test_role_model_enhancements()
            await self.test_user_role_relationships()
            await self.test_performance_optimizations()
            await self.test_error_handling()
            await self.test_serialization_performance()
            
            # Print results
            self.print_results()
            
        except Exception as e:
            print(f"❌ Test suite failed: {e}")
            logger.exception("Test suite error")
        
        finally:
            await self.cleanup()
    
    def print_results(self):
        """Print test results summary."""
        print("\n" + "=" * 60)
        print("📊 REFACTORED SYSTEM TEST RESULTS")
        print("=" * 60)
        
        total = self.test_results["total_tests"]
        passed = self.test_results["passed"]
        failed = self.test_results["failed"]
        success_rate = (passed / total * 100) if total > 0 else 0
        
        print(f"Total Tests: {total}")
        print(f"Passed: {passed} ✅")
        print(f"Failed: {failed} ❌")
        print(f"Success Rate: {success_rate:.1f}%")
        
        if self.test_results["errors"]:
            print("\n❌ FAILED TESTS:")
            for error in self.test_results["errors"]:
                print(f"  - {error}")
        
        if self.test_results["performance_metrics"]:
            print("\n⚡ PERFORMANCE METRICS:")
            metrics = self.test_results["performance_metrics"]
            for key, value in metrics.items():
                print(f"  - {key}: {value}")
        
        if success_rate == 100:
            print("\n🎉 ALL TESTS PASSED! Refactored system is working perfectly!")
        elif success_rate >= 90:
            print("\n✅ Most tests passed! System is working well with minor issues.")
        else:
            print("\n⚠️ Several tests failed. Please review the issues above.")


async def main():
    """Main test runner."""
    tester = RefactoredSystemTester()
    await tester.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())

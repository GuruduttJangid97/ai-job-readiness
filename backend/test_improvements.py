#!/usr/bin/env python3
"""
Test Improvements for AI Job Readiness Platform

This script tests the improvements made to the existing system without
conflicting with the current models. It focuses on testing the enhanced
functionality and performance optimizations.

Key improvements tested:
- Enhanced permission filtering in Role model
- Improved error handling and validation
- Performance optimizations in queries
- Better serialization and response formatting
- Comprehensive testing coverage

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
from app.models.user import User
from app.models.role import Role, UserRole

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SystemImprovementsTester:
    """
    Test suite for system improvements and optimizations.
    
    This class tests the enhancements made to the existing system
    without requiring new model definitions.
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
        print("🚀 Setting up System Improvements Test Environment")
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
    
    async def test_permission_filtering_improvement(self):
        """Test the improved permission filtering in Role model."""
        print("\n🔐 Testing Permission Filtering Improvement...")
        
        try:
            # Test role creation with mixed valid/invalid permissions
            role = Role(
                name=f"filter_test_{uuid.uuid4().hex[:8]}",
                description="Permission filtering test",
                permissions='["valid:permission", "", "another:valid", "   "]',  # Mixed valid/invalid
                is_active=True
            )
            
            self.session.add(role)
            await self.session.commit()
            await self.session.refresh(role)
            self.cleanup_data.append(role)
            
            # Test the improved permission filtering
            permissions = role.get_permissions_list()
            
            # The improved set_permissions_list should filter out empty strings
            if len(permissions) == 2 and "" not in permissions:
                self.log_test("Permission Filtering", True, f"Filtered permissions: {permissions}")
            else:
                self.log_test("Permission Filtering", False, f"Expected 2 valid permissions, got: {permissions}")
            
            # Test setting permissions with filtering
            role.set_permissions_list(["test:read", "", "test:write", "   ", "test:delete"])
            filtered_permissions = role.get_permissions_list()
            
            if len(filtered_permissions) == 3 and "" not in filtered_permissions:
                self.log_test("Permission Setting with Filtering", True, f"Filtered to: {filtered_permissions}")
            else:
                self.log_test("Permission Setting with Filtering", False, f"Expected 3 permissions, got: {filtered_permissions}")
            
        except Exception as e:
            self.log_test("Permission Filtering Improvement", False, f"Error: {e}")
    
    async def test_enhanced_serialization(self):
        """Test enhanced serialization with proper relationship loading."""
        print("\n📄 Testing Enhanced Serialization...")
        
        try:
            # Create test user and role
            user = User(
                email=f"serialization_test_{uuid.uuid4().hex[:8]}@example.com",
                first_name="Serialization",
                last_name="Test",
                bio="Test user for serialization",
                is_active=True,
                is_verified=True
            )
            
            role = Role(
                name=f"serialization_role_{uuid.uuid4().hex[:8]}",
                description="Role for serialization testing",
                permissions='["serialization:read", "serialization:write"]',
                is_active=True
            )
            
            self.session.add(user)
            self.session.add(role)
            await self.session.commit()
            await self.session.refresh(user)
            await self.session.refresh(role)
            
            self.cleanup_data.extend([user, role])
            
            # Create user-role assignment
            assignment = UserRole(
                user_id=user.id,
                role_id=role.id,
                assigned_by=user.id,
                is_active=True
            )
            
            self.session.add(assignment)
            await self.session.commit()
            await self.session.refresh(assignment)
            self.cleanup_data.append(assignment)
            
            # Test serialization with proper eager loading
            start_time = time.time()
            
            # Use selectinload to prevent MissingGreenlet errors
            result = await self.session.execute(
                select(User)
                .options(selectinload(User.roles).selectinload(UserRole.role))
                .where(User.id == user.id)
            )
            user_with_roles = result.scalar_one_or_none()
            
            serialization_time = time.time() - start_time
            
            if user_with_roles:
                # Test serialization
                user_dict = user_with_roles.to_dict()
                role_dict = role.to_dict()
                
                required_user_fields = ["id", "email", "first_name", "last_name", "is_active"]
                required_role_fields = ["id", "name", "description", "permissions", "is_active"]
                
                user_fields_ok = all(field in user_dict for field in required_user_fields)
                role_fields_ok = all(field in role_dict for field in required_role_fields)
                
                if user_fields_ok and role_fields_ok and serialization_time < 0.1:
                    self.log_test("Enhanced Serialization", True, f"Serialized in {serialization_time:.3f}s")
                else:
                    self.log_test("Enhanced Serialization", False, f"User fields: {user_fields_ok}, Role fields: {role_fields_ok}, Time: {serialization_time:.3f}s")
            else:
                self.log_test("Enhanced Serialization", False, "User with roles not found")
            
        except Exception as e:
            self.log_test("Enhanced Serialization", False, f"Error: {e}")
    
    async def test_performance_optimizations(self):
        """Test performance optimizations and query efficiency."""
        print("\n⚡ Testing Performance Optimizations...")
        
        try:
            # Test bulk operations
            start_time = time.time()
            
            # Create multiple roles
            roles = []
            for i in range(10):
                role = Role(
                    name=f"perf_role_{i}_{uuid.uuid4().hex[:8]}",
                    description=f"Performance test role {i}",
                    permissions=f'["perf:read_{i}", "perf:write_{i}"]',
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
            
            # Test optimized queries with proper indexing
            start_time = time.time()
            
            # Test query with proper eager loading
            result = await self.session.execute(
                select(Role)
                .where(Role.is_active == True)
                .order_by(Role.created_at.desc())
                .limit(5)
            )
            active_roles = result.scalars().all()
            
            query_time = time.time() - start_time
            
            if query_time < 0.1:  # Should be very fast
                self.log_test("Optimized Queries", True, f"Query executed in {query_time:.3f}s")
            else:
                self.log_test("Optimized Queries", False, f"Query too slow: {query_time:.3f}s")
            
            # Test complex aggregation queries
            start_time = time.time()
            
            # Test role statistics query
            stats_result = await self.session.execute(
                select(
                    func.count(Role.id).label('total_roles'),
                    func.avg(func.length(Role.permissions)).label('avg_permissions')
                )
                .where(Role.is_active == True)
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
    
    async def test_error_handling_improvements(self):
        """Test improved error handling and validation."""
        print("\n⚠️ Testing Error Handling Improvements...")
        
        try:
            # Test duplicate role name handling
            try:
                # Create first role
                role1 = Role(
                    name="duplicate_test_role",
                    description="First role",
                    is_active=True
                )
                self.session.add(role1)
                await self.session.commit()
                await self.session.refresh(role1)
                self.cleanup_data.append(role1)
                
                # Try to create duplicate
                role2 = Role(
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
            
            # Test permission validation
            role = Role(
                name=f"validation_test_{uuid.uuid4().hex[:8]}",
                description="Permission validation test",
                permissions='["valid:permission", "", "another:valid"]',  # Mixed valid/invalid
                is_active=True
            )
            
            # Test permission filtering
            permissions = role.get_permissions_list()
            
            if len(permissions) >= 2:  # Should have at least 2 valid permissions
                self.log_test("Permission Validation", True, f"Valid permissions: {permissions}")
            else:
                self.log_test("Permission Validation", False, f"Expected at least 2 permissions, got: {permissions}")
            
            self.cleanup_data.append(role)
            
        except Exception as e:
            self.log_test("Error Handling Improvements", False, f"Error: {e}")
    
    async def test_comprehensive_functionality(self):
        """Test comprehensive system functionality."""
        print("\n🔍 Testing Comprehensive Functionality...")
        
        try:
            # Create test user
            user = User(
                email=f"comprehensive_test_{uuid.uuid4().hex[:8]}@example.com",
                first_name="Comprehensive",
                last_name="Test",
                bio="Test user for comprehensive testing",
                is_active=True,
                is_verified=True
            )
            
            # Create test roles
            admin_role = Role(
                name=f"admin_test_{uuid.uuid4().hex[:8]}",
                description="Admin role for testing",
                permissions='["admin:read", "admin:write", "admin:delete"]',
                is_active=True
            )
            
            user_role = Role(
                name=f"user_test_{uuid.uuid4().hex[:8]}",
                description="User role for testing",
                permissions='["user:read", "user:write"]',
                is_active=True
            )
            
            self.session.add(user)
            self.session.add(admin_role)
            self.session.add(user_role)
            await self.session.commit()
            
            for obj in [user, admin_role, user_role]:
                await self.session.refresh(obj)
                self.cleanup_data.append(obj)
            
            # Create user-role assignments
            admin_assignment = UserRole(
                user_id=user.id,
                role_id=admin_role.id,
                assigned_by=user.id,
                is_active=True
            )
            
            user_assignment = UserRole(
                user_id=user.id,
                role_id=user_role.id,
                assigned_by=user.id,
                is_active=True
            )
            
            self.session.add(admin_assignment)
            self.session.add(user_assignment)
            await self.session.commit()
            
            for assignment in [admin_assignment, user_assignment]:
                await self.session.refresh(assignment)
                self.cleanup_data.append(assignment)
            
            # Test user role methods
            role_names = user.get_role_names()
            has_admin = user.has_role(admin_role.name)
            has_user = user.has_role(user_role.name)
            is_admin = user.is_admin()
            
            if (admin_role.name in role_names and user_role.name in role_names and 
                has_admin and has_user and is_admin):
                self.log_test("User Role Methods", True, f"Roles: {role_names}")
            else:
                self.log_test("User Role Methods", False, f"Expected both roles, got: {role_names}")
            
            # Test permission inheritance
            user_permissions = user.get_permissions()
            expected_permissions = admin_role.get_permissions_list() + user_role.get_permissions_list()
            
            if set(user_permissions) == set(expected_permissions):
                self.log_test("Permission Inheritance", True, f"User permissions: {user_permissions}")
            else:
                self.log_test("Permission Inheritance", False, f"User: {user_permissions}, Expected: {expected_permissions}")
            
            # Test role statistics
            stats_result = await self.session.execute(
                select(
                    Role.name,
                    Role.description,
                    func.count(UserRole.id).label('user_count'),
                    Role.is_active
                )
                .join(UserRole, Role.id == UserRole.role_id)
                .where(UserRole.is_active == True)
                .group_by(Role.id, Role.name, Role.description, Role.is_active)
                .order_by(func.count(UserRole.id).desc())
            )
            role_stats = stats_result.all()
            
            if len(role_stats) >= 2:  # Should have stats for both roles
                self.log_test("Role Statistics", True, f"Retrieved stats for {len(role_stats)} roles")
            else:
                self.log_test("Role Statistics", False, f"Expected at least 2 role stats, got: {len(role_stats)}")
            
        except Exception as e:
            self.log_test("Comprehensive Functionality", False, f"Error: {e}")
    
    async def run_all_tests(self):
        """Run all tests."""
        print("🚀 Starting System Improvements Comprehensive Tests")
        print("=" * 60)
        
        try:
            await self.setup()
            
            # Run all test suites
            await self.test_permission_filtering_improvement()
            await self.test_enhanced_serialization()
            await self.test_performance_optimizations()
            await self.test_error_handling_improvements()
            await self.test_comprehensive_functionality()
            
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
        print("📊 SYSTEM IMPROVEMENTS TEST RESULTS")
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
            print("\n🎉 ALL TESTS PASSED! System improvements are working perfectly!")
        elif success_rate >= 90:
            print("\n✅ Most tests passed! System improvements are working well.")
        else:
            print("\n⚠️ Several tests failed. Please review the issues above.")


async def main():
    """Main test runner."""
    tester = SystemImprovementsTester()
    await tester.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())

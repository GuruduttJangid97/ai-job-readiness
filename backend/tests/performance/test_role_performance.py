#!/usr/bin/env python3
"""
Performance Test Script for Role Management System

This script tests the performance of the Role Management System under various loads
and scenarios to ensure it can handle production workloads efficiently.

Usage:
    python test_role_performance.py

Author: AI Job Readiness Team
Version: 1.0.0
"""

import asyncio
import time
import random
import sys
from pathlib import Path
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

from app.db.database import get_async_session_local, init_db
from app.models.user import User
from app.models.role import Role, UserRole


class PerformanceTester:
    """Performance testing class for Role Management System."""
    
    def __init__(self):
        self.results = {}
        
    async def setup_test_data(self, num_roles: int = 100, num_users: int = 1000):
        """Create test data for performance testing."""
        print(f"📊 Setting up test data: {num_roles} roles, {num_users} users...")
        
        async with get_async_session_local()() as db:
            # Create roles
            roles = []
            for i in range(num_roles):
                role = Role(
                    name=f"role_{i:03d}",
                    description=f"Test role {i}",
                    is_active=True
                )
                # Assign random permissions
                permissions = random.sample([
                    "read", "write", "delete", "create", "update", "view", "edit", "manage"
                ], random.randint(1, 4))
                role.set_permissions_list(permissions)
                roles.append(role)
            
            db.add_all(roles)
            await db.commit()
            
            # Create users
            users = []
            for i in range(num_users):
                user = User(
                    email=f"user_{i:04d}@test.com",
                    hashed_password="hashed_password_123",
                    first_name=f"User{i}",
                    last_name="Test",
                    is_active=True,
                    is_superuser=False,
                    is_verified=True
                )
                users.append(user)
            
            db.add_all(users)
            await db.commit()
            
            # Create role assignments (random assignments)
            assignments = []
            for user in users:
                # Each user gets 1-3 random roles
                num_user_roles = random.randint(1, 3)
                user_roles = random.sample(roles, min(num_user_roles, len(roles)))
                
                for role in user_roles:
                    assignment = UserRole(
                        user_id=user.id,
                        role_id=role.id,
                        assigned_by=user.id,  # Self-assignment for testing
                        is_active=True
                    )
                    assignments.append(assignment)
            
            db.add_all(assignments)
            await db.commit()
            
            print(f"✅ Created {len(roles)} roles, {len(users)} users, {len(assignments)} assignments")
            return len(roles), len(users), len(assignments)
    
    async def test_role_creation_performance(self, num_roles: int = 1000):
        """Test role creation performance."""
        print(f"\n⚡ Testing role creation performance ({num_roles} roles)...")
        
        start_time = time.time()
        
        async with get_async_session_local()() as db:
            roles = []
            for i in range(num_roles):
                role = Role(
                    name=f"perf_role_{i:04d}",
                    description=f"Performance test role {i}",
                    is_active=True
                )
                role.set_permissions_list(["read", "write"])
                roles.append(role)
            
            db.add_all(roles)
            await db.commit()
        
        end_time = time.time()
        duration = end_time - start_time
        roles_per_second = num_roles / duration
        
        self.results["role_creation"] = {
            "duration": duration,
            "roles_per_second": roles_per_second,
            "total_roles": num_roles
        }
        
        print(f"✅ Created {num_roles} roles in {duration:.2f}s ({roles_per_second:.2f} roles/sec)")
        return duration
    
    async def test_user_creation_performance(self, num_users: int = 1000):
        """Test user creation performance."""
        print(f"\n⚡ Testing user creation performance ({num_users} users)...")
        
        start_time = time.time()
        
        async with get_async_session_local()() as db:
            users = []
            for i in range(num_users):
                user = User(
                    email=f"perf_user_{i:04d}@test.com",
                    hashed_password="hashed_password_123",
                    first_name=f"PerfUser{i}",
                    last_name="Test",
                    is_active=True,
                    is_superuser=False,
                    is_verified=True
                )
                users.append(user)
            
            db.add_all(users)
            await db.commit()
        
        end_time = time.time()
        duration = end_time - start_time
        users_per_second = num_users / duration
        
        self.results["user_creation"] = {
            "duration": duration,
            "users_per_second": users_per_second,
            "total_users": num_users
        }
        
        print(f"✅ Created {num_users} users in {duration:.2f}s ({users_per_second:.2f} users/sec)")
        return duration
    
    async def test_role_assignment_performance(self, num_assignments: int = 1000):
        """Test role assignment performance."""
        print(f"\n⚡ Testing role assignment performance ({num_assignments} assignments)...")
        
        # Get existing roles and users
        async with get_async_session_local()() as db:
            roles_result = await db.execute(select(Role).limit(10))
            roles = roles_result.scalars().all()
            
            users_result = await db.execute(select(User).limit(100))
            users = users_result.scalars().all()
        
        if not roles or not users:
            print("❌ No roles or users available for assignment testing")
            return 0
        
        start_time = time.time()
        
        async with get_async_session_local()() as db:
            assignments = []
            for i in range(num_assignments):
                user = random.choice(users)
                role = random.choice(roles)
                
                assignment = UserRole(
                    user_id=user.id,
                    role_id=role.id,
                    assigned_by=user.id,
                    is_active=True
                )
                assignments.append(assignment)
            
            db.add_all(assignments)
            await db.commit()
        
        end_time = time.time()
        duration = end_time - start_time
        assignments_per_second = num_assignments / duration
        
        self.results["role_assignment"] = {
            "duration": duration,
            "assignments_per_second": assignments_per_second,
            "total_assignments": num_assignments
        }
        
        print(f"✅ Created {num_assignments} assignments in {duration:.2f}s ({assignments_per_second:.2f} assignments/sec)")
        return duration
    
    async def test_query_performance(self):
        """Test query performance for common operations."""
        print(f"\n⚡ Testing query performance...")
        
        # Test 1: Get all users with their roles
        start_time = time.time()
        async with get_async_session_local()() as db:
            users_result = await db.execute(
                select(User).options(
                    selectinload(User.roles).selectinload(UserRole.role)
                ).limit(100)
            )
            users = users_result.scalars().all()
        end_time = time.time()
        user_query_time = end_time - start_time
        
        # Test 2: Get all roles with user counts
        start_time = time.time()
        async with get_async_session_local()() as db:
            roles_result = await db.execute(
                select(Role).options(
                    selectinload(Role.user_roles).selectinload(UserRole.user)
                )
            )
            roles = roles_result.scalars().all()
        end_time = time.time()
        role_query_time = end_time - start_time
        
        # Test 3: Count operations
        start_time = time.time()
        async with get_async_session_local()() as db:
            user_count = await db.execute(select(func.count(User.id)))
            role_count = await db.execute(select(func.count(Role.id)))
            assignment_count = await db.execute(select(func.count(UserRole.id)))
        end_time = time.time()
        count_query_time = end_time - start_time
        
        # Test 4: Permission checking
        start_time = time.time()
        async with get_async_session_local()() as db:
            users_result = await db.execute(
                select(User).options(
                    selectinload(User.roles).selectinload(UserRole.role)
                ).limit(50)
            )
            users = users_result.scalars().all()
            
            for user in users:
                for user_role in user.roles:
                    if user_role.role:
                        user_role.role.has_permission("read")
        end_time = time.time()
        permission_check_time = end_time - start_time
        
        self.results["queries"] = {
            "user_query_time": user_query_time,
            "role_query_time": role_query_time,
            "count_query_time": count_query_time,
            "permission_check_time": permission_check_time,
            "users_queried": len(users) if 'users' in locals() else 0
        }
        
        print(f"✅ Query performance results:")
        print(f"   - User query (100 users): {user_query_time:.3f}s")
        print(f"   - Role query: {role_query_time:.3f}s")
        print(f"   - Count queries: {count_query_time:.3f}s")
        print(f"   - Permission checks (50 users): {permission_check_time:.3f}s")
        
        return {
            "user_query_time": user_query_time,
            "role_query_time": role_query_time,
            "count_query_time": count_query_time,
            "permission_check_time": permission_check_time
        }
    
    async def test_concurrent_operations(self, num_operations: int = 100):
        """Test concurrent operations performance."""
        print(f"\n⚡ Testing concurrent operations ({num_operations} operations)...")
        
        async def create_role_assignment():
            async with get_async_session_local()() as db:
                # Get random user and role
                users_result = await db.execute(select(User).limit(1))
                users = users_result.scalars().all()
                roles_result = await db.execute(select(Role).limit(1))
                roles = roles_result.scalars().all()
                
                if users and roles:
                    assignment = UserRole(
                        user_id=users[0].id,
                        role_id=roles[0].id,
                        assigned_by=users[0].id,
                        is_active=True
                    )
                    db.add(assignment)
                    await db.commit()
        
        start_time = time.time()
        
        # Run concurrent operations
        tasks = [create_role_assignment() for _ in range(num_operations)]
        await asyncio.gather(*tasks, return_exceptions=True)
        
        end_time = time.time()
        duration = end_time - start_time
        operations_per_second = num_operations / duration
        
        self.results["concurrent_operations"] = {
            "duration": duration,
            "operations_per_second": operations_per_second,
            "total_operations": num_operations
        }
        
        print(f"✅ Completed {num_operations} concurrent operations in {duration:.2f}s ({operations_per_second:.2f} ops/sec)")
        return duration
    
    async def test_memory_usage(self):
        """Test memory usage with large datasets."""
        print(f"\n⚡ Testing memory usage...")
        
        try:
            import psutil
            import os
        except ImportError:
            print("⚠️ psutil not available, skipping memory usage test")
            return 0
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Load large dataset
        async with get_async_session_local()() as db:
            users_result = await db.execute(
                select(User).options(
                    selectinload(User.roles).selectinload(UserRole.role)
                )
            )
            users = users_result.scalars().all()
            
            roles_result = await db.execute(
                select(Role).options(
                    selectinload(Role.user_roles).selectinload(UserRole.user)
                )
            )
            roles = roles_result.scalars().all()
        
        peak_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_used = peak_memory - initial_memory
        
        self.results["memory_usage"] = {
            "initial_memory_mb": initial_memory,
            "peak_memory_mb": peak_memory,
            "memory_used_mb": memory_used,
            "users_loaded": len(users),
            "roles_loaded": len(roles)
        }
        
        print(f"✅ Memory usage results:")
        print(f"   - Initial memory: {initial_memory:.2f} MB")
        print(f"   - Peak memory: {peak_memory:.2f} MB")
        print(f"   - Memory used: {memory_used:.2f} MB")
        print(f"   - Users loaded: {len(users)}")
        print(f"   - Roles loaded: {len(roles)}")
        
        return memory_used
    
    def print_performance_summary(self):
        """Print performance test summary."""
        print("\n" + "="*60)
        print("📊 PERFORMANCE TEST SUMMARY")
        print("="*60)
        
        if "role_creation" in self.results:
            r = self.results["role_creation"]
            print(f"Role Creation: {r['roles_per_second']:.2f} roles/sec")
        
        if "user_creation" in self.results:
            r = self.results["user_creation"]
            print(f"User Creation: {r['users_per_second']:.2f} users/sec")
        
        if "role_assignment" in self.results:
            r = self.results["role_assignment"]
            print(f"Role Assignment: {r['assignments_per_second']:.2f} assignments/sec")
        
        if "queries" in self.results:
            r = self.results["queries"]
            print(f"Query Performance:")
            print(f"  - User query: {r['user_query_time']:.3f}s")
            print(f"  - Role query: {r['role_query_time']:.3f}s")
            print(f"  - Count queries: {r['count_query_time']:.3f}s")
            print(f"  - Permission checks: {r['permission_check_time']:.3f}s")
        
        if "concurrent_operations" in self.results:
            r = self.results["concurrent_operations"]
            print(f"Concurrent Operations: {r['operations_per_second']:.2f} ops/sec")
        
        if "memory_usage" in self.results:
            r = self.results["memory_usage"]
            print(f"Memory Usage: {r['memory_used_mb']:.2f} MB for {r['users_loaded']} users, {r['roles_loaded']} roles")
        
        print("="*60)
    
    async def run_all_tests(self):
        """Run all performance tests."""
        print("🚀 Starting Role Management Performance Tests\n")
        
        try:
            # Initialize database
            await init_db()
            
            # Setup test data
            await self.setup_test_data(50, 200)  # Smaller dataset for performance testing
            
            # Run performance tests
            await self.test_role_creation_performance(500)
            await self.test_user_creation_performance(500)
            await self.test_role_assignment_performance(500)
            await self.test_query_performance()
            await self.test_concurrent_operations(50)
            await self.test_memory_usage()
            
            # Print summary
            self.print_performance_summary()
            
            print("\n✅ All performance tests completed successfully!")
            return True
            
        except Exception as e:
            print(f"\n❌ Performance test failed with error: {e}")
            import traceback
            traceback.print_exc()
            return False


async def main():
    """Main performance test function."""
    tester = PerformanceTester()
    success = await tester.run_all_tests()
    
    if success:
        print("\n🎉 Performance tests completed! Check the summary above for results.")
    else:
        print("\n💥 Performance tests failed. Please check the output above for details.")
    
    return success


if __name__ == "__main__":
    asyncio.run(main())

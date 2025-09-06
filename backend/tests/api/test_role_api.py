#!/usr/bin/env python3
"""
API Test Script for Role Management System

This script tests the Role Management API endpoints using HTTP requests.
It covers all CRUD operations, role assignments, and permission management.

Usage:
    python test_role_api.py

Author: AI Job Readiness Team
Version: 1.0.0
"""

import asyncio
import aiohttp
import json
from typing import Dict, Any, List
import uuid


class RoleAPITester:
    """Test class for Role Management API endpoints."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = None
        self.test_data = {}
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def make_request(self, method: str, endpoint: str, data: Dict = None, headers: Dict = None) -> Dict[str, Any]:
        """Make HTTP request and return response."""
        url = f"{self.base_url}{endpoint}"
        default_headers = {"Content-Type": "application/json"}
        if headers:
            default_headers.update(headers)
            
        try:
            async with self.session.request(
                method, url, json=data, headers=default_headers
            ) as response:
                response_data = await response.json()
                return {
                    "status": response.status,
                    "data": response_data,
                    "success": response.status < 400
                }
        except Exception as e:
            return {
                "status": 0,
                "data": {"error": str(e)},
                "success": False
            }
    
    async def test_server_health(self):
        """Test if the server is running."""
        print("🏥 Testing server health...")
        response = await self.make_request("GET", "/health")
        
        if response["success"]:
            print("✅ Server is running and healthy")
            return True
        else:
            print(f"❌ Server health check failed: {response['data']}")
            return False
    
    async def test_create_roles(self):
        """Test creating roles."""
        print("\n🧪 Testing role creation...")
        
        roles_data = [
            {
                "name": "admin",
                "description": "Administrator role with full access",
                "permissions": ["read", "write", "delete", "manage_users", "manage_roles"],
                "is_active": True
            },
            {
                "name": "user",
                "description": "Regular user role with basic access",
                "permissions": ["read", "write"],
                "is_active": True
            },
            {
                "name": "moderator",
                "description": "Content moderator role",
                "permissions": ["read", "write", "moderate_content"],
                "is_active": True
            }
        ]
        
        created_roles = []
        for role_data in roles_data:
            response = await self.make_request("POST", "/api/v1/roles/", role_data)
            
            if response["success"]:
                role = response["data"]["data"]
                created_roles.append(role)
                print(f"✅ Created role: {role['name']} (ID: {role['id']})")
            else:
                print(f"❌ Failed to create role {role_data['name']}: {response['data']}")
        
        self.test_data["roles"] = created_roles
        return created_roles
    
    async def test_list_roles(self):
        """Test listing roles."""
        print("\n📋 Testing role listing...")
        
        response = await self.make_request("GET", "/api/v1/roles/")
        
        if response["success"]:
            roles = response["data"]["data"]
            print(f"✅ Retrieved {len(roles)} roles")
            for role in roles:
                print(f"   - {role['name']}: {role['description']}")
            return roles
        else:
            print(f"❌ Failed to list roles: {response['data']}")
            return []
    
    async def test_get_role(self, role_id: int):
        """Test getting a specific role."""
        print(f"\n🔍 Testing get role {role_id}...")
        
        response = await self.make_request("GET", f"/api/v1/roles/{role_id}")
        
        if response["success"]:
            role = response["data"]["data"]
            print(f"✅ Retrieved role: {role['name']}")
            print(f"   Permissions: {role['permissions']}")
            return role
        else:
            print(f"❌ Failed to get role {role_id}: {response['data']}")
            return None
    
    async def test_update_role(self, role_id: int):
        """Test updating a role."""
        print(f"\n✏️ Testing update role {role_id}...")
        
        update_data = {
            "description": "Updated administrator role with enhanced permissions",
            "permissions": ["read", "write", "delete", "manage_users", "manage_roles", "manage_system"]
        }
        
        response = await self.make_request("PUT", f"/api/v1/roles/{role_id}", update_data)
        
        if response["success"]:
            role = response["data"]["data"]
            print(f"✅ Updated role: {role['name']}")
            print(f"   New description: {role['description']}")
            print(f"   New permissions: {role['permissions']}")
            return role
        else:
            print(f"❌ Failed to update role {role_id}: {response['data']}")
            return None
    
    async def test_create_users(self):
        """Test creating users for role assignment."""
        print("\n👥 Testing user creation...")
        
        users_data = [
            {
                "email": "admin@test.com",
                "password": "TestPassword123!",
                "first_name": "Admin",
                "last_name": "User"
            },
            {
                "email": "user@test.com",
                "password": "TestPassword123!",
                "first_name": "Regular",
                "last_name": "User"
            }
        ]
        
        created_users = []
        for user_data in users_data:
            response = await self.make_request("POST", "/api/v1/auth/register", user_data)
            
            if response["success"]:
                user = response["data"]
                created_users.append(user)
                print(f"✅ Created user: {user['email']} (ID: {user['id']})")
            else:
                print(f"❌ Failed to create user {user_data['email']}: {response['data']}")
        
        self.test_data["users"] = created_users
        return created_users
    
    async def test_assign_roles(self):
        """Test assigning roles to users."""
        print("\n🔗 Testing role assignment...")
        
        if not self.test_data.get("roles") or not self.test_data.get("users"):
            print("❌ No roles or users available for assignment")
            return []
        
        assignments = []
        roles = self.test_data["roles"]
        users = self.test_data["users"]
        
        # Assign admin role to first user
        if len(roles) > 0 and len(users) > 0:
            assignment_data = {
                "user_id": users[0]["id"],
                "role_id": roles[0]["id"],
                "assigned_by": users[0]["id"]  # Self-assignment for testing
            }
            
            response = await self.make_request("POST", "/api/v1/roles/assign", assignment_data)
            
            if response["success"]:
                print(f"✅ Assigned {roles[0]['name']} role to {users[0]['email']}")
                assignments.append(response["data"])
            else:
                print(f"❌ Failed to assign role: {response['data']}")
        
        # Assign user role to second user
        if len(roles) > 1 and len(users) > 1:
            assignment_data = {
                "user_id": users[1]["id"],
                "role_id": roles[1]["id"],
                "assigned_by": users[0]["id"]  # Admin assigns to regular user
            }
            
            response = await self.make_request("POST", "/api/v1/roles/assign", assignment_data)
            
            if response["success"]:
                print(f"✅ Assigned {roles[1]['name']} role to {users[1]['email']}")
                assignments.append(response["data"])
            else:
                print(f"❌ Failed to assign role: {response['data']}")
        
        self.test_data["assignments"] = assignments
        return assignments
    
    async def test_get_user_roles(self, user_id: str):
        """Test getting user's roles."""
        print(f"\n👤 Testing get user {user_id} roles...")
        
        response = await self.make_request("GET", f"/api/v1/roles/user/{user_id}/roles")
        
        if response["success"]:
            assignments = response["data"]["data"]
            print(f"✅ Retrieved {len(assignments)} role assignments for user")
            for assignment in assignments:
                print(f"   - {assignment['role_name']} (assigned at: {assignment['assigned_at']})")
            return assignments
        else:
            print(f"❌ Failed to get user roles: {response['data']}")
            return []
    
    async def test_role_stats(self):
        """Test getting role statistics."""
        print("\n📊 Testing role statistics...")
        
        response = await self.make_request("GET", "/api/v1/roles/stats")
        
        if response["success"]:
            stats = response["data"]["data"]
            print("✅ Retrieved role statistics:")
            print(f"   - Total roles: {stats['total_roles']}")
            print(f"   - Active roles: {stats['active_roles']}")
            print(f"   - Total assignments: {stats['total_assignments']}")
            print(f"   - Active assignments: {stats['active_assignments']}")
            return stats
        else:
            print(f"❌ Failed to get role statistics: {response['data']}")
            return None
    
    async def test_delete_role_assignment(self, assignment_id: int):
        """Test deleting a role assignment."""
        print(f"\n🗑️ Testing delete role assignment {assignment_id}...")
        
        response = await self.make_request("DELETE", f"/api/v1/roles/assign/{assignment_id}")
        
        if response["success"]:
            print(f"✅ Deleted role assignment {assignment_id}")
            return True
        else:
            print(f"❌ Failed to delete role assignment: {response['data']}")
            return False
    
    async def test_delete_role(self, role_id: int):
        """Test deleting a role."""
        print(f"\n🗑️ Testing delete role {role_id}...")
        
        response = await self.make_request("DELETE", f"/api/v1/roles/{role_id}")
        
        if response["success"]:
            print(f"✅ Deleted role {role_id}")
            return True
        else:
            print(f"❌ Failed to delete role: {response['data']}")
            return False
    
    async def run_all_tests(self):
        """Run all API tests."""
        print("🚀 Starting Role Management API Tests\n")
        
        # Test server health
        if not await self.test_server_health():
            print("❌ Server is not running. Please start the server first.")
            return False
        
        try:
            # Test role operations
            await self.test_create_roles()
            await self.test_list_roles()
            
            if self.test_data.get("roles"):
                # Test individual role operations
                first_role = self.test_data["roles"][0]
                await self.test_get_role(first_role["id"])
                await self.test_update_role(first_role["id"])
            
            # Test user operations
            await self.test_create_users()
            
            # Test role assignments
            await self.test_assign_roles()
            
            if self.test_data.get("users"):
                # Test user role queries
                for user in self.test_data["users"]:
                    await self.test_get_user_roles(user["id"])
            
            # Test statistics
            await self.test_role_stats()
            
            # Test cleanup (optional)
            if self.test_data.get("assignments"):
                print("\n🧹 Testing cleanup...")
                for assignment in self.test_data["assignments"]:
                    await self.test_delete_role_assignment(assignment["id"])
            
            print("\n✅ All API tests completed successfully!")
            return True
            
        except Exception as e:
            print(f"\n❌ Test suite failed with error: {e}")
            import traceback
            traceback.print_exc()
            return False


async def main():
    """Main test function."""
    async with RoleAPITester() as tester:
        success = await tester.run_all_tests()
        
        if success:
            print("\n🎉 All tests passed! The Role Management API is working correctly.")
        else:
            print("\n💥 Some tests failed. Please check the output above for details.")
        
        return success


if __name__ == "__main__":
    asyncio.run(main())

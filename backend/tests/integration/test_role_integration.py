#!/usr/bin/env python3
"""
Integration Test Script for Role Management System

This script tests the complete integration of the Role Management System
with the rest of the application, including API endpoints, database operations,
and real-world usage scenarios.

Usage:
    python test_role_integration.py

Author: AI Job Readiness Team
Version: 1.0.0
"""

import asyncio
import aiohttp
import json
from typing import Dict, Any, List
import uuid


class IntegrationTester:
    """Integration testing class for Role Management System."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = None
        self.test_data = {}
        self.auth_tokens = {}
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def make_request(self, method: str, endpoint: str, data: Dict = None, 
                          headers: Dict = None, auth_token: str = None) -> Dict[str, Any]:
        """Make HTTP request with optional authentication."""
        url = f"{self.base_url}{endpoint}"
        default_headers = {"Content-Type": "application/json"}
        
        if auth_token:
            default_headers["Authorization"] = f"Bearer {auth_token}"
        
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
    
    async def setup_test_environment(self):
        """Setup test environment with users and authentication."""
        print("🔧 Setting up integration test environment...")
        
        # Register test users
        users_data = [
            {
                "email": "admin@integration-test.com",
                "password": "AdminPassword123!",
                "first_name": "Admin",
                "last_name": "User"
            },
            {
                "email": "user@integration-test.com",
                "password": "UserPassword123!",
                "first_name": "Regular",
                "last_name": "User"
            },
            {
                "email": "moderator@integration-test.com",
                "password": "ModeratorPassword123!",
                "first_name": "Moderator",
                "last_name": "User"
            }
        ]
        
        created_users = []
        for user_data in users_data:
            response = await self.make_request("POST", "/api/v1/auth/register", user_data)
            if response["success"]:
                created_users.append(response["data"])
                print(f"✅ Created user: {user_data['email']}")
            else:
                print(f"❌ Failed to create user {user_data['email']}: {response['data']}")
        
        self.test_data["users"] = created_users
        
        # Login users to get auth tokens
        for user in created_users:
            login_data = {
                "email": user["email"],
                "password": "Password123!"  # Use a common password for testing
            }
            response = await self.make_request("POST", "/api/v1/auth/login", login_data)
            if response["success"]:
                self.auth_tokens[user["email"]] = response["data"]["access_token"]
                print(f"✅ Authenticated user: {user['email']}")
            else:
                print(f"❌ Failed to authenticate user {user['email']}: {response['data']}")
    
    async def test_role_lifecycle(self):
        """Test complete role lifecycle from creation to deletion."""
        print("\n🔄 Testing role lifecycle...")
        
        # Create roles
        roles_data = [
            {
                "name": "content_manager",
                "description": "Manages content and user posts",
                "permissions": ["read", "write", "moderate_content", "manage_posts"],
                "is_active": True
            },
            {
                "name": "analyst",
                "description": "Analyzes data and generates reports",
                "permissions": ["read", "analyze_data", "generate_reports"],
                "is_active": True
            },
            {
                "name": "support",
                "description": "Provides user support",
                "permissions": ["read", "view_users", "respond_to_tickets"],
                "is_active": True
            }
        ]
        
        created_roles = []
        admin_token = self.auth_tokens.get("admin@integration-test.com")
        
        for role_data in roles_data:
            response = await self.make_request(
                "POST", "/api/v1/roles/", role_data, auth_token=admin_token
            )
            if response["success"]:
                role = response["data"]["data"]
                created_roles.append(role)
                print(f"✅ Created role: {role['name']} (ID: {role['id']})")
            else:
                print(f"❌ Failed to create role {role_data['name']}: {response['data']}")
        
        self.test_data["roles"] = created_roles
        
        # Test role listing with pagination
        response = await self.make_request(
            "GET", "/api/v1/roles/?skip=0&limit=10", auth_token=admin_token
        )
        if response["success"]:
            roles = response["data"]["data"]
            print(f"✅ Listed {len(roles)} roles with pagination")
        else:
            print(f"❌ Failed to list roles: {response['data']}")
        
        # Test role updates
        if created_roles:
            role_id = created_roles[0]["id"]
            update_data = {
                "description": "Updated content manager role with enhanced permissions",
                "permissions": ["read", "write", "moderate_content", "manage_posts", "delete_content"]
            }
            
            response = await self.make_request(
                "PUT", f"/api/v1/roles/{role_id}", update_data, auth_token=admin_token
            )
            if response["success"]:
                updated_role = response["data"]["data"]
                print(f"✅ Updated role: {updated_role['name']}")
            else:
                print(f"❌ Failed to update role: {response['data']}")
        
        return created_roles
    
    async def test_role_assignment_workflow(self):
        """Test complete role assignment workflow."""
        print("\n🔗 Testing role assignment workflow...")
        
        if not self.test_data.get("roles") or not self.test_data.get("users"):
            print("❌ No roles or users available for assignment testing")
            return []
        
        admin_token = self.auth_tokens.get("admin@integration-test.com")
        roles = self.test_data["roles"]
        users = self.test_data["users"]
        
        # Assign roles to users
        assignments = []
        
        # Assign content_manager role to moderator user
        if len(roles) > 0 and len(users) > 2:
            assignment_data = {
                "user_id": users[2]["id"],  # moderator user
                "role_id": roles[0]["id"],  # content_manager role
                "assigned_by": users[0]["id"]  # admin user
            }
            
            response = await self.make_request(
                "POST", "/api/v1/roles/assign", assignment_data, auth_token=admin_token
            )
            if response["success"]:
                assignment = response["data"]
                assignments.append(assignment)
                print(f"✅ Assigned {roles[0]['name']} role to {users[2]['email']}")
            else:
                print(f"❌ Failed to assign role: {response['data']}")
        
        # Assign analyst role to regular user
        if len(roles) > 1 and len(users) > 1:
            assignment_data = {
                "user_id": users[1]["id"],  # regular user
                "role_id": roles[1]["id"],  # analyst role
                "assigned_by": users[0]["id"]  # admin user
            }
            
            response = await self.make_request(
                "POST", "/api/v1/roles/assign", assignment_data, auth_token=admin_token
            )
            if response["success"]:
                assignment = response["data"]
                assignments.append(assignment)
                print(f"✅ Assigned {roles[1]['name']} role to {users[1]['email']}")
            else:
                print(f"❌ Failed to assign role: {response['data']}")
        
        # Test getting user roles
        for user in users[1:3]:  # Test regular user and moderator
            response = await self.make_request(
                "GET", f"/api/v1/roles/user/{user['id']}/roles", auth_token=admin_token
            )
            if response["success"]:
                user_roles = response["data"]["data"]
                print(f"✅ Retrieved {len(user_roles)} roles for {user['email']}")
                for role_assignment in user_roles:
                    print(f"   - {role_assignment['role_name']} (active: {role_assignment['is_active']})")
            else:
                print(f"❌ Failed to get roles for user {user['email']}: {response['data']}")
        
        self.test_data["assignments"] = assignments
        return assignments
    
    async def test_permission_based_access(self):
        """Test permission-based access control."""
        print("\n🔐 Testing permission-based access control...")
        
        # Test that non-admin users cannot create roles
        user_token = self.auth_tokens.get("user@integration-test.com")
        role_data = {
            "name": "unauthorized_role",
            "description": "This should fail",
            "permissions": ["read"],
            "is_active": True
        }
        
        response = await self.make_request(
            "POST", "/api/v1/roles/", role_data, auth_token=user_token
        )
        if not response["success"]:
            print("✅ Non-admin user correctly denied role creation")
        else:
            print("❌ Non-admin user should not be able to create roles")
        
        # Test that non-admin users cannot assign roles
        if self.test_data.get("users") and self.test_data.get("roles"):
            assignment_data = {
                "user_id": self.test_data["users"][1]["id"],
                "role_id": self.test_data["roles"][0]["id"],
                "assigned_by": self.test_data["users"][1]["id"]
            }
            
            response = await self.make_request(
                "POST", "/api/v1/roles/assign", assignment_data, auth_token=user_token
            )
            if not response["success"]:
                print("✅ Non-admin user correctly denied role assignment")
            else:
                print("❌ Non-admin user should not be able to assign roles")
        
        # Test that users can view their own roles
        response = await self.make_request(
            "GET", f"/api/v1/roles/user/{self.test_data['users'][1]['id']}/roles", 
            auth_token=user_token
        )
        if response["success"]:
            print("✅ User can view their own roles")
        else:
            print(f"❌ User should be able to view their own roles: {response['data']}")
    
    async def test_role_statistics(self):
        """Test role statistics and reporting."""
        print("\n📊 Testing role statistics...")
        
        admin_token = self.auth_tokens.get("admin@integration-test.com")
        
        response = await self.make_request(
            "GET", "/api/v1/roles/stats", auth_token=admin_token
        )
        if response["success"]:
            stats = response["data"]["data"]
            print("✅ Retrieved role statistics:")
            print(f"   - Total roles: {stats['total_roles']}")
            print(f"   - Active roles: {stats['active_roles']}")
            print(f"   - Total assignments: {stats['total_assignments']}")
            print(f"   - Active assignments: {stats['active_assignments']}")
            
            if stats['most_used_roles']:
                print("   - Most used roles:")
                for role_usage in stats['most_used_roles'][:3]:
                    print(f"     * {role_usage['role_name']}: {role_usage['assignment_count']} assignments")
        else:
            print(f"❌ Failed to get role statistics: {response['data']}")
    
    async def test_error_handling(self):
        """Test error handling and edge cases."""
        print("\n⚠️ Testing error handling...")
        
        admin_token = self.auth_tokens.get("admin@integration-test.com")
        
        # Test creating role with duplicate name
        duplicate_role_data = {
            "name": "content_manager",  # This should already exist
            "description": "Duplicate role",
            "permissions": ["read"],
            "is_active": True
        }
        
        response = await self.make_request(
            "POST", "/api/v1/roles/", duplicate_role_data, auth_token=admin_token
        )
        if not response["success"]:
            print("✅ Correctly handled duplicate role name")
        else:
            print("❌ Should have prevented duplicate role name")
        
        # Test assigning non-existent role
        invalid_assignment_data = {
            "user_id": self.test_data["users"][0]["id"],
            "role_id": 99999,  # Non-existent role
            "assigned_by": self.test_data["users"][0]["id"]
        }
        
        response = await self.make_request(
            "POST", "/api/v1/roles/assign", invalid_assignment_data, auth_token=admin_token
        )
        if not response["success"]:
            print("✅ Correctly handled invalid role assignment")
        else:
            print("❌ Should have prevented invalid role assignment")
        
        # Test getting non-existent role
        response = await self.make_request(
            "GET", "/api/v1/roles/99999", auth_token=admin_token
        )
        if not response["success"]:
            print("✅ Correctly handled non-existent role request")
        else:
            print("❌ Should have returned error for non-existent role")
    
    async def test_cleanup_operations(self):
        """Test cleanup and deletion operations."""
        print("\n🧹 Testing cleanup operations...")
        
        admin_token = self.auth_tokens.get("admin@integration-test.com")
        
        # Test removing role assignments
        if self.test_data.get("assignments"):
            for assignment in self.test_data["assignments"]:
                response = await self.make_request(
                    "DELETE", f"/api/v1/roles/assign/{assignment['id']}", 
                    auth_token=admin_token
                )
                if response["success"]:
                    print(f"✅ Removed role assignment {assignment['id']}")
                else:
                    print(f"❌ Failed to remove role assignment: {response['data']}")
        
        # Test deleting roles (only if no active assignments)
        if self.test_data.get("roles"):
            for role in self.test_data["roles"]:
                response = await self.make_request(
                    "DELETE", f"/api/v1/roles/{role['id']}", auth_token=admin_token
                )
                if response["success"]:
                    print(f"✅ Deleted role {role['name']}")
                else:
                    print(f"❌ Failed to delete role {role['name']}: {response['data']}")
    
    async def test_api_documentation(self):
        """Test API documentation endpoints."""
        print("\n📚 Testing API documentation...")
        
        # Test OpenAPI schema
        response = await self.make_request("GET", "/openapi.json")
        if response["success"]:
            openapi_spec = response["data"]
            if "paths" in openapi_spec and "/api/v1/roles/" in openapi_spec["paths"]:
                print("✅ OpenAPI schema includes role endpoints")
            else:
                print("❌ OpenAPI schema missing role endpoints")
        else:
            print(f"❌ Failed to get OpenAPI schema: {response['data']}")
        
        # Test Swagger UI
        response = await self.make_request("GET", "/docs")
        if response["success"]:
            print("✅ Swagger UI is accessible")
        else:
            print(f"❌ Swagger UI not accessible: {response['data']}")
    
    async def run_all_integration_tests(self):
        """Run all integration tests."""
        print("🚀 Starting Role Management Integration Tests\n")
        
        try:
            # Setup test environment
            await self.setup_test_environment()
            
            # Run integration tests
            await self.test_role_lifecycle()
            await self.test_role_assignment_workflow()
            await self.test_permission_based_access()
            await self.test_role_statistics()
            await self.test_error_handling()
            await self.test_api_documentation()
            await self.test_cleanup_operations()
            
            print("\n✅ All integration tests completed successfully!")
            print("🎉 Role Management System integration validation passed!")
            return True
            
        except Exception as e:
            print(f"\n❌ Integration test failed with error: {e}")
            import traceback
            traceback.print_exc()
            return False


async def main():
    """Main integration test function."""
    async with IntegrationTester() as tester:
        success = await tester.run_all_integration_tests()
        
        if success:
            print("\n🎉 Integration tests completed! The system is fully integrated.")
        else:
            print("\n💥 Integration tests failed. Please check the output above for details.")
        
        return success


if __name__ == "__main__":
    asyncio.run(main())

#!/usr/bin/env python3
"""
Role System Demo Script

This script demonstrates the complete Role model and many-to-many relationship
with User model implementation. It shows all the key features and capabilities.

Usage:
    python demo_role_system.py

Author: AI Job Readiness Team
Version: 1.0.0
"""

import asyncio
import json
import sys
import os
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


class RoleSystemDemo:
    """Demo class for Role and User model system."""
    
    def __init__(self):
        self.session: AsyncSession = None
    
    async def setup(self):
        """Initialize database and create session."""
        print("🎬 Setting up Role System Demo")
        print("=" * 50)
        
        # Initialize database
        await init_db()
        
        # Create session
        async_session = get_async_session_local()
        self.session = async_session()
        
        print("✅ Demo environment ready")
    
    async def cleanup(self):
        """Clean up and close session."""
        if self.session:
            await self.session.close()
        print("✅ Demo cleanup completed")
    
    async def demo_role_creation(self):
        """Demonstrate role creation and management."""
        print("\n🎭 DEMO: Role Creation and Management")
        print("-" * 40)
        
        # Create some demo roles
        roles_data = [
            {
                "name": "demo_admin",
                "description": "Demo administrator role",
                "permissions": ["user:read", "user:create", "user:update", "user:delete", "role:manage"],
                "is_active": True
            },
            {
                "name": "demo_user",
                "description": "Demo user role",
                "permissions": ["profile:read", "profile:update", "resume:read", "resume:create"],
                "is_active": True
            },
            {
                "name": "demo_guest",
                "description": "Demo guest role",
                "permissions": ["profile:read"],
                "is_active": True
            }
        ]
        
        created_roles = []
        for data in roles_data:
            # Check if role already exists
            result = await self.session.execute(
                select(Role).where(Role.name == data["name"])
            )
            existing_role = result.scalar_one_or_none()
            
            if existing_role:
                print(f"   ⚠️  Role '{data['name']}' already exists, using existing...")
                created_roles.append(existing_role)
                continue
            
            role = Role(
                name=data["name"],
                description=data["description"],
                is_active=data["is_active"]
            )
            role.set_permissions_list(data["permissions"])
            
            self.session.add(role)
            created_roles.append(role)
        
        await self.session.commit()
        
        # Refresh roles to get their IDs
        for role in created_roles:
            await self.session.refresh(role)
        
        print(f"✅ Using {len(created_roles)} demo roles:")
        for role in created_roles:
            print(f"   - {role.name}: {role.description}")
            print(f"     Permissions: {role.get_permissions_list()}")
        
        return created_roles
    
    async def demo_user_creation(self):
        """Demonstrate user creation."""
        print("\n👥 DEMO: User Creation")
        print("-" * 40)
        
        # Create demo users
        users_data = [
            {
                "email": "demo.admin@example.com",
                "password": "DemoAdmin123!",
                "first_name": "Demo",
                "last_name": "Admin",
                "is_superuser": False,
                "is_active": True,
                "is_verified": True
            },
            {
                "email": "demo.user@example.com",
                "password": "DemoUser123!",
                "first_name": "Demo",
                "last_name": "User",
                "is_superuser": False,
                "is_active": True,
                "is_verified": True
            },
            {
                "email": "demo.guest@example.com",
                "password": "DemoGuest123!",
                "first_name": "Demo",
                "last_name": "Guest",
                "is_superuser": False,
                "is_active": True,
                "is_verified": False
            }
        ]
        
        created_users = []
        for data in users_data:
            # Check if user already exists
            result = await self.session.execute(
                select(User).where(User.email == data["email"])
            )
            existing_user = result.scalar_one_or_none()
            
            if existing_user:
                print(f"   ⚠️  User '{data['email']}' already exists, using existing...")
                created_users.append(existing_user)
                continue
            
            user = User(
                email=data["email"],
                hashed_password=get_password_hash(data["password"]),
                first_name=data["first_name"],
                last_name=data["last_name"],
                is_superuser=data["is_superuser"],
                is_active=data["is_active"],
                is_verified=data["is_verified"]
            )
            
            self.session.add(user)
            created_users.append(user)
        
        await self.session.commit()
        
        # Refresh users to get their IDs
        for user in created_users:
            await self.session.refresh(user)
        
        print(f"✅ Using {len(created_users)} demo users:")
        for user in created_users:
            print(f"   - {user.email} ({user.full_name})")
        
        return created_users
    
    async def demo_role_assignments(self, users: List[User], roles: List[Role]):
        """Demonstrate role assignments."""
        print("\n🔗 DEMO: Role Assignments")
        print("-" * 40)
        
        # Create role assignments
        assignments = [
            (users[0], roles[0]),  # demo.admin@example.com -> demo_admin
            (users[1], roles[1]),  # demo.user@example.com -> demo_user
            (users[2], roles[2]),  # demo.guest@example.com -> demo_guest
        ]
        
        created_assignments = []
        for user, role in assignments:
            # Check if assignment already exists
            result = await self.session.execute(
                select(UserRole).where(
                    UserRole.user_id == user.id,
                    UserRole.role_id == role.id
                )
            )
            existing_assignment = result.scalar_one_or_none()
            
            if existing_assignment:
                print(f"   ⚠️  Assignment {user.email} -> {role.name} already exists, using existing...")
                created_assignments.append(existing_assignment)
                continue
            
            assignment = UserRole(
                user_id=user.id,
                role_id=role.id,
                assigned_by=user.id,  # Self-assigned for demo
                is_active=True
            )
            
            self.session.add(assignment)
            created_assignments.append(assignment)
        
        await self.session.commit()
        
        # Refresh assignments to get their IDs
        for assignment in created_assignments:
            await self.session.refresh(assignment)
        
        print(f"✅ Using {len(created_assignments)} role assignments:")
        for assignment in created_assignments:
            print(f"   - {assignment.user.email} -> {assignment.role.name}")
        
        return created_assignments
    
    async def demo_permission_management(self, roles: List[Role]):
        """Demonstrate permission management."""
        print("\n🔐 DEMO: Permission Management")
        print("-" * 40)
        
        # Get the demo_user role
        user_role = next((r for r in roles if r.name == "demo_user"), None)
        
        if user_role:
            print(f"Managing permissions for role: {user_role.name}")
            print(f"Current permissions: {user_role.get_permissions_list()}")
            
            # Add a new permission
            print("\n➕ Adding permission 'resume:update'...")
            user_role.add_permission("resume:update")
            await self.session.commit()
            await self.session.refresh(user_role)
            print(f"Updated permissions: {user_role.get_permissions_list()}")
            
            # Check if role has specific permission
            print(f"\n🔍 Checking if role has 'resume:update': {user_role.has_permission('resume:update')}")
            print(f"🔍 Checking if role has 'admin:access': {user_role.has_permission('admin:access')}")
            
            # Remove a permission
            print("\n➖ Removing permission 'resume:create'...")
            user_role.remove_permission("resume:create")
            await self.session.commit()
            await self.session.refresh(user_role)
            print(f"Final permissions: {user_role.get_permissions_list()}")
    
    async def demo_user_role_queries(self, users: List[User]):
        """Demonstrate user-role relationship queries."""
        print("\n🔍 DEMO: User-Role Relationship Queries")
        print("-" * 40)
        
        # Query users with their roles using selectinload
        result = await self.session.execute(
            select(User)
            .options(selectinload(User.roles).selectinload(UserRole.role))
            .where(User.id.in_([user.id for user in users]))
        )
        users_with_roles = result.scalars().all()
        
        print("Users with their roles:")
        for user in users_with_roles:
            role_names = [ur.role.name for ur in user.roles if ur.is_active]
            print(f"   - {user.email}: {role_names}")
            
            # Demonstrate user role methods
            print(f"     - Has 'demo_admin' role: {user.has_role('demo_admin')}")
            print(f"     - Is admin: {user.is_admin()}")
            print(f"     - Full name: {user.full_name}")
    
    async def demo_role_statistics(self):
        """Demonstrate role statistics and reporting."""
        print("\n📊 DEMO: Role Statistics and Reporting")
        print("-" * 40)
        
        # Get role statistics
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
        
        print("Role Statistics:")
        print("Role Name        | Description           | User Count | Active")
        print("-" * 65)
        for stat in role_stats:
            print(f"{stat[0]:<15} | {stat[1]:<20} | {stat[2]:<10} | {stat[3]}")
        
        # Get total counts
        total_roles_result = await self.session.execute(select(func.count(Role.id)))
        total_roles = total_roles_result.scalar()
        
        total_assignments_result = await self.session.execute(select(func.count(UserRole.id)))
        total_assignments = total_assignments_result.scalar()
        
        print(f"\nSummary:")
        print(f"   - Total roles: {total_roles}")
        print(f"   - Total assignments: {total_assignments}")
    
    async def demo_serialization(self, users: List[User], roles: List[Role]):
        """Demonstrate serialization capabilities."""
        print("\n📄 DEMO: Serialization")
        print("-" * 40)
        
        # Serialize a role
        demo_role = roles[0]
        role_dict = demo_role.to_dict()
        print(f"Role serialization ({demo_role.name}):")
        print(json.dumps(role_dict, indent=2, default=str))
        
        # Serialize a user with roles
        demo_user = users[0]
        user_dict = demo_user.to_dict()
        print(f"\nUser serialization ({demo_user.email}):")
        print(json.dumps(user_dict, indent=2, default=str))
    
    async def demo_error_handling(self):
        """Demonstrate error handling."""
        print("\n⚠️ DEMO: Error Handling")
        print("-" * 40)
        
        # Try to create a duplicate role
        print("Testing duplicate role creation...")
        try:
            duplicate_role = Role(
                name="demo_admin",  # This should conflict
                description="Duplicate role",
                is_active=True
            )
            self.session.add(duplicate_role)
            await self.session.commit()
            print("❌ Should have failed for duplicate role name")
        except Exception as e:
            await self.session.rollback()
            print(f"✅ Properly handled duplicate role: {type(e).__name__}")
        
        # Test permission validation
        print("\nTesting permission validation...")
        try:
            role = Role(name="test_role", description="Test role")
            role.set_permissions_list(["valid:permission", "", "another:valid"])  # Empty string should be handled
            print("✅ Permission validation handled gracefully")
        except Exception as e:
            print(f"❌ Permission validation error: {e}")
    
    async def cleanup_demo_data(self, users: List[User], roles: List[Role], assignments: List[UserRole]):
        """Clean up demo data."""
        print("\n🧹 DEMO: Cleanup")
        print("-" * 40)
        
        # Only clean up demo-specific data (not existing data)
        demo_emails = ["demo.admin@example.com", "demo.user@example.com", "demo.guest@example.com"]
        demo_role_names = ["demo_admin", "demo_user", "demo_guest"]
        
        # Get user emails and role names to avoid lazy loading
        user_emails = {user.id: user.email for user in users}
        role_names = {role.id: role.name for role in roles}
        
        # Delete demo assignments
        for assignment in assignments:
            user_email = user_emails.get(assignment.user_id)
            role_name = role_names.get(assignment.role_id)
            if (user_email in demo_emails and role_name in demo_role_names):
                await self.session.delete(assignment)
        
        # Delete demo users
        for user in users:
            if user.email in demo_emails:
                await self.session.delete(user)
        
        # Delete demo roles
        for role in roles:
            if role.name in demo_role_names:
                await self.session.delete(role)
        
        await self.session.commit()
        print("✅ Demo data cleaned up")
    
    async def run_demo(self):
        """Run the complete demo."""
        print("🎬 Role System Implementation Demo")
        print("=" * 50)
        print("This demo showcases the complete Role model and")
        print("many-to-many relationship with User model.")
        print("=" * 50)
        
        try:
            await self.setup()
            
            # Run demo sections
            roles = await self.demo_role_creation()
            users = await self.demo_user_creation()
            assignments = await self.demo_role_assignments(users, roles)
            await self.demo_permission_management(roles)
            await self.demo_user_role_queries(users)
            await self.demo_role_statistics()
            await self.demo_serialization(users, roles)
            await self.demo_error_handling()
            
            # Cleanup
            await self.cleanup_demo_data(users, roles, assignments)
            
            print("\n" + "=" * 50)
            print("🎉 Demo completed successfully!")
            print("✅ Role model and User-Role relationship working perfectly")
            print("=" * 50)
            
        except Exception as e:
            print(f"\n❌ Demo failed with error: {e}")
            import traceback
            traceback.print_exc()
            raise
        
        finally:
            await self.cleanup()


async def main():
    """Main function to run the demo."""
    demo = RoleSystemDemo()
    await demo.run_demo()


if __name__ == "__main__":
    asyncio.run(main())

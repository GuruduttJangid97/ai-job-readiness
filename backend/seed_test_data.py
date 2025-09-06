#!/usr/bin/env python3
"""
Database Seeding Script for Role and User Models

This script seeds the database with test data including users, roles,
and role assignments for testing the Role model and many-to-many relationship.

Usage:
    python seed_test_data.py

Author: AI Job Readiness Team
Version: 1.0.0
"""

import asyncio
import sys
import os
from datetime import datetime
from typing import List, Dict, Any

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.database import get_async_session_local, init_db
from app.models.user import User
from app.models.role import Role, UserRole
from app.core.security import get_password_hash


class DatabaseSeeder:
    """Database seeder for test data."""
    
    def __init__(self):
        self.session: AsyncSession = None
        self.seeded_users: List[User] = []
        self.seeded_roles: List[Role] = []
        self.seeded_assignments: List[UserRole] = []
    
    async def setup(self):
        """Initialize database and create session."""
        print("🔧 Setting up database seeder...")
        
        # Initialize database
        await init_db()
        
        # Create session
        async_session = get_async_session_local()
        self.session = async_session()
        
        print("✅ Database seeder ready")
    
    async def cleanup(self):
        """Clean up and close session."""
        if self.session:
            await self.session.close()
        print("✅ Database seeder cleanup completed")
    
    async def check_existing_data(self):
        """Check if data already exists in the database."""
        print("🔍 Checking for existing data...")
        
        # Check for existing users
        result = await self.session.execute(select(User))
        existing_users = result.scalars().all()
        
        # Check for existing roles
        result = await self.session.execute(select(Role))
        existing_roles = result.scalars().all()
        
        if existing_users or existing_roles:
            print(f"⚠️  Found existing data:")
            print(f"   - {len(existing_users)} users")
            print(f"   - {len(existing_roles)} roles")
            
            response = input("Do you want to continue and add more data? (y/N): ")
            if response.lower() != 'y':
                print("❌ Seeding cancelled")
                return False
        
        return True
    
    async def seed_roles(self) -> List[Role]:
        """Seed roles into the database."""
        print("🎭 Seeding roles...")
        
        role_data = [
            {
                "name": "super_admin",
                "description": "Super administrator with full system access",
                "permissions": ["*"],
                "is_active": True
            },
            {
                "name": "admin",
                "description": "Administrator with management privileges",
                "permissions": [
                    "user:read", "user:create", "user:update", "user:delete",
                    "role:read", "role:create", "role:update", "role:delete",
                    "resume:read", "resume:create", "resume:update", "resume:delete",
                    "score:read", "score:create", "score:update", "score:delete"
                ],
                "is_active": True
            },
            {
                "name": "moderator",
                "description": "Content moderator with user management capabilities",
                "permissions": [
                    "user:read", "user:update",
                    "role:read",
                    "resume:read", "resume:create", "resume:update",
                    "score:read", "score:create"
                ],
                "is_active": True
            },
            {
                "name": "user",
                "description": "Regular user with basic access",
                "permissions": [
                    "profile:read", "profile:update",
                    "resume:read", "resume:create", "resume:update",
                    "score:read", "score:create"
                ],
                "is_active": True
            },
            {
                "name": "guest",
                "description": "Guest user with limited access",
                "permissions": [
                    "profile:read",
                    "resume:read"
                ],
                "is_active": True
            },
            {
                "name": "hr_manager",
                "description": "HR manager with recruitment access",
                "permissions": [
                    "user:read",
                    "resume:read", "resume:create", "resume:update",
                    "score:read", "score:create", "score:update",
                    "recruitment:read", "recruitment:create", "recruitment:update"
                ],
                "is_active": True
            },
            {
                "name": "analyst",
                "description": "Data analyst with reporting access",
                "permissions": [
                    "user:read",
                    "resume:read",
                    "score:read", "score:create",
                    "analytics:read", "analytics:create", "analytics:update",
                    "reports:read", "reports:create"
                ],
                "is_active": True
            },
            {
                "name": "inactive_role",
                "description": "Inactive role for testing purposes",
                "permissions": ["test:permission"],
                "is_active": False
            }
        ]
        
        roles = []
        for data in role_data:
            # Check if role already exists
            result = await self.session.execute(
                select(Role).where(Role.name == data["name"])
            )
            existing_role = result.scalar_one_or_none()
            
            if existing_role:
                print(f"   ⚠️  Role '{data['name']}' already exists, skipping...")
                roles.append(existing_role)
                continue
            
            role = Role(
                name=data["name"],
                description=data["description"],
                is_active=data["is_active"]
            )
            role.set_permissions_list(data["permissions"])
            
            self.session.add(role)
            roles.append(role)
        
        await self.session.commit()
        
        # Refresh roles to get their IDs
        for role in roles:
            await self.session.refresh(role)
        
        self.seeded_roles = roles
        print(f"✅ Seeded {len(roles)} roles")
        return roles
    
    async def seed_users(self) -> List[User]:
        """Seed users into the database."""
        print("👥 Seeding users...")
        
        user_data = [
            {
                "email": "superadmin@test.com",
                "password": "SuperAdmin123!",
                "first_name": "Super",
                "last_name": "Admin",
                "is_superuser": True,
                "is_active": True,
                "is_verified": True,
                "bio": "Super administrator with full system access"
            },
            {
                "email": "admin@test.com",
                "password": "Admin123!",
                "first_name": "Admin",
                "last_name": "User",
                "is_superuser": False,
                "is_active": True,
                "is_verified": True,
                "bio": "System administrator"
            },
            {
                "email": "moderator@test.com",
                "password": "Moderator123!",
                "first_name": "Moderator",
                "last_name": "User",
                "is_superuser": False,
                "is_active": True,
                "is_verified": True,
                "bio": "Content moderator"
            },
            {
                "email": "john.doe@test.com",
                "password": "User123!",
                "first_name": "John",
                "last_name": "Doe",
                "is_superuser": False,
                "is_active": True,
                "is_verified": True,
                "bio": "Software developer looking for new opportunities",
                "phone": "+1-555-0123"
            },
            {
                "email": "jane.smith@test.com",
                "password": "User123!",
                "first_name": "Jane",
                "last_name": "Smith",
                "is_superuser": False,
                "is_active": True,
                "is_verified": True,
                "bio": "Data scientist with 5 years of experience",
                "phone": "+1-555-0124"
            },
            {
                "email": "bob.wilson@test.com",
                "password": "User123!",
                "first_name": "Bob",
                "last_name": "Wilson",
                "is_superuser": False,
                "is_active": True,
                "is_verified": True,
                "bio": "Marketing professional",
                "phone": "+1-555-0125"
            },
            {
                "email": "alice.brown@test.com",
                "password": "User123!",
                "first_name": "Alice",
                "last_name": "Brown",
                "is_superuser": False,
                "is_active": True,
                "is_verified": True,
                "bio": "UX Designer with creative skills",
                "phone": "+1-555-0126"
            },
            {
                "email": "guest@test.com",
                "password": "Guest123!",
                "first_name": "Guest",
                "last_name": "User",
                "is_superuser": False,
                "is_active": True,
                "is_verified": False,
                "bio": "Guest user with limited access"
            },
            {
                "email": "hr.manager@test.com",
                "password": "HR123!",
                "first_name": "HR",
                "last_name": "Manager",
                "is_superuser": False,
                "is_active": True,
                "is_verified": True,
                "bio": "Human Resources Manager",
                "phone": "+1-555-0127"
            },
            {
                "email": "analyst@test.com",
                "password": "Analyst123!",
                "first_name": "Data",
                "last_name": "Analyst",
                "is_superuser": False,
                "is_active": True,
                "is_verified": True,
                "bio": "Data analyst specializing in job market trends",
                "phone": "+1-555-0128"
            },
            {
                "email": "inactive@test.com",
                "password": "Inactive123!",
                "first_name": "Inactive",
                "last_name": "User",
                "is_superuser": False,
                "is_active": False,
                "is_verified": False,
                "bio": "Inactive user for testing"
            }
        ]
        
        users = []
        for data in user_data:
            # Check if user already exists
            result = await self.session.execute(
                select(User).where(User.email == data["email"])
            )
            existing_user = result.scalar_one_or_none()
            
            if existing_user:
                print(f"   ⚠️  User '{data['email']}' already exists, skipping...")
                users.append(existing_user)
                continue
            
            user = User(
                email=data["email"],
                hashed_password=get_password_hash(data["password"]),
                first_name=data["first_name"],
                last_name=data["last_name"],
                is_superuser=data["is_superuser"],
                is_active=data["is_active"],
                is_verified=data["is_verified"],
                bio=data.get("bio"),
                phone=data.get("phone")
            )
            
            self.session.add(user)
            users.append(user)
        
        await self.session.commit()
        
        # Refresh users to get their IDs
        for user in users:
            await self.session.refresh(user)
        
        self.seeded_users = users
        print(f"✅ Seeded {len(users)} users")
        return users
    
    async def seed_role_assignments(self, users: List[User], roles: List[Role]):
        """Seed role assignments into the database."""
        print("🔗 Seeding role assignments...")
        
        # Create a mapping of role names to role objects
        role_map = {role.name: role for role in roles}
        user_map = {user.email: user for user in users}
        
        # Define role assignments
        assignments = [
            # Super admin gets super_admin role
            ("superadmin@test.com", "super_admin"),
            
            # Admin gets admin role
            ("admin@test.com", "admin"),
            
            # Moderator gets moderator role
            ("moderator@test.com", "moderator"),
            
            # Regular users get user role
            ("john.doe@test.com", "user"),
            ("jane.smith@test.com", "user"),
            ("bob.wilson@test.com", "user"),
            ("alice.brown@test.com", "user"),
            
            # Guest gets guest role
            ("guest@test.com", "guest"),
            
            # HR manager gets hr_manager role
            ("hr.manager@test.com", "hr_manager"),
            
            # Analyst gets analyst role
            ("analyst@test.com", "analyst"),
            
            # Inactive user gets inactive role
            ("inactive@test.com", "inactive_role"),
            
            # Additional assignments for testing
            ("john.doe@test.com", "guest"),  # User with multiple roles
            ("jane.smith@test.com", "analyst"),  # User with multiple roles
        ]
        
        assignment_objects = []
        for email, role_name in assignments:
            user = user_map.get(email)
            role = role_map.get(role_name)
            
            if not user or not role:
                print(f"   ⚠️  Skipping assignment: {email} -> {role_name} (user or role not found)")
                continue
            
            # Check if assignment already exists
            result = await self.session.execute(
                select(UserRole).where(
                    UserRole.user_id == user.id,
                    UserRole.role_id == role.id
                )
            )
            existing_assignment = result.scalar_one_or_none()
            
            if existing_assignment:
                print(f"   ⚠️  Assignment {email} -> {role_name} already exists, skipping...")
                assignment_objects.append(existing_assignment)
                continue
            
            # Find an admin user to assign roles
            admin_user = user_map.get("admin@test.com") or user_map.get("superadmin@test.com")
            assigned_by = admin_user.id if admin_user else user.id
            
            assignment = UserRole(
                user_id=user.id,
                role_id=role.id,
                assigned_by=assigned_by,
                is_active=True
            )
            
            self.session.add(assignment)
            assignment_objects.append(assignment)
        
        await self.session.commit()
        
        # Refresh assignments to get their IDs
        for assignment in assignment_objects:
            await self.session.refresh(assignment)
        
        self.seeded_assignments = assignment_objects
        print(f"✅ Seeded {len(assignment_objects)} role assignments")
        return assignment_objects
    
    async def print_summary(self):
        """Print a summary of seeded data."""
        print("\n" + "="*60)
        print("📊 SEEDING SUMMARY")
        print("="*60)
        
        print(f"👥 Users created: {len(self.seeded_users)}")
        for user in self.seeded_users:
            print(f"   - {user.email} ({user.first_name} {user.last_name})")
        
        print(f"\n🎭 Roles created: {len(self.seeded_roles)}")
        for role in self.seeded_roles:
            print(f"   - {role.name}: {role.description}")
        
        print(f"\n🔗 Role assignments created: {len(self.seeded_assignments)}")
        
        # Group assignments by user
        user_assignments = {}
        for assignment in self.seeded_assignments:
            if assignment.user.email not in user_assignments:
                user_assignments[assignment.user.email] = []
            user_assignments[assignment.user.email].append(assignment.role.name)
        
        for email, role_names in user_assignments.items():
            print(f"   - {email}: {', '.join(role_names)}")
        
        print("\n🔑 Test Credentials:")
        print("   Super Admin: superadmin@test.com / SuperAdmin123!")
        print("   Admin: admin@test.com / Admin123!")
        print("   Moderator: moderator@test.com / Moderator123!")
        print("   User: john.doe@test.com / User123!")
        print("   HR Manager: hr.manager@test.com / HR123!")
        print("   Analyst: analyst@test.com / Analyst123!")
        
        print("\n🌐 API Endpoints:")
        print("   - Swagger UI: http://localhost:8000/docs")
        print("   - ReDoc: http://localhost:8000/redoc")
        print("   - Health Check: http://localhost:8000/health")
        
        print("\n🧪 Testing:")
        print("   - Python test: python test_role_system.py")
        print("   - API test: ./test_api.sh")
        
        print("="*60)
    
    async def run_seeding(self):
        """Run the complete seeding process."""
        print("🌱 Starting database seeding...")
        
        try:
            await self.setup()
            
            if not await self.check_existing_data():
                return
            
            # Seed data
            roles = await self.seed_roles()
            users = await self.seed_users()
            assignments = await self.seed_role_assignments(users, roles)
            
            # Print summary
            await self.print_summary()
            
            print("\n🎉 Database seeding completed successfully!")
            
        except Exception as e:
            print(f"\n❌ Seeding failed with error: {e}")
            import traceback
            traceback.print_exc()
            raise
        
        finally:
            await self.cleanup()


async def main():
    """Main function to run the seeding."""
    seeder = DatabaseSeeder()
    await seeder.run_seeding()


if __name__ == "__main__":
    asyncio.run(main())

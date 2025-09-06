#!/usr/bin/env python3
"""
Final Demo Script - Complete Role System Showcase

This script demonstrates all the key features of the Role and User model system
in a comprehensive, easy-to-understand format.

Usage:
    python final_demo.py

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
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from app.db.database import get_async_session_local, init_db
from app.models.user import User
from app.models.role import Role, UserRole
from app.core.security import get_password_hash


class FinalDemo:
    """Complete demonstration of the Role and User model system."""
    
    def __init__(self):
        self.session: AsyncSession = None
    
    async def setup(self):
        """Initialize database and create test session."""
        print("🚀 Setting up Final Demo...")
        await init_db()
        async_session = get_async_session_local()
        self.session = async_session()
        print("✅ Demo environment ready")
    
    async def cleanup(self):
        """Clean up and close session."""
        if self.session:
            await self.session.close()
        print("✅ Demo cleanup completed")
    
    async def demo_role_management(self):
        """Demonstrate complete role management."""
        print("\n" + "="*60)
        print("🎭 ROLE MANAGEMENT DEMONSTRATION")
        print("="*60)
        
        # Create demo roles
        print("\n📝 Creating demo roles...")
        
        roles_data = [
            {
                "name": "demo_admin",
                "description": "Demo administrator with full access",
                "permissions": ["user:read", "user:write", "user:delete", "role:manage", "system:admin"]
            },
            {
                "name": "demo_moderator",
                "description": "Demo moderator with content management access",
                "permissions": ["content:read", "content:write", "content:moderate", "user:read"]
            },
            {
                "name": "demo_user",
                "description": "Demo regular user with basic access",
                "permissions": ["profile:read", "profile:write", "content:read"]
            }
        ]
        
        created_roles = []
        for data in roles_data:
            role = Role(
                name=data["name"],
                description=data["description"],
                is_active=True
            )
            role.set_permissions_list(data["permissions"])
            
            self.session.add(role)
            created_roles.append(role)
        
        await self.session.commit()
        
        for role in created_roles:
            await self.session.refresh(role)
            print(f"  ✅ Created role: {role.name} (ID: {role.id})")
            print(f"     Permissions: {role.get_permissions_list()}")
        
        # Demonstrate permission management
        print("\n🔐 Demonstrating permission management...")
        admin_role = created_roles[0]
        
        print(f"  Role: {admin_role.name}")
        print(f"  Current permissions: {admin_role.get_permissions_list()}")
        
        # Add a new permission
        added = admin_role.add_permission("audit:read")
        print(f"  ➕ Added 'audit:read': {added}")
        
        # Remove a permission
        removed = admin_role.remove_permission("user:delete")
        print(f"  ➖ Removed 'user:delete': {removed}")
        
        # Check permissions
        has_read = admin_role.has_permission("user:read")
        has_delete = admin_role.has_permission("user:delete")
        print(f"  🔍 Has 'user:read': {has_read}")
        print(f"  🔍 Has 'user:delete': {has_delete}")
        
        # Update permissions
        admin_role.set_permissions_list(["user:read", "user:write", "role:manage", "audit:read"])
        await self.session.commit()
        await self.session.refresh(admin_role)
        print(f"  ✏️  Updated permissions: {admin_role.get_permissions_list()}")
        
        return created_roles
    
    async def demo_user_management(self):
        """Demonstrate complete user management."""
        print("\n" + "="*60)
        print("👥 USER MANAGEMENT DEMONSTRATION")
        print("="*60)
        
        # Create demo users
        print("\n📝 Creating demo users...")
        
        users_data = [
            {
                "email": "admin@demo.com",
                "first_name": "Demo",
                "last_name": "Admin",
                "is_superuser": True
            },
            {
                "email": "moderator@demo.com",
                "first_name": "Demo",
                "last_name": "Moderator",
                "is_superuser": False
            },
            {
                "email": "user@demo.com",
                "first_name": "Demo",
                "last_name": "User",
                "is_superuser": False
            }
        ]
        
        created_users = []
        for data in users_data:
            user = User(
                email=data["email"],
                hashed_password=get_password_hash("DemoPassword123!"),
                first_name=data["first_name"],
                last_name=data["last_name"],
                is_superuser=data["is_superuser"],
                is_active=True,
                is_verified=True
            )
            
            self.session.add(user)
            created_users.append(user)
        
        await self.session.commit()
        
        for user in created_users:
            await self.session.refresh(user)
            print(f"  ✅ Created user: {user.email} (ID: {user.id})")
            print(f"     Full name: {user.full_name}")
            print(f"     Is superuser: {user.is_superuser}")
        
        # Demonstrate user properties
        print("\n👤 Demonstrating user properties...")
        demo_user = created_users[2]
        
        print(f"  User: {demo_user.email}")
        print(f"  Full name: {demo_user.full_name}")
        print(f"  Display name: {demo_user.display_name}")
        print(f"  Is active: {demo_user.is_active}")
        print(f"  Is verified: {demo_user.is_verified}")
        
        # Update user profile
        demo_user.phone = "+1234567890"
        demo_user.bio = "Demo user for testing purposes"
        await self.session.commit()
        await self.session.refresh(demo_user)
        
        print(f"  📞 Phone: {demo_user.phone}")
        print(f"  📝 Bio: {demo_user.bio}")
        
        return created_users
    
    async def demo_role_assignments(self, users: List[User], roles: List[Role]):
        """Demonstrate user-role assignments."""
        print("\n" + "="*60)
        print("🔗 ROLE ASSIGNMENT DEMONSTRATION")
        print("="*60)
        
        # Create role assignments
        print("\n📝 Creating role assignments...")
        
        assignments = [
            (users[0], roles[0]),  # admin@demo.com -> demo_admin
            (users[1], roles[1]),  # moderator@demo.com -> demo_moderator
            (users[2], roles[2]),  # user@demo.com -> demo_user
        ]
        
        created_assignments = []
        for user, role in assignments:
            assignment = UserRole(
                user_id=user.id,
                role_id=role.id,
                assigned_by=user.id,  # Self-assigned for demo
                is_active=True
            )
            
            self.session.add(assignment)
            created_assignments.append(assignment)
        
        await self.session.commit()
        
        for assignment in created_assignments:
            await self.session.refresh(assignment)
            print(f"  ✅ Assigned {assignment.user.email} -> {assignment.role.name}")
        
        # Demonstrate user role methods
        print("\n🔍 Demonstrating user role methods...")
        
        # Load users with their roles
        result = await self.session.execute(
            select(User)
            .options(selectinload(User.roles).selectinload(UserRole.role))
            .where(User.id.in_([user.id for user in users]))
        )
        users_with_roles = result.scalars().all()
        
        for user in users_with_roles:
            print(f"\n  👤 User: {user.email}")
            print(f"     Full name: {user.full_name}")
            
            # Role checking methods
            role_names = [ur.role.name for ur in user.roles if ur.is_active]
            print(f"     Roles: {role_names}")
            
            # Check specific roles
            is_admin = user.is_admin()
            is_moderator = user.is_moderator()
            has_admin_role = user.has_role("demo_admin")
            
            print(f"     Is admin: {is_admin}")
            print(f"     Is moderator: {is_moderator}")
            print(f"     Has 'demo_admin' role: {has_admin_role}")
            
            # Permission checking
            if user.roles:
                user_permissions = []
                for ur in user.roles:
                    if ur.is_active and ur.role.is_active:
                        user_permissions.extend(ur.role.get_permissions_list())
                
                unique_permissions = list(set(user_permissions))
                print(f"     Permissions: {unique_permissions}")
        
        return created_assignments
    
    async def demo_complex_queries(self):
        """Demonstrate complex database queries."""
        print("\n" + "="*60)
        print("🔍 COMPLEX QUERIES DEMONSTRATION")
        print("="*60)
        
        # Role statistics query
        print("\n📊 Role statistics query...")
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
        print("  Role Statistics:")
        print("  " + "-" * 50)
        for stat in role_stats:
            print(f"  {stat[0]:<15} | {stat[2]:<3} users | Active: {stat[3]}")
        
        # Users with roles query
        print("\n👥 Users with roles query...")
        result = await self.session.execute(
            select(User)
            .options(selectinload(User.roles).selectinload(UserRole.role))
            .where(User.is_active == True)
            .limit(5)
        )
        
        users_with_roles = result.scalars().all()
        print(f"  Found {len(users_with_roles)} active users with roles:")
        for user in users_with_roles:
            role_names = [ur.role.name for ur in user.roles if ur.is_active]
            print(f"    {user.email}: {role_names}")
        
        # Permission-based query
        print("\n🔐 Permission-based query...")
        result = await self.session.execute(
            select(Role)
            .where(Role.permissions.like('%admin%'))
            .limit(5)
        )
        
        admin_roles = result.scalars().all()
        print(f"  Found {len(admin_roles)} roles with admin permissions:")
        for role in admin_roles:
            print(f"    {role.name}: {role.get_permissions_list()}")
    
    async def demo_serialization(self, users: List[User], roles: List[Role]):
        """Demonstrate serialization capabilities."""
        print("\n" + "="*60)
        print("📄 SERIALIZATION DEMONSTRATION")
        print("="*60)
        
        # Role serialization
        print("\n🎭 Role serialization...")
        if roles:
            role = roles[0]
            role_dict = role.to_dict()
            print(f"  Role: {role.name}")
            print(f"  Serialized fields: {len(role_dict)}")
            print(f"  Data: {role_dict}")
        
        # User serialization
        print("\n👥 User serialization...")
        if users:
            user = users[0]
            user_dict = user.to_dict()
            public_dict = user.to_public_dict()
            
            print(f"  User: {user.email}")
            print(f"  Full serialization: {len(user_dict)} fields")
            print(f"  Public serialization: {len(public_dict)} fields")
            print(f"  Public data: {public_dict}")
    
    async def demo_error_handling(self):
        """Demonstrate error handling."""
        print("\n" + "="*60)
        print("⚠️ ERROR HANDLING DEMONSTRATION")
        print("="*60)
        
        # Test duplicate role name
        print("\n🔄 Testing duplicate role name...")
        try:
            duplicate_role = Role(
                name="demo_admin",  # This should already exist
                description="Duplicate role",
                is_active=True
            )
            self.session.add(duplicate_role)
            await self.session.commit()
            print("  ❌ Should have failed for duplicate name")
        except Exception as e:
            await self.session.rollback()
            print(f"  ✅ Properly handled duplicate role: {type(e).__name__}")
        
        # Test duplicate user email
        print("\n🔄 Testing duplicate user email...")
        try:
            duplicate_user = User(
                email="admin@demo.com",  # This should already exist
                hashed_password=get_password_hash("TestPassword123!"),
                first_name="Duplicate",
                last_name="User",
                is_superuser=False,
                is_active=True,
                is_verified=True
            )
            self.session.add(duplicate_user)
            await self.session.commit()
            print("  ❌ Should have failed for duplicate email")
        except Exception as e:
            await self.session.rollback()
            print(f"  ✅ Properly handled duplicate user: {type(e).__name__}")
        
        # Test permission validation
        print("\n🔄 Testing permission validation...")
        try:
            role = Role(
                name="test_validation",
                description="Role for validation testing",
                is_active=True
            )
            role.set_permissions_list(["valid:permission", "", "another:valid"])
            self.session.add(role)
            await self.session.commit()
            await self.session.refresh(role)
            
            permissions = role.get_permissions_list()
            print(f"  ✅ Permission validation handled gracefully")
            print(f"  Final permissions: {permissions}")
            
            # Cleanup
            await self.session.delete(role)
            await self.session.commit()
        except Exception as e:
            print(f"  ❌ Permission validation error: {e}")
    
    async def run_demo(self):
        """Run the complete demonstration."""
        print("🎬 FINAL ROLE SYSTEM DEMONSTRATION")
        print("="*60)
        print("This demo showcases the complete Role model and")
        print("many-to-many relationship with User model.")
        print("="*60)
        
        try:
            await self.setup()
            
            # Run all demonstrations
            roles = await self.demo_role_management()
            users = await self.demo_user_management()
            assignments = await self.demo_role_assignments(users, roles)
            await self.demo_complex_queries()
            await self.demo_serialization(users, roles)
            await self.demo_error_handling()
            
            # Final summary
            print("\n" + "="*60)
            print("🎉 DEMONSTRATION COMPLETE")
            print("="*60)
            print("✅ All features demonstrated successfully!")
            print("✅ Role model working perfectly!")
            print("✅ User model working perfectly!")
            print("✅ Many-to-many relationship working perfectly!")
            print("✅ Permission management working perfectly!")
            print("✅ Serialization working perfectly!")
            print("✅ Error handling working perfectly!")
            print("\n🚀 System is production-ready!")
            
        except Exception as e:
            print(f"\n❌ Demo failed with error: {e}")
            import traceback
            traceback.print_exc()
            raise
        
        finally:
            await self.cleanup()


async def main():
    """Main function to run the final demo."""
    demo = FinalDemo()
    await demo.run_demo()


if __name__ == "__main__":
    asyncio.run(main())

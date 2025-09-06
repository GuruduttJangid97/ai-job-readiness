#!/usr/bin/env python3
"""
Simple test script for Role model and User-Role relationship functionality.

This script tests the role management system by creating tables directly
and testing the models without relying on migrations.

Author: AI Job Readiness Team
Version: 1.0.0
"""

import asyncio
import sys
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, delete
from sqlalchemy.orm import selectinload

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

from app.db.database import get_async_session_local, init_db
from app.models.user import User
from app.models.role import Role, UserRole


async def test_role_system():
    """Test the complete role system."""
    print("🚀 Starting Role Management System Test\n")
    
    try:
        # Initialize database
        print("📊 Initializing database...")
        await init_db()
        print("✅ Database initialized successfully")
        
        # Clear existing data for clean test
        async with get_async_session_local()() as db:
            # Delete all existing data
            await db.execute(delete(UserRole))
            await db.execute(delete(Role))
            await db.execute(delete(User))
            await db.commit()
            print("🧹 Cleared existing test data\n")

        async with get_async_session_local()() as db:
            # Test 1: Create roles
            print("\n🧪 Test 1: Creating roles...")
            
            admin_role = Role(
                name="admin",
                description="Administrator role with full access",
                is_active=True
            )
            admin_role.set_permissions_list(["read", "write", "delete", "manage_users", "manage_roles"])
            
            user_role = Role(
                name="user",
                description="Regular user role with basic access",
                is_active=True
            )
            user_role.set_permissions_list(["read", "write"])
            
            db.add(admin_role)
            db.add(user_role)
            await db.commit()
            
            print(f"✅ Created role: {admin_role.name} (ID: {admin_role.id})")
            print(f"✅ Created role: {user_role.name} (ID: {user_role.id})")
            
            # Test 2: Create users
            print("\n🧪 Test 2: Creating users...")
            
            admin_user = User(
                email="admin@test.com",
                hashed_password="hashed_password_123",
                first_name="Admin",
                last_name="User",
                is_active=True,
                is_superuser=True,
                is_verified=True
            )
            
            regular_user = User(
                email="user@test.com",
                hashed_password="hashed_password_123",
                first_name="Regular",
                last_name="User",
                is_active=True,
                is_superuser=False,
                is_verified=True
            )
            
            db.add(admin_user)
            db.add(regular_user)
            await db.commit()
            
            print(f"✅ Created user: {admin_user.email} (ID: {admin_user.id})")
            print(f"✅ Created user: {regular_user.email} (ID: {regular_user.id})")
            
            # Test 3: Assign roles to users
            print("\n🧪 Test 3: Assigning roles to users...")
            
            admin_assignment = UserRole(
                user_id=admin_user.id,
                role_id=admin_role.id,
                assigned_by=admin_user.id,
                is_active=True
            )
            
            user_assignment = UserRole(
                user_id=regular_user.id,
                role_id=user_role.id,
                assigned_by=admin_user.id,
                is_active=True
            )
            
            db.add(admin_assignment)
            db.add(user_assignment)
            await db.commit()
            
            print(f"✅ Assigned {admin_role.name} role to {admin_user.email}")
            print(f"✅ Assigned {user_role.name} role to {regular_user.email}")
            
            # Test 4: Query users with roles
            print("\n🧪 Test 4: Querying users with roles...")
            
            users_result = await db.execute(
                select(User).options(selectinload(User.roles).selectinload(UserRole.role))
            )
            users = users_result.scalars().all()
            
            for user in users:
                print(f"\n👤 User: {user.email}")
                print(f"   Full Name: {user.full_name}")
                print(f"   Roles: {user.get_role_names()}")
                print(f"   Is Admin: {user.is_admin()}")
                
                for user_role in user.roles:
                    if user_role.role:
                        print(f"   - {user_role.role.name}: {user_role.role.description}")
                        print(f"     Permissions: {user_role.role.get_permissions_list()}")
            
            # Test 5: Test role permissions
            print("\n🧪 Test 5: Testing role permissions...")
            
            print(f"🔧 Admin role permissions: {admin_role.get_permissions_list()}")
            print(f"   Has 'manage_users' permission: {admin_role.has_permission('manage_users')}")
            print(f"   Has 'delete' permission: {admin_role.has_permission('delete')}")
            
            # Get the user role from the regular user
            regular_user_role = None
            for user_role_entry in regular_user.roles:
                if user_role_entry.role and user_role_entry.role.name == "user":
                    regular_user_role = user_role_entry.role
                    break
            
            if regular_user_role:
                print(f"🔧 User role permissions: {regular_user_role.get_permissions_list()}")
                print(f"   Has 'read' permission: {regular_user_role.has_permission('read')}")
                print(f"   Has 'delete' permission: {regular_user_role.has_permission('delete')}")
            else:
                print("❌ Could not find user role")
            
            # Test 6: Test permission operations
            print("\n🧪 Test 6: Testing permission operations...")
            
            # Add a new permission to admin role
            admin_role.add_permission("manage_system")
            print(f"   Added 'manage_system' permission to admin role")
            print(f"   Updated permissions: {admin_role.get_permissions_list()}")
            
            # Check if permission exists
            has_manage = admin_role.has_permission("manage_system")
            print(f"   Has 'manage_system' permission: {has_manage}")
            
            # Remove permission
            admin_role.remove_permission("manage_system")
            print(f"   Removed 'manage_system' permission from admin role")
            print(f"   Final permissions: {admin_role.get_permissions_list()}")
            
            await db.commit()
            
            print("\n✅ All tests completed successfully!")
            print("\n📊 Role Management System Summary:")
            roles_count = await db.execute(select(func.count(Role.id)))
            users_count = await db.execute(select(func.count(User.id)))
            assignments_count = await db.execute(select(func.count(UserRole.id)))
            
            print(f"   - Created {roles_count.scalar()} roles")
            print(f"   - Created {users_count.scalar()} users")
            print(f"   - Created {assignments_count.scalar()} role assignments")
            
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_role_system())

#!/usr/bin/env python3
"""
Database Reset Script

This script resets the database by dropping all tables and running migrations.
Use this when you encounter table conflicts or need a fresh start.

Usage:
    python reset_database.py
"""

import asyncio
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

from app.db.database import get_async_session_local, init_db, close_db
from sqlalchemy import text


async def reset_database():
    """Reset the database by dropping all tables and recreating them."""
    print("🔄 Resetting Database")
    print("=" * 50)
    
    try:
        # Connect to database
        async with get_async_session_local()() as db:
            print("📊 Connected to database")
            
            # Drop all tables in correct order (reverse of creation)
            print("🗑️  Dropping existing tables...")
            
            # Drop foreign key dependent tables first
            await db.execute(text("DROP TABLE IF EXISTS scores CASCADE"))
            print("   ✅ Dropped scores table")
            
            await db.execute(text("DROP TABLE IF EXISTS resumes CASCADE"))
            print("   ✅ Dropped resumes table")
            
            await db.execute(text("DROP TABLE IF EXISTS user_roles CASCADE"))
            print("   ✅ Dropped user_roles table")
            
            await db.execute(text("DROP TABLE IF EXISTS roles CASCADE"))
            print("   ✅ Dropped roles table")
            
            await db.execute(text("DROP TABLE IF EXISTS users CASCADE"))
            print("   ✅ Dropped users table")
            
            # Drop any remaining tables
            await db.execute(text("DROP TABLE IF EXISTS alembic_version CASCADE"))
            print("   ✅ Dropped alembic_version table")
            
            await db.commit()
            print("✅ All tables dropped successfully")
            
            # Recreate database
            print("\n🏗️  Recreating database...")
            await init_db()
            print("✅ Database recreated successfully")
            
    except Exception as e:
        print(f"❌ Error resetting database: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Clean up database connections
        try:
            await close_db()
            print("\n🧹 Database connections closed")
        except Exception as e:
            print(f"⚠️  Warning: Error closing database connections: {e}")
    
    print("\n🎉 Database reset completed successfully!")
    return True


async def main():
    """Main function."""
    print("🚀 AI Job Readiness - Database Reset")
    print("=" * 60)
    print()
    
    # Confirm action
    response = input("⚠️  This will delete ALL data in the database. Continue? (y/N): ")
    if response.lower() != 'y':
        print("❌ Operation cancelled")
        return
    
    success = await reset_database()
    
    if success:
        print("\n✅ Database reset completed successfully!")
        print("🚀 You can now run: docker compose up backend")
    else:
        print("\n❌ Database reset failed!")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

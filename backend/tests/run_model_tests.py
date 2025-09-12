#!/usr/bin/env python3
"""
Comprehensive test runner for model creation and relationships.

This script runs all unit tests for model creation, relationships, and constraints
to verify the integrity and functionality of the database schema.

Author: AI Job Readiness Team
Version: 1.0.0
"""

import asyncio
import sys
import subprocess
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from app.db.database import init_db, close_db


async def run_model_tests():
    """Run all model-related unit tests."""
    print("🚀 Starting Model Creation and Relationships Test Suite\n")
    
    try:
        # Initialize database
        print("📊 Initializing database...")
        await init_db()
        print("✅ Database initialized successfully\n")
        
        # Run pytest for model creation tests
        print("🧪 Running Model Creation Tests...")
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/unit/test_model_creation.py", 
            "-v", "--tb=short"
        ], cwd=backend_dir, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Model Creation Tests: PASSED")
        else:
            print("❌ Model Creation Tests: FAILED")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
        
        print()
        
        # Run pytest for model relationships tests
        print("🧪 Running Model Relationships Tests...")
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/unit/test_model_relationships.py", 
            "-v", "--tb=short"
        ], cwd=backend_dir, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Model Relationships Tests: PASSED")
        else:
            print("❌ Model Relationships Tests: FAILED")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
        
        print()
        
        # Run pytest for model constraints tests
        print("🧪 Running Model Constraints Tests...")
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/unit/test_model_constraints.py", 
            "-v", "--tb=short"
        ], cwd=backend_dir, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Model Constraints Tests: PASSED")
        else:
            print("❌ Model Constraints Tests: FAILED")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
        
        print()
        
        # Run all model tests together
        print("🧪 Running All Model Tests Together...")
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/unit/test_model_*.py", 
            "-v", "--tb=short", "--durations=10"
        ], cwd=backend_dir, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ All Model Tests: PASSED")
            print("\n🎉 All tests completed successfully!")
        else:
            print("❌ Some Model Tests: FAILED")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test execution failed with error: {e}")
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


async def run_specific_test(test_file: str):
    """Run a specific test file."""
    print(f"🚀 Running specific test: {test_file}\n")
    
    try:
        # Initialize database
        print("📊 Initializing database...")
        await init_db()
        print("✅ Database initialized successfully\n")
        
        # Run specific test
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            f"tests/unit/{test_file}", 
            "-v", "--tb=short"
        ], cwd=backend_dir, capture_output=True, text=True)
        
        print("STDOUT:", result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        if result.returncode == 0:
            print("✅ Test completed successfully!")
            return True
        else:
            print("❌ Test failed!")
            return False
        
    except Exception as e:
        print(f"\n❌ Test execution failed with error: {e}")
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


def main():
    """Main function to run tests."""
    if len(sys.argv) > 1:
        # Run specific test file
        test_file = sys.argv[1]
        success = asyncio.run(run_specific_test(test_file))
    else:
        # Run all tests
        success = asyncio.run(run_model_tests())
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

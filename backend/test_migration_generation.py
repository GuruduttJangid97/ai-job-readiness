#!/usr/bin/env python3
"""
Test script to verify that SQLAlchemy models can generate proper SQL DDL statements.
This tests the migration generation capability without needing a database connection.
"""

import sys
import os

# Add the app directory to the Python path
sys.path.append(os.path.dirname(__file__))

def test_model_sql_generation():
    """Test that models can generate SQL DDL statements"""
    try:
        from app.models import User, Role, UserRole, Resume, Score
        from app.db.database import Base
        from sqlalchemy import create_engine
        
        print("✅ Models imported successfully")
        
        # Create a dummy engine for SQL generation
        engine = create_engine("sqlite:///:memory:")
        
        # Generate SQL for all tables
        sql_statements = []
        for table in Base.metadata.sorted_tables:
            create_sql = str(table.compile(engine))
            sql_statements.append(create_sql)
            print(f"✅ Generated SQL for table '{table.name}':")
            print(f"   {create_sql[:100]}...")
        
        # Verify we have SQL for all expected tables
        expected_tables = {'users', 'roles', 'user_roles', 'resumes', 'scores'}
        generated_tables = {table.name for table in Base.metadata.sorted_tables}
        
        print(f"\n📊 Table Generation Summary:")
        print(f"   Expected tables: {expected_tables}")
        print(f"   Generated tables: {generated_tables}")
        
        if expected_tables.issubset(generated_tables):
            print("✅ All expected tables have SQL generated")
            return True
        else:
            missing = expected_tables - generated_tables
            print(f"❌ Missing tables: {missing}")
            return False
            
    except Exception as e:
        print(f"❌ Error generating SQL: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_model_metadata():
    """Test that models have proper metadata"""
    try:
        from app.models import User, Role, UserRole, Resume, Score
        from app.db.database import Base
        
        print("\n🔍 Testing Model Metadata...")
        
        # Check table names
        assert User.__tablename__ == "users", f"User table name should be 'users', got {User.__tablename__}"
        assert Role.__tablename__ == "roles", f"Role table name should be 'roles', got {Role.__tablename__}"
        assert UserRole.__tablename__ == "user_roles", f"UserRole table name should be 'user_roles', got {UserRole.__tablename__}"
        assert Resume.__tablename__ == "resumes", f"Resume table name should be 'resumes', got {Resume.__tablename__}"
        assert Score.__tablename__ == "scores", f"Score table name should be 'scores', got {Score.__tablename__}"
        
        print("✅ All table names are correct")
        
        # Check that models are registered with Base metadata
        metadata_tables = set(Base.metadata.tables.keys())
        expected_tables = {'users', 'roles', 'user_roles', 'resumes', 'scores'}
        
        print(f"   Metadata tables: {metadata_tables}")
        print(f"   Expected tables: {expected_tables}")
        
        if expected_tables.issubset(metadata_tables):
            print("✅ All models are registered with Base metadata")
            return True
        else:
            missing = expected_tables - metadata_tables
            print(f"❌ Missing from metadata: {missing}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing metadata: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🧪 Testing SQLAlchemy Model SQL Generation...")
    print("=" * 60)
    
    # Test 1: SQL generation
    print("\n1. Testing SQL generation...")
    sql_success = test_model_sql_generation()
    
    # Test 2: Model metadata
    print("\n2. Testing model metadata...")
    metadata_success = test_model_metadata()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary:")
    print(f"   SQL Generation: {'✅ PASS' if sql_success else '❌ FAIL'}")
    print(f"   Model Metadata: {'✅ PASS' if metadata_success else '❌ FAIL'}")
    
    if all([sql_success, metadata_success]):
        print("\n🎉 All migration tests passed! Models are ready for database creation.")
        return 0
    else:
        print("\n💥 Some migration tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

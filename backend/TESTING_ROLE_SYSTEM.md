# Role System Testing Guide

This guide provides comprehensive instructions for testing the Role model and many-to-many relationship with the User model in the AI Job Readiness platform.

## 📋 Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Testing Methods](#testing-methods)
- [Test Data](#test-data)
- [API Testing](#api-testing)
- [Database Testing](#database-testing)
- [Troubleshooting](#troubleshooting)
- [Advanced Testing](#advanced-testing)

## 🎯 Overview

The Role system implements a comprehensive role-based access control (RBAC) system with:

- **Role Model**: Defines roles with permissions and metadata
- **User Model**: Extended with role relationships
- **UserRole Model**: Many-to-many association table
- **API Endpoints**: Full CRUD operations for roles and assignments
- **Permission Management**: JSON-based permission system
- **Audit Trails**: Created/updated timestamps and assignment tracking

## 🔧 Prerequisites

Before testing, ensure you have:

1. **Python 3.8+** installed
2. **PostgreSQL** database running
3. **Dependencies** installed:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
4. **Database** initialized:
   ```bash
   cd backend
   alembic upgrade head
   ```

## 🚀 Quick Start

### 1. Start the Server

```bash
cd backend
python -m uvicorn app.main:app --reload
```

The server will start at `http://localhost:8000`

### 2. Seed Test Data

```bash
cd backend
python seed_test_data.py
```

This creates test users, roles, and assignments.

### 3. Run Tests

```bash
# Python comprehensive tests
python test_role_system.py

# API endpoint tests
./test_api.sh

# Check server status
./test_api.sh --server
```

## 🧪 Testing Methods

### Method 1: Python Comprehensive Tests

The `test_role_system.py` script provides comprehensive testing of the Role and User models.

**Features:**
- ✅ Role CRUD operations
- ✅ User-Role assignments
- ✅ Permission management
- ✅ Complex queries and relationships
- ✅ Error handling and edge cases
- ✅ Serialization testing

**Run:**
```bash
cd backend
python test_role_system.py
```

**Expected Output:**
```
🚀 Starting Role System Tests
==================================================
🔧 Setting up test environment...
✅ Test environment ready
👥 Creating test users...
✅ Created 4 test users
🎭 Creating test roles...
✅ Created 5 test roles

🧪 Testing Role CRUD operations...
  📝 Testing role creation...
    ✅ Role creation successful
  📖 Testing role reading...
    ✅ Role reading successful
  ✏️ Testing role update...
    ✅ Role update successful
  🗑️ Testing role deletion...
    ✅ Role deletion successful

🔗 Testing User-Role assignments...
  📋 Testing role assignments...
    ✅ Role assignments created successfully
  🔍 Testing role assignment verification...
    ✅ Role assignment verification successful

🔐 Testing permission management...
  🔍 Testing permission checking...
    ✅ Permission checking successful
  ➕ Testing permission addition...
    ✅ Permission addition successful
  ➖ Testing permission removal...
    ✅ Permission removal successful

🔍 Testing role queries and relationships...
  📊 Testing role statistics...
    ✅ Role statistics query successful
  👥 Testing user-role relationships...
    ✅ User-role relationships query successful

⚠️ Testing error handling and edge cases...
  🔄 Testing duplicate role name handling...
    ✅ Duplicate role name properly handled
  🚫 Testing inactive role assignment...
    ✅ Inactive role handling verified

📄 Testing serialization...
  🎭 Testing role serialization...
    ✅ Role serialization successful
  👤 Testing user serialization with roles...
    ✅ User serialization successful

==================================================
🎉 All tests passed successfully!
✅ Role model and User-Role relationship working correctly
```

### Method 2: API Endpoint Testing

The `test_api.sh` script tests the REST API endpoints.

**Features:**
- ✅ Server health checks
- ✅ Role CRUD operations via API
- ✅ Role listing and filtering
- ✅ Role statistics
- ✅ User role queries

**Run:**
```bash
cd backend
./test_api.sh
```

**Options:**
```bash
./test_api.sh --help          # Show help
./test_api.sh --server        # Check server status only
./test_api.sh --roles         # Test role operations only
./test_api.sh --users         # Test user operations only
```

### Method 3: Interactive API Testing

Use the built-in API documentation:

1. **Swagger UI**: `http://localhost:8000/docs`
2. **ReDoc**: `http://localhost:8000/redoc`

## 📊 Test Data

The seeding script creates comprehensive test data:

### Users (11 total)
- **superadmin@test.com** - Super Admin (SuperUser)
- **admin@test.com** - Admin User
- **moderator@test.com** - Moderator User
- **john.doe@test.com** - Regular User
- **jane.smith@test.com** - Regular User
- **bob.wilson@test.com** - Regular User
- **alice.brown@test.com** - Regular User
- **guest@test.com** - Guest User
- **hr.manager@test.com** - HR Manager
- **analyst@test.com** - Data Analyst
- **inactive@test.com** - Inactive User

### Roles (8 total)
- **super_admin** - Full system access
- **admin** - Management privileges
- **moderator** - Content moderation
- **user** - Basic user access
- **guest** - Limited access
- **hr_manager** - Recruitment access
- **analyst** - Data analysis access
- **inactive_role** - Inactive role

### Role Assignments
- Super Admin → super_admin
- Admin → admin
- Moderator → moderator
- Regular Users → user
- Guest → guest
- HR Manager → hr_manager
- Analyst → analyst
- Some users have multiple roles

## 🌐 API Testing

### Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/roles/` | List all roles |
| POST | `/api/v1/roles/` | Create a new role |
| GET | `/api/v1/roles/{id}` | Get role by ID |
| PUT | `/api/v1/roles/{id}` | Update role |
| DELETE | `/api/v1/roles/{id}` | Delete role |
| POST | `/api/v1/roles/assign` | Assign role to user |
| DELETE | `/api/v1/roles/assign/{id}` | Remove role assignment |
| GET | `/api/v1/roles/user/{user_id}/roles` | Get user's roles |
| GET | `/api/v1/roles/stats` | Get role statistics |

### Example API Calls

**Create a Role:**
```bash
curl -X POST "http://localhost:8000/api/v1/roles/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "test_role",
    "description": "Test role for API testing",
    "permissions": ["test:read", "test:write"],
    "is_active": true
  }'
```

**List Roles:**
```bash
curl -X GET "http://localhost:8000/api/v1/roles/"
```

**Assign Role to User:**
```bash
curl -X POST "http://localhost:8000/api/v1/roles/assign" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user-uuid-here",
    "role_id": 1
  }'
```

## 🗄️ Database Testing

### Direct Database Queries

You can test the models directly using Python:

```python
import asyncio
from app.db.database import get_async_session_local
from app.models.role import Role, UserRole
from app.models.user import User
from sqlalchemy import select

async def test_database():
    async with get_async_session_local()() as session:
        # Get all roles
        result = await session.execute(select(Role))
        roles = result.scalars().all()
        print(f"Found {len(roles)} roles")
        
        # Get users with their roles
        result = await session.execute(
            select(User).options(selectinload(User.roles).selectinload(UserRole.role))
        )
        users = result.scalars().all()
        
        for user in users:
            print(f"{user.email}: {[ur.role.name for ur in user.roles]}")

asyncio.run(test_database())
```

### Database Schema Verification

Check the database schema:

```sql
-- Check tables exist
\dt

-- Check role table structure
\d roles

-- Check user_roles table structure
\d user_roles

-- Check users table structure
\d users

-- Check indexes
\di
```

## 🔍 Troubleshooting

### Common Issues

**1. Server won't start**
```bash
# Check if port 8000 is in use
lsof -i :8000

# Kill process if needed
kill -9 <PID>

# Start server
python -m uvicorn app.main:app --reload
```

**2. Database connection issues**
```bash
# Check database status
python -c "from app.db.database import check_db_connection; import asyncio; print(asyncio.run(check_db_connection()))"

# Run migrations
alembic upgrade head
```

**3. Import errors**
```bash
# Ensure you're in the backend directory
cd backend

# Check Python path
python -c "import sys; print(sys.path)"

# Install dependencies
pip install -r requirements.txt
```

**4. Permission errors on scripts**
```bash
# Make scripts executable
chmod +x test_api.sh
chmod +x seed_test_data.py
chmod +x test_role_system.py
```

### Debug Mode

Enable debug logging:

```bash
# Set environment variable
export SQL_ECHO=true

# Start server with debug
python -m uvicorn app.main:app --reload --log-level debug
```

## 🚀 Advanced Testing

### Custom Test Scenarios

Create custom test scenarios:

```python
# test_custom_scenarios.py
import asyncio
from app.db.database import get_async_session_local
from app.models.role import Role, UserRole
from app.models.user import User

async def test_custom_scenario():
    async with get_async_session_local()() as session:
        # Your custom test logic here
        pass

asyncio.run(test_custom_scenario())
```

### Performance Testing

Test with large datasets:

```python
# test_performance.py
import asyncio
import time
from app.db.database import get_async_session_local
from app.models.role import Role, UserRole
from app.models.user import User
from sqlalchemy import select

async def test_performance():
    async with get_async_session_local()() as session:
        start_time = time.time()
        
        # Test query performance
        result = await session.execute(
            select(User)
            .options(selectinload(User.roles).selectinload(UserRole.role))
        )
        users = result.scalars().all()
        
        end_time = time.time()
        print(f"Query took {end_time - start_time:.2f} seconds")
        print(f"Retrieved {len(users)} users with roles")

asyncio.run(test_performance())
```

### Load Testing

Use tools like `wrk` or `ab` for load testing:

```bash
# Install wrk (macOS)
brew install wrk

# Load test role listing endpoint
wrk -t12 -c400 -d30s http://localhost:8000/api/v1/roles/
```

## 📈 Monitoring

### Health Checks

Monitor system health:

```bash
# API health
curl http://localhost:8000/health

# Database health
curl http://localhost:8000/database

# Model status
curl http://localhost:8000/models
```

### Logs

Monitor application logs:

```bash
# View logs in real-time
tail -f logs/app.log

# Filter error logs
grep "ERROR" logs/app.log
```

## 🎯 Success Criteria

Your Role system is working correctly if:

- ✅ All Python tests pass
- ✅ API endpoints respond correctly
- ✅ Database relationships work
- ✅ Permission system functions
- ✅ Role assignments persist
- ✅ Serialization works
- ✅ Error handling is robust

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)

## 🤝 Contributing

To add new tests:

1. Create test functions in `test_role_system.py`
2. Add API test cases in `test_api.sh`
3. Update this documentation
4. Test your changes thoroughly

---

**Happy Testing! 🎉**

For questions or issues, please check the troubleshooting section or create an issue in the project repository.

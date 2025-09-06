# Role Management System Implementation

## Overview

This document describes the implementation of a comprehensive Role-Based Access Control (RBAC) system for the AI Job Readiness Platform. The system allows users to be assigned multiple roles with specific permissions, enabling efficient permission management and access control.

## Features Implemented

### 1. Database Models

#### Role Model (`app/models/role.py`)
- **Purpose**: Defines roles with permissions and metadata
- **Key Features**:
  - Unique role names (e.g., 'admin', 'user', 'moderator')
  - JSON-based permission storage
  - Active/inactive status management
  - Audit trails with created/updated timestamps
  - Permission management methods (add, remove, check)

#### UserRole Model (`app/models/role.py`)
- **Purpose**: Association table for many-to-many relationship between users and roles
- **Key Features**:
  - Tracks role assignments with metadata
  - Records who assigned the role and when
  - Active/inactive status for role assignments
  - Cascade deletion when users or roles are deleted

#### User Model Updates (`app/models/user.py`)
- **Purpose**: Extended user model with role relationships
- **Key Features**:
  - Many-to-many relationship with roles via UserRole
  - Helper methods for role checking (`has_role`, `is_admin`, `get_role_names`)
  - Role-aware user properties

### 2. Database Schema

#### Tables Created
1. **roles** - Stores role definitions
2. **user_roles** - Association table for user-role assignments

#### Key Fields
- **roles**: id, name, description, permissions (JSON), is_active, created_at, updated_at
- **user_roles**: id, user_id, role_id, assigned_at, assigned_by, is_active

#### Indexes
- Performance-optimized indexes on frequently queried fields
- Unique constraints on role names
- Foreign key constraints with cascade deletion

### 3. API Endpoints

#### Role Management (`app/api/roles.py`)
- `POST /api/v1/roles/` - Create new role
- `GET /api/v1/roles/` - List roles with pagination and filtering
- `GET /api/v1/roles/{role_id}` - Get specific role
- `PUT /api/v1/roles/{role_id}` - Update role
- `DELETE /api/v1/roles/{role_id}` - Delete role

#### Role Assignment
- `POST /api/v1/roles/assign` - Assign role to user
- `DELETE /api/v1/roles/assign/{assignment_id}` - Remove role assignment
- `GET /api/v1/roles/user/{user_id}/roles` - Get user's roles

#### Statistics and Reporting
- `GET /api/v1/roles/stats` - Get role usage statistics

### 4. Pydantic Schemas

#### Role Schemas (`app/schemas/role.py`)
- **RoleCreate**: For creating new roles
- **RoleUpdate**: For updating existing roles
- **RoleRead**: For reading role data
- **UserRoleAssignment**: For role assignment operations
- **RoleStats**: For role statistics and reporting

#### User Schema Updates (`app/schemas/user.py`)
- Extended UserProfile to include role information
- Added role_assignments field for detailed role data

### 5. Database Migrations

#### Migration Files
1. `f6f4914742e2_initial_migration_create_all_tables.py` - Initial table creation
2. `4f2bed31f0e2_add_is_active_column_to_user_roles.py` - Added missing is_active column

#### Migration Commands
```bash
# Generate new migration
alembic revision -m "description"

# Apply migrations
alembic upgrade head

# Check current migration status
alembic current
```

## Usage Examples

### 1. Creating Roles

```python
# Create admin role
admin_role = Role(
    name="admin",
    description="Administrator role with full access",
    is_active=True
)
admin_role.set_permissions_list([
    "read", "write", "delete", "manage_users", "manage_roles"
])

# Create user role
user_role = Role(
    name="user",
    description="Regular user role with basic access",
    is_active=True
)
user_role.set_permissions_list(["read", "write"])
```

### 2. Assigning Roles to Users

```python
# Assign admin role to user
assignment = UserRole(
    user_id=user.id,
    role_id=admin_role.id,
    assigned_by=current_user.id,
    is_active=True
)
```

### 3. Checking User Permissions

```python
# Check if user has specific role
if user.has_role("admin"):
    # User has admin role

# Check if user is admin (includes superuser check)
if user.is_admin():
    # User is admin or superuser

# Get all user roles
roles = user.get_role_names()  # ['admin', 'moderator']
```

### 4. Permission Management

```python
# Add permission to role
role.add_permission("manage_system")

# Remove permission from role
role.remove_permission("manage_system")

# Check if role has permission
if role.has_permission("delete"):
    # Role has delete permission
```

## API Usage Examples

### 1. Create Role
```bash
curl -X POST "http://localhost:8000/api/v1/roles/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "moderator",
    "description": "Content moderator role",
    "permissions": ["read", "write", "moderate_content"],
    "is_active": true
  }'
```

### 2. Assign Role to User
```bash
curl -X POST "http://localhost:8000/api/v1/roles/assign" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user-uuid-here",
    "role_id": 1,
    "assigned_by": "admin-uuid-here"
  }'
```

### 3. Get User Roles
```bash
curl -X GET "http://localhost:8000/api/v1/roles/user/{user_id}/roles"
```

## Testing

### Test Script
A comprehensive test script (`test_roles_simple.py`) is provided that demonstrates:
- Role creation and management
- User creation and role assignment
- Permission checking and management
- Database relationship queries
- Complete system functionality

### Running Tests
```bash
cd backend
python test_roles_simple.py
```

## Security Considerations

### 1. Permission-Based Access Control
- All API endpoints check for appropriate permissions
- Role assignment requires admin privileges
- Role deletion prevents if users are assigned

### 2. Data Validation
- Role names are validated and normalized
- Permission lists are validated
- Foreign key constraints ensure data integrity

### 3. Audit Trails
- All role assignments are tracked with timestamps
- Assignment history includes who assigned the role
- Soft deletion for role assignments (is_active flag)

## Performance Optimizations

### 1. Database Indexes
- Indexed on frequently queried fields
- Optimized for role lookups and user queries
- Efficient pagination support

### 2. Query Optimization
- Eager loading for role relationships
- Efficient permission checking
- Minimal database queries for common operations

## Future Enhancements

### 1. Role Hierarchies
- Parent-child role relationships
- Inherited permissions
- Role hierarchy validation

### 2. Time-Based Permissions
- Role expiration dates
- Temporary role assignments
- Scheduled role changes

### 3. Advanced Permission System
- Resource-specific permissions
- Context-aware permissions
- Dynamic permission evaluation

### 4. Audit and Logging
- Comprehensive audit logs
- Permission change tracking
- Security event monitoring

## Conclusion

The Role Management System provides a robust, scalable foundation for access control in the AI Job Readiness Platform. It supports flexible role assignment, efficient permission management, and comprehensive API access while maintaining security and performance standards.

The implementation follows best practices for database design, API development, and security, making it suitable for production use and future enhancements.

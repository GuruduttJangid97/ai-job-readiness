# Relationships and Foreign Keys Summary

## Overview

This document provides a comprehensive overview of the relationships and foreign keys defined among the User, Role, Resume, and Score models in the AI Job Readiness platform. The database schema has been designed with proper data integrity, referential integrity, and query performance in mind.

## Database Schema Analysis

### Current Database: SQLite
- **Database File**: `ai_job_readiness.db`
- **Tables**: 5 tables with proper relationships
- **Foreign Keys**: 6 foreign key relationships
- **Indexes**: 24 indexes for optimal query performance

## Table Relationships

### 1. Users Table
**Primary Key**: `id` (UUID)
**Foreign Keys**: None (root table)

**Relationships**:
- **One-to-Many** with `resumes` via `resumes.user_id`
- **One-to-Many** with `scores` via `scores.user_id`
- **Many-to-Many** with `roles` via `user_roles` association table

### 2. Roles Table
**Primary Key**: `id` (INTEGER)
**Foreign Keys**: None

**Relationships**:
- **One-to-Many** with `user_roles` via `user_roles.role_id`
- **Many-to-Many** with `users` via `user_roles` association table

### 3. UserRoles Table (Association Table)
**Primary Key**: `id` (INTEGER)
**Foreign Keys**:
- `user_id` → `users.id` (CASCADE DELETE)
- `role_id` → `roles.id` (CASCADE DELETE)
- `assigned_by` → `users.id` (NULLABLE)

**Relationships**:
- **Many-to-One** with `users` via `user_id`
- **Many-to-One** with `roles` via `role_id`
- **Many-to-One** with `users` via `assigned_by` (who assigned the role)

### 4. Resumes Table
**Primary Key**: `id` (INTEGER)
**Foreign Keys**:
- `user_id` → `users.id` (CASCADE DELETE)

**Relationships**:
- **Many-to-One** with `users` via `user_id`
- **One-to-Many** with `scores` via `scores.resume_id`

### 5. Scores Table
**Primary Key**: `id` (INTEGER)
**Foreign Keys**:
- `user_id` → `users.id` (CASCADE DELETE)
- `resume_id` → `resumes.id` (CASCADE DELETE)

**Relationships**:
- **Many-to-One** with `users` via `user_id`
- **Many-to-One** with `resumes` via `resume_id`

## Foreign Key Constraints

### 1. User-Role Relationship
```sql
-- user_roles.user_id → users.id
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE

-- user_roles.role_id → roles.id  
FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE

-- user_roles.assigned_by → users.id
FOREIGN KEY (assigned_by) REFERENCES users(id)
```

### 2. User-Resume Relationship
```sql
-- resumes.user_id → users.id
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
```

### 3. User-Score Relationship
```sql
-- scores.user_id → users.id
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
```

### 4. Resume-Score Relationship
```sql
-- scores.resume_id → resumes.id
FOREIGN KEY (resume_id) REFERENCES resumes(id) ON DELETE CASCADE
```

## Indexes for Query Performance

### Primary Key Indexes
- `users.id` (PRIMARY KEY)
- `roles.id` (PRIMARY KEY)
- `user_roles.id` (PRIMARY KEY)
- `resumes.id` (PRIMARY KEY)
- `scores.id` (PRIMARY KEY)

### Foreign Key Indexes
- `ix_user_roles_user_id` on `user_roles.user_id`
- `ix_user_roles_role_id` on `user_roles.role_id`
- `ix_resumes_user_id` on `resumes.user_id`
- `ix_scores_user_id` on `scores.user_id`
- `ix_scores_resume_id` on `scores.resume_id`

### Business Logic Indexes
- `ix_users_email` (UNIQUE) on `users.email`
- `ix_roles_name` (UNIQUE) on `roles.name`
- `ix_users_is_active` on `users.is_active`
- `ix_roles_is_active` on `roles.is_active`
- `ix_user_roles_is_active` on `user_roles.is_active`
- `ix_resumes_is_active` on `resumes.is_active`
- `ix_scores_is_active` on `scores.is_active`

### Timestamp Indexes
- `ix_users_created_at` on `users.created_at`
- `ix_roles_created_at` on `roles.created_at`
- `ix_user_roles_assigned_at` on `user_roles.assigned_at`
- `ix_resumes_created_at` on `resumes.created_at`
- `ix_scores_analysis_date` on `scores.analysis_date`

### Specialized Indexes
- `ix_resumes_file_type` on `resumes.file_type`
- `ix_scores_analysis_type` on `scores.analysis_type`
- `ix_scores_overall_score` on `scores.overall_score`

## Data Integrity Features

### 1. Cascade Deletes
- When a user is deleted, all their resumes and scores are automatically deleted
- When a role is deleted, all user-role assignments are automatically deleted
- When a resume is deleted, all associated scores are automatically deleted

### 2. Referential Integrity
- All foreign key relationships are enforced at the database level
- Attempts to insert invalid foreign key values will be rejected
- Orphaned records cannot exist due to foreign key constraints

### 3. Unique Constraints
- User emails must be unique
- Role names must be unique
- Primary keys are automatically unique

## Query Patterns Supported

### 1. User Queries
```sql
-- Get user with all their roles
SELECT u.*, r.name as role_name 
FROM users u 
LEFT JOIN user_roles ur ON u.id = ur.user_id 
LEFT JOIN roles r ON ur.role_id = r.id 
WHERE u.id = ?

-- Get user with all their resumes
SELECT * FROM resumes WHERE user_id = ? AND is_active = 1

-- Get user with all their scores
SELECT * FROM scores WHERE user_id = ? AND is_active = 1
```

### 2. Resume Queries
```sql
-- Get resume with all its scores
SELECT r.*, s.* 
FROM resumes r 
LEFT JOIN scores s ON r.id = s.resume_id 
WHERE r.id = ?

-- Get user's most recent resume
SELECT * FROM resumes 
WHERE user_id = ? AND is_active = 1 
ORDER BY created_at DESC LIMIT 1
```

### 3. Score Queries
```sql
-- Get scores for a specific analysis type
SELECT * FROM scores 
WHERE user_id = ? AND analysis_type = ? AND is_active = 1

-- Get scores for a specific resume
SELECT * FROM scores 
WHERE resume_id = ? AND is_active = 1
```

### 4. Role Queries
```sql
-- Get all users with a specific role
SELECT u.*, ur.assigned_at 
FROM users u 
JOIN user_roles ur ON u.id = ur.user_id 
JOIN roles r ON ur.role_id = r.id 
WHERE r.name = ? AND ur.is_active = 1
```

## Model Relationships in SQLAlchemy

### User Model Relationships
```python
# One-to-Many with resumes
resumes: Mapped[List["Resume"]] = relationship(
    "Resume", 
    back_populates="user", 
    cascade="all, delete-orphan"
)

# One-to-Many with scores
scores: Mapped[List["Score"]] = relationship(
    "Score", 
    back_populates="user", 
    cascade="all, delete-orphan"
)

# Many-to-Many with roles via UserRole
roles: Mapped[List["UserRole"]] = relationship(
    "UserRole", 
    back_populates="user", 
    cascade="all, delete-orphan",
    foreign_keys="UserRole.user_id"
)
```

### Resume Model Relationships
```python
# Many-to-One with user
user: Mapped["User"] = relationship(
    "User", 
    back_populates="resumes"
)

# One-to-Many with scores
scores: Mapped[List["Score"]] = relationship(
    "Score", 
    back_populates="resume", 
    cascade="all, delete-orphan"
)
```

### Score Model Relationships
```python
# Many-to-One with user
user: Mapped["User"] = relationship(
    "User", 
    back_populates="scores"
)

# Many-to-One with resume
resume: Mapped["Resume"] = relationship(
    "Resume", 
    back_populates="scores"
)
```

### Role Model Relationships
```python
# One-to-Many with user_roles
user_roles: Mapped[List["UserRole"]] = relationship(
    "UserRole", 
    back_populates="role", 
    cascade="all, delete-orphan"
)
```

## Performance Optimizations

### 1. Index Strategy
- All foreign keys are indexed for fast joins
- Frequently queried fields have dedicated indexes
- Composite indexes support common query patterns
- Unique indexes prevent duplicate data

### 2. Query Optimization
- Relationships use proper foreign key constraints
- Cascade deletes maintain data consistency
- Indexes support efficient filtering and sorting
- Lazy loading prevents unnecessary data fetching

### 3. Data Integrity
- Foreign key constraints prevent orphaned records
- Unique constraints prevent duplicate data
- Cascade deletes maintain referential integrity
- Proper data types ensure data consistency

## Migration History

### Initial Migration (f6f4914742e2)
- Created all core tables with basic relationships
- Established foreign key constraints
- Added primary indexes

### User Roles Enhancement (4f2bed31f0e2)
- Added `is_active` column to `user_roles` table
- Enhanced role assignment tracking

### Relationship Enhancement (7f91e9655315)
- Attempted to add additional constraints (SQLite limitations)
- Added comprehensive indexing strategy

### SQLite-Compatible Constraints (0e9150a01e7e)
- Added composite indexes for query performance
- Enhanced indexing for common query patterns
- Optimized for SQLite database engine

## Conclusion

The database schema for the AI Job Readiness platform has been designed with comprehensive relationships and foreign keys that ensure:

1. **Data Integrity**: Foreign key constraints prevent orphaned records
2. **Referential Integrity**: All relationships are properly enforced
3. **Query Performance**: Comprehensive indexing strategy supports efficient queries
4. **Scalability**: Proper normalization and indexing support growth
5. **Maintainability**: Clear relationships make the schema easy to understand and modify

The relationships between User, Role, Resume, and Score models are well-defined and support all necessary business operations while maintaining data consistency and query performance.

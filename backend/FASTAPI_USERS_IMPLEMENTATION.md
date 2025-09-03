# FastAPI-Users Implementation Guide

## Overview

This document describes the complete FastAPI-Users implementation for the AI Job Readiness Platform. The implementation extends FastAPI-Users base functionality to provide comprehensive user authentication and management capabilities.

## Architecture

### Components

1. **User Model** (`app/models/user.py`)
   - Extends `SQLAlchemyBaseUserTable[uuid.UUID]`
   - Includes additional profile fields (first_name, last_name, phone, bio, etc.)
   - Relationships with roles, resumes, and scores
   - Audit trails with created/updated timestamps

2. **Pydantic Schemas** (`app/schemas/user.py`)
   - `UserCreate`: User registration schema
   - `UserUpdate`: User update schema
   - `UserRead`: User read schema
   - `UserProfile`: Extended profile schema
   - `UserProfileUpdate`: Profile update schema
   - Authentication and password management schemas

3. **Core Configuration** (`app/core/`)
   - `config.py`: Application settings and configuration
   - `security.py`: Password hashing and JWT token utilities
   - `users.py`: FastAPI-Users configuration and user manager

4. **API Endpoints** (`app/api/`)
   - `auth.py`: Authentication endpoints (login, register, verify, reset password)
   - `users.py`: User management endpoints (profile, CRUD operations)

## Features

### Authentication
- ✅ User registration with email validation
- ✅ JWT-based authentication
- ✅ Password strength validation
- ✅ Email verification
- ✅ Password reset functionality
- ✅ Protected routes with authentication dependencies

### User Management
- ✅ Profile management (view, update)
- ✅ Password change functionality
- ✅ User listing with pagination and filtering (admin)
- ✅ User activation/deactivation (admin)
- ✅ Role-based access control integration

### Security
- ✅ Bcrypt password hashing
- ✅ JWT token generation and validation
- ✅ Password strength requirements
- ✅ Email format validation
- ✅ Phone number validation
- ✅ Profile picture URL validation

## API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/auth/register` | User registration | No |
| POST | `/api/v1/auth/jwt/login` | User login | No |
| POST | `/api/v1/auth/jwt/logout` | User logout | Yes |
| GET | `/api/v1/auth/me` | Get current user | Yes |
| POST | `/api/v1/auth/request-password-reset` | Request password reset | No |
| POST | `/api/v1/auth/confirm-password-reset` | Confirm password reset | No |
| GET | `/api/v1/auth/verify-email` | Verify email address | No |
| POST | `/api/v1/auth/resend-verification` | Resend verification email | No |

### User Management Endpoints

| Method | Endpoint | Description | Auth Required | Admin Required |
|--------|----------|-------------|---------------|----------------|
| GET | `/api/v1/users/profile` | Get user profile | Yes | No |
| PUT | `/api/v1/users/profile` | Update user profile | Yes | No |
| POST | `/api/v1/users/change-password` | Change password | Yes | No |
| GET | `/api/v1/users/list` | List users | Yes | Yes |
| GET | `/api/v1/users/{user_id}` | Get user by ID | Yes | Yes |
| DELETE | `/api/v1/users/{user_id}` | Delete user | Yes | Yes |
| PATCH | `/api/v1/users/{user_id}/activate` | Activate user | Yes | Yes |
| PATCH | `/api/v1/users/{user_id}/deactivate` | Deactivate user | Yes | Yes |

### Protected Routes

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/v1/protected` | Example protected route | Yes |

## Usage Examples

### 1. User Registration

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "+1234567890"
  }'
```

### 2. User Login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/jwt/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=SecurePass123"
```

### 3. Get Current User Profile

```bash
curl -X GET "http://localhost:8000/api/v1/users/profile" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 4. Update User Profile

```bash
curl -X PUT "http://localhost:8000/api/v1/users/profile" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Jane",
    "last_name": "Smith",
    "bio": "Software Developer with 5 years experience"
  }'
```

### 5. Change Password

```bash
curl -X POST "http://localhost:8000/api/v1/users/change-password" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "current_password": "OldPass123",
    "new_password": "NewSecurePass456"
  }'
```

## Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# Database
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/ai_job_readiness
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=ai_job_readiness

# Security
SECRET_KEY=your-super-secret-key-change-in-production
USERS_SECRET=your-users-secret-change-in-production
VERIFICATION_TOKEN_SECRET=your-verification-secret-change-in-production
RESET_PASSWORD_TOKEN_SECRET=your-reset-password-secret-change-in-production

# JWT Settings
ACCESS_TOKEN_EXPIRE_MINUTES=30
VERIFICATION_TOKEN_EXPIRE_HOURS=24
RESET_PASSWORD_TOKEN_EXPIRE_HOURS=1

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:3001"]

# Logging
LOG_LEVEL=INFO
SQL_ECHO=false
```

## Dependencies

The following packages are required for the FastAPI-Users implementation:

```
fastapi-users[sqlalchemy]
pydantic[email]
pydantic-settings
python-jose[cryptography]
passlib[bcrypt]
email-validator
```

## Testing

### Run the Test Script

```bash
cd backend
python test_fastapi_users.py
```

### Manual Testing

1. Start the application:
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

2. Access the API documentation:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

3. Test endpoints using the interactive documentation or curl commands.

## Security Considerations

### Production Deployment

1. **Change Default Secrets**: Update all secret keys in production
2. **Use HTTPS**: Always use HTTPS in production
3. **Environment Variables**: Store sensitive data in environment variables
4. **Database Security**: Use strong database credentials and network security
5. **Rate Limiting**: Implement rate limiting for authentication endpoints
6. **Email Verification**: Configure proper email sending for verification

### Password Requirements

- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit

### Token Security

- JWT tokens expire after 30 minutes by default
- Password reset tokens expire after 1 hour
- Email verification tokens expire after 24 hours

## Integration with Existing Models

The User model integrates seamlessly with existing models:

- **Roles**: Many-to-many relationship via `UserRole` association table
- **Resumes**: One-to-many relationship for user's resumes
- **Scores**: One-to-many relationship for user's job readiness scores

## Error Handling

The implementation includes comprehensive error handling:

- Validation errors for input data
- Authentication errors for invalid credentials
- Authorization errors for insufficient permissions
- Database errors for data operations
- HTTP status codes following REST conventions

## Future Enhancements

Potential future enhancements:

1. **OAuth Integration**: Add Google, GitHub, or other OAuth providers
2. **Two-Factor Authentication**: Implement 2FA for enhanced security
3. **Session Management**: Add session tracking and management
4. **Audit Logging**: Enhanced audit trails for user actions
5. **Email Templates**: Customizable email templates for notifications
6. **Social Features**: User following, connections, and social interactions

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
2. **Database Connection**: Check database URL and credentials
3. **JWT Token Issues**: Verify secret keys are properly configured
4. **CORS Issues**: Check CORS origins configuration
5. **Email Issues**: Configure SMTP settings for email functionality

### Debug Mode

Enable debug mode by setting:
```env
DEBUG=true
SQL_ECHO=true
LOG_LEVEL=DEBUG
```

## Support

For issues or questions regarding the FastAPI-Users implementation:

1. Check the API documentation at `/docs`
2. Review the test script output
3. Check application logs for error details
4. Verify environment configuration
5. Test database connectivity

---

**Note**: This implementation provides a solid foundation for user authentication and management. Customize the schemas, endpoints, and business logic as needed for your specific requirements.

# Postman Testing Guide for AI Job Readiness API

## 🚀 Quick Start

### 1. Start the Server
```bash
cd /Users/guruduttjangid/ai-job-readiness/backend
python start_server.py
```

### 2. Import Postman Collection
1. Open Postman
2. Click "Import" button
3. Select `AI_Job_Readiness_API.postman_collection.json`
4. The collection will be imported with all endpoints ready to test

## 📋 Available Endpoints

### **Health & System Endpoints**
- **GET** `/` - Root endpoint with API info
- **GET** `/health` - Health check
- **GET** `/models` - List all database models
- **GET** `/database` - Database connection status
- **GET** `/api/v1/info` - Comprehensive API information

### **Authentication Endpoints**
- **POST** `/api/v1/auth/register` - Register new user
- **POST** `/api/v1/auth/jwt/login` - Login user
- **GET** `/api/v1/auth/me` - Get current user
- **POST** `/api/v1/auth/jwt/logout` - Logout user
- **POST** `/api/v1/auth/forgot-password` - Request password reset
- **POST** `/api/v1/auth/reset-password` - Reset password

### **User Management Endpoints**
- **GET** `/api/v1/users/profile` - Get user profile
- **PUT** `/api/v1/users/profile` - Update user profile
- **POST** `/api/v1/users/change-password` - Change password
- **GET** `/api/v1/users/` - List all users (Admin)
- **GET** `/api/v1/users/{user_id}` - Get user by ID (Admin)
- **PUT** `/api/v1/users/{user_id}` - Update user (Admin)
- **DELETE** `/api/v1/users/{user_id}` - Delete user (Admin)

### **Role Management Endpoints**
- **POST** `/api/v1/roles/` - Create role
- **GET** `/api/v1/roles/` - List all roles
- **GET** `/api/v1/roles/{role_id}` - Get role by ID
- **PUT** `/api/v1/roles/{role_id}` - Update role
- **DELETE** `/api/v1/roles/{role_id}` - Delete role
- **POST** `/api/v1/roles/assign` - Assign role to user
- **GET** `/api/v1/roles/user/{user_id}` - Get user roles
- **DELETE** `/api/v1/roles/assign/{user_id}/{role_id}` - Remove role from user
- **PUT** `/api/v1/roles/{role_id}/permissions` - Update role permissions
- **GET** `/api/v1/roles/stats` - Get role statistics

### **Resume Management Endpoints**
- **POST** `/api/v1/resumes/` - Create resume
- **POST** `/api/v1/resumes/upload` - Upload resume file
- **GET** `/api/v1/resumes/` - List user resumes
- **GET** `/api/v1/resumes/{resume_id}` - Get resume by ID
- **PUT** `/api/v1/resumes/{resume_id}` - Update resume
- **DELETE** `/api/v1/resumes/{resume_id}` - Delete resume
- **GET** `/api/v1/resumes/{resume_id}/download` - Download resume file
- **POST** `/api/v1/resumes/{resume_id}/analyze` - Request resume analysis
- **GET** `/api/v1/resumes/{resume_id}/scores` - Get analysis results

### **Protected Routes**
- **GET** `/api/v1/protected` - Example protected route

## 🔧 Testing Workflow

### **Step 1: Health Check**
1. Start with **GET** `/health` to verify server is running
2. Check **GET** `/database` to verify database connection

### **Step 2: User Registration & Authentication**
1. **POST** `/api/v1/auth/register` - Register a new user
2. **POST** `/api/v1/auth/jwt/login` - Login with credentials
3. Copy the `access_token` from login response
4. Set the token in collection variables: `{{access_token}}`

### **Step 3: User Profile Management**
1. **GET** `/api/v1/users/profile` - Get current user profile
2. **PUT** `/api/v1/users/profile` - Update profile information
3. **POST** `/api/v1/users/change-password` - Change password

### **Step 4: Role Management (Admin)**
1. **POST** `/api/v1/roles/` - Create a new role
2. **GET** `/api/v1/roles/` - List all roles
3. **POST** `/api/v1/roles/assign` - Assign role to user
4. **GET** `/api/v1/roles/user/{user_id}` - Check user roles

### **Step 5: Resume Management**
1. **POST** `/api/v1/resumes/` - Create a resume
2. **POST** `/api/v1/resumes/upload` - Upload resume file
3. **GET** `/api/v1/resumes/` - List user resumes
4. **POST** `/api/v1/resumes/{resume_id}/analyze` - Analyze resume
5. **GET** `/api/v1/resumes/{resume_id}/scores` - Get analysis results

## 📝 Sample Request Bodies

### **User Registration**
```json
{
  "email": "test@example.com",
  "password": "SecurePass123!",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "+1234567890",
  "bio": "Software Engineer with 5 years experience"
}
```

### **User Login**
```
username: test@example.com
password: SecurePass123!
```

### **Create Role**
```json
{
  "name": "moderator",
  "description": "Moderator role with limited admin privileges",
  "permissions": ["read", "write", "moderate"],
  "is_active": true
}
```

### **Create Resume**
```json
{
  "title": "Senior Software Engineer Resume",
  "summary": "Experienced software engineer with 5+ years in full-stack development",
  "experience_years": 5.5,
  "education_level": "Bachelor's Degree",
  "skills": ["Python", "JavaScript", "React", "Node.js", "PostgreSQL"],
  "languages": [
    {"name": "English", "proficiency": "Native"},
    {"name": "Spanish", "proficiency": "Intermediate"}
  ],
  "is_public": false
}
```

### **Resume Analysis Request**
```json
{
  "job_title": "Senior Software Engineer",
  "company": "Tech Corp",
  "job_description": "We are looking for a senior software engineer with experience in Python, React, and cloud technologies..."
}
```

## 🔐 Authentication Setup

### **JWT Token Authentication**
1. Login using the login endpoint
2. Copy the `access_token` from the response
3. Set it in the collection variable `{{access_token}}`
4. All protected endpoints will automatically use this token

### **Headers for Protected Routes**
```
Authorization: Bearer {{access_token}}
Content-Type: application/json
```

## 📊 Collection Variables

The collection uses these variables:
- `{{base_url}}` - API base URL (default: http://localhost:8000)
- `{{api_version}}` - API version (default: /api/v1)
- `{{access_token}}` - JWT access token (auto-populated)
- `{{user_id}}` - User ID (auto-populated)
- `{{resume_id}}` - Resume ID (auto-populated)
- `{{role_id}}` - Role ID (auto-populated)

## 🧪 Testing Scenarios

### **Scenario 1: Complete User Journey**
1. Register user → Login → Get profile → Update profile
2. Create role → Assign role → Check user roles
3. Create resume → Upload file → Analyze resume → Get scores

### **Scenario 2: Admin Operations**
1. Login as admin → List all users → Create role → Assign roles
2. Update user permissions → Get role statistics

### **Scenario 3: Resume Analysis**
1. Create resume → Upload PDF → Request analysis → Get results
2. Update resume → Re-analyze → Compare scores

## 🚨 Common Issues & Solutions

### **401 Unauthorized**
- Check if access token is set correctly
- Verify token hasn't expired
- Ensure Authorization header format: `Bearer {token}`

### **422 Validation Error**
- Check request body format
- Verify required fields are provided
- Check data types match schema

### **500 Internal Server Error**
- Check server logs
- Verify database connection
- Check if all dependencies are installed

### **File Upload Issues**
- Ensure file size is under 10MB
- Check file format (PDF, DOC, DOCX, TXT)
- Verify multipart/form-data content type

## 📈 Performance Testing

### **Load Testing with Postman**
1. Use Postman Runner to run multiple requests
2. Test concurrent user registrations
3. Test bulk resume uploads
4. Monitor response times

### **Database Performance**
- Test with large datasets
- Monitor query execution times
- Check index usage

## 🔍 Debugging Tips

1. **Enable Request/Response Logging**
   - Check server console for detailed logs
   - Use Postman Console for request details

2. **Test Individual Endpoints**
   - Start with simple GET requests
   - Gradually add complexity

3. **Verify Data Integrity**
   - Check database after operations
   - Verify relationships are maintained

4. **Error Handling**
   - Test with invalid data
   - Verify proper error responses

## 📚 Additional Resources

- **API Documentation**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc
- **Database Schema**: Check `RELATIONSHIPS_AND_FOREIGN_KEYS_SUMMARY.md`
- **Implementation Details**: Check `RELATIONSHIPS_IMPLEMENTATION_COMPLETE.md`

## 🎯 Success Criteria

✅ **All endpoints return 200/201 status codes**
✅ **Authentication works correctly**
✅ **Data is persisted in database**
✅ **Relationships are maintained**
✅ **File uploads work**
✅ **Analysis requests are processed**
✅ **Error handling is proper**

---

**Happy Testing! 🚀**

The API is now ready for comprehensive testing with Postman. All endpoints are documented and ready to use.

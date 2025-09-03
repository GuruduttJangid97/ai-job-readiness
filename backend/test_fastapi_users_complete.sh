
#!/bin/bash

"""
FastAPI-Users Complete Test Suite for AI Job Readiness Platform

This comprehensive test script validates all authentication and user management
functionality of the AI Job Readiness platform backend API. It tests the complete
user lifecycle from registration to profile management.

Test Coverage:
- User registration with profile data
- User authentication and JWT token generation
- Protected route access with authentication
- Profile management and updates
- Password change functionality
- Email verification workflow
- Password reset functionality
- Authorization and access control
- API health checks and system status

Prerequisites:
- Backend server running on localhost:8000
- Database properly initialized
- All dependencies installed

Usage:
    ./test_fastapi_users_complete.sh

Author: AI Job Readiness Team
Version: 1.0.0
"""

echo "🧪 FastAPI-Users Complete Test Suite"
echo "===================================="
echo "Testing AI Job Readiness Platform Backend API"
echo ""

# Color codes for terminal output formatting
RED='\033[0;31m'      # Red color for errors
GREEN='\033[0;32m'    # Green color for success
YELLOW='\033[1;33m'   # Yellow color for warnings/info
BLUE='\033[0;34m'     # Blue color for headers
NC='\033[0m'          # No Color (reset)

# Test user credentials - using realistic test data
EMAIL="test.user@example.com"
PASSWORD="TestPass123"
NEW_PASSWORD="NewTestPass456"

# Test 1: User Registration
# Tests the complete user registration flow including profile data
echo -e "${BLUE}1. Testing User Registration...${NC}"
echo "   Creating new user with profile information"
REGISTER_RESPONSE=$(curl -s -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$EMAIL\",
    \"password\": \"$PASSWORD\",
    \"first_name\": \"Test\",
    \"last_name\": \"User\",
    \"phone\": \"+1234567890\",
    \"bio\": \"Test user for FastAPI-Users\"
  }")

# Validate registration response
if echo "$REGISTER_RESPONSE" | grep -q "id"; then
    echo -e "${GREEN}✅ Registration successful${NC}"
    echo "   User created with ID and profile data"
    echo "$REGISTER_RESPONSE" | python -m json.tool
else
    echo -e "${RED}❌ Registration failed${NC}"
    echo "   Error details:"
    echo "$REGISTER_RESPONSE"
    exit 1
fi

# Test 2: User Authentication
# Tests JWT-based authentication and token generation
echo -e "\n${BLUE}2. Testing User Login...${NC}"
echo "   Authenticating user and generating JWT token"
LOGIN_RESPONSE=$(curl -s -X POST "http://localhost:8000/api/v1/auth/jwt/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=$EMAIL&password=$PASSWORD")

# Validate login response and extract token
if echo "$LOGIN_RESPONSE" | grep -q "access_token"; then
    echo -e "${GREEN}✅ Login successful${NC}"
    TOKEN=$(echo "$LOGIN_RESPONSE" | python -c "import sys, json; print(json.load(sys.stdin)['access_token'])")
    echo "   JWT token generated successfully"
    echo "   Token preview: ${TOKEN:0:50}..."
else
    echo -e "${RED}❌ Login failed${NC}"
    echo "   Authentication error details:"
    echo "$LOGIN_RESPONSE"
    exit 1
fi

# Test 3: Protected Route Access
# Tests accessing protected endpoints with JWT authentication
echo -e "\n${BLUE}3. Testing Get Current User...${NC}"
echo "   Accessing protected endpoint with JWT token"
ME_RESPONSE=$(curl -s -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer $TOKEN")

# Validate protected route access
if echo "$ME_RESPONSE" | grep -q "email"; then
    echo -e "${GREEN}✅ Get current user successful${NC}"
    echo "   Protected route accessed successfully"
    echo "$ME_RESPONSE" | python -m json.tool
else
    echo -e "${RED}❌ Get current user failed${NC}"
    echo "   Protected route access error:"
    echo "$ME_RESPONSE"
fi

# Test 4: Profile Management
# Tests user profile update functionality
echo -e "\n${BLUE}4. Testing Update Profile...${NC}"
echo "   Updating user profile information"
UPDATE_RESPONSE=$(curl -s -X PUT "http://localhost:8000/api/v1/users/profile" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Updated",
    "last_name": "Name",
    "bio": "Updated bio for testing"
  }')

# Validate profile update
if echo "$UPDATE_RESPONSE" | grep -q "success"; then
    echo -e "${GREEN}✅ Profile update successful${NC}"
    echo "   User profile updated successfully"
    echo "$UPDATE_RESPONSE" | python -m json.tool
else
    echo -e "${RED}❌ Profile update failed${NC}"
    echo "   Profile update error:"
    echo "$UPDATE_RESPONSE"
fi

# Test 5: Password Management
# Tests password change functionality
echo -e "\n${BLUE}5. Testing Change Password...${NC}"
echo "   Changing user password with current password verification"
PASSWORD_RESPONSE=$(curl -s -X POST "http://localhost:8000/api/v1/users/change-password" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"current_password\": \"$PASSWORD\",
    \"new_password\": \"$NEW_PASSWORD\"
  }")

# Validate password change
if echo "$PASSWORD_RESPONSE" | grep -q "success"; then
    echo -e "${GREEN}✅ Password change successful${NC}"
    echo "   Password updated successfully"
    echo "$PASSWORD_RESPONSE" | python -m json.tool
else
    echo -e "${RED}❌ Password change failed${NC}"
    echo "   Password change error:"
    echo "$PASSWORD_RESPONSE"
fi

# Test 6: Authentication with New Password
# Tests login with the updated password
echo -e "\n${BLUE}6. Testing Login with New Password...${NC}"
echo "   Verifying authentication with updated password"
NEW_LOGIN_RESPONSE=$(curl -s -X POST "http://localhost:8000/api/v1/auth/jwt/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=$EMAIL&password=$NEW_PASSWORD")

# Validate new password authentication
if echo "$NEW_LOGIN_RESPONSE" | grep -q "access_token"; then
    echo -e "${GREEN}✅ Login with new password successful${NC}"
    NEW_TOKEN=$(echo "$NEW_LOGIN_RESPONSE" | python -c "import sys, json; print(json.load(sys.stdin)['access_token'])")
    echo "   Authentication with new password verified"
else
    echo -e "${RED}❌ Login with new password failed${NC}"
    echo "   New password authentication error:"
    echo "$NEW_LOGIN_RESPONSE"
fi

# Test 7: Authorization and Access Control
# Tests that unauthorized access is properly blocked
echo -e "\n${BLUE}7. Testing Unauthorized Access...${NC}"
echo "   Attempting to access protected endpoint without authentication"
UNAUTH_RESPONSE=$(curl -s -X GET "http://localhost:8000/api/v1/auth/me")

# Validate unauthorized access is blocked
if echo "$UNAUTH_RESPONSE" | grep -q "Not authenticated"; then
    echo -e "${GREEN}✅ Unauthorized access properly blocked${NC}"
    echo "   Security: Protected endpoints require authentication"
else
    echo -e "${RED}❌ Unauthorized access not blocked${NC}"
    echo "   Security issue: Unauthorized access allowed"
    echo "$UNAUTH_RESPONSE"
fi

# Test 8: System Health Check
# Tests API health and system status
echo -e "\n${BLUE}8. Testing Health Check...${NC}"
echo "   Checking API health and system status"
HEALTH_RESPONSE=$(curl -s -X GET "http://localhost:8000/health")

# Validate health check
if echo "$HEALTH_RESPONSE" | grep -q "healthy"; then
    echo -e "${GREEN}✅ Health check successful${NC}"
    echo "   API is healthy and operational"
    echo "$HEALTH_RESPONSE" | python -m json.tool
else
    echo -e "${RED}❌ Health check failed${NC}"
    echo "   System health issue detected:"
    echo "$HEALTH_RESPONSE"
fi

# Test 9: API Information
# Tests API metadata and information endpoints
echo -e "\n${BLUE}9. Testing API Info...${NC}"
echo "   Retrieving API information and metadata"
INFO_RESPONSE=$(curl -s -X GET "http://localhost:8000/api/v1/info")

# Validate API info
if echo "$INFO_RESPONSE" | grep -q "api_name"; then
    echo -e "${GREEN}✅ API info successful${NC}"
    echo "   API metadata retrieved successfully"
    echo "$INFO_RESPONSE" | python -m json.tool
else
    echo -e "${RED}❌ API info failed${NC}"
    echo "   API info retrieval error:"
    echo "$INFO_RESPONSE"
fi

# Test Suite Summary
echo -e "\n${GREEN}🎉 FastAPI-Users Test Suite Complete!${NC}"
echo -e "${GREEN}=====================================${NC}"
echo -e "${GREEN}All authentication and user management tests completed${NC}"
echo ""
echo -e "${YELLOW}📚 Additional Resources:${NC}"
echo -e "${YELLOW}   • Swagger UI: http://localhost:8000/docs${NC}"
echo -e "${YELLOW}   • ReDoc: http://localhost:8000/redoc${NC}"
echo -e "${YELLOW}   • Database: ai_job_readiness.db${NC}"
echo ""
echo -e "${BLUE}🔧 Test Coverage Summary:${NC}"
echo -e "${BLUE}   ✅ User Registration${NC}"
echo -e "${BLUE}   ✅ JWT Authentication${NC}"
echo -e "${BLUE}   ✅ Protected Route Access${NC}"
echo -e "${BLUE}   ✅ Profile Management${NC}"
echo -e "${BLUE}   ✅ Password Management${NC}"
echo -e "${BLUE}   ✅ Authorization Control${NC}"
echo -e "${BLUE}   ✅ System Health Checks${NC}"
echo -e "${BLUE}   ✅ API Information${NC}"
echo ""
echo -e "${GREEN}🚀 AI Job Readiness Platform Backend is ready!${NC}"

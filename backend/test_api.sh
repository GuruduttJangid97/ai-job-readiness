#!/bin/bash

# API Testing Script for Role and User Models
# This script tests the Role API endpoints and User-Role relationships

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
BASE_URL="http://localhost:8000"
API_BASE="${BASE_URL}/api/v1"

# Test data
ADMIN_EMAIL="admin@test.com"
ADMIN_PASSWORD="AdminPass123!"
MODERATOR_EMAIL="moderator@test.com"
MODERATOR_PASSWORD="ModPass123!"
USER_EMAIL="user1@test.com"
USER_PASSWORD="UserPass123!"

# Global variables
ADMIN_TOKEN=""
MODERATOR_TOKEN=""
USER_TOKEN=""
ADMIN_USER_ID=""
MODERATOR_USER_ID=""
USER_ID=""
ADMIN_ROLE_ID=""
MODERATOR_ROLE_ID=""
USER_ROLE_ID=""

# Function to print colored output
print_status() {
    local status=$1
    local message=$2
    case $status in
        "INFO")
            echo -e "${BLUE}ℹ️  $message${NC}"
            ;;
        "SUCCESS")
            echo -e "${GREEN}✅ $message${NC}"
            ;;
        "ERROR")
            echo -e "${RED}❌ $message${NC}"
            ;;
        "WARNING")
            echo -e "${YELLOW}⚠️  $message${NC}"
            ;;
        "TEST")
            echo -e "${BLUE}🧪 $message${NC}"
            ;;
    esac
}

# Function to check if server is running
check_server() {
    print_status "INFO" "Checking if server is running..."
    
    if curl -s "${BASE_URL}/health" > /dev/null; then
        print_status "SUCCESS" "Server is running at ${BASE_URL}"
        return 0
    else
        print_status "ERROR" "Server is not running. Please start the server first:"
        echo "  cd backend && python -m uvicorn app.main:app --reload"
        return 1
    fi
}

# Function to make API request
api_request() {
    local method=$1
    local endpoint=$2
    local data=$3
    local token=$4
    local expected_status=$5
    
    local url="${API_BASE}${endpoint}"
    local headers="Content-Type: application/json"
    
    if [ -n "$token" ]; then
        headers="${headers}; Authorization: Bearer ${token}"
    fi
    
    local response
    local status_code
    
    if [ "$method" = "GET" ]; then
        response=$(curl -s -w "\n%{http_code}" -H "$headers" "$url")
    elif [ "$method" = "POST" ]; then
        response=$(curl -s -w "\n%{http_code}" -X POST -H "$headers" -d "$data" "$url")
    elif [ "$method" = "PUT" ]; then
        response=$(curl -s -w "\n%{http_code}" -X PUT -H "$headers" -d "$data" "$url")
    elif [ "$method" = "DELETE" ]; then
        response=$(curl -s -w "\n%{http_code}" -X DELETE -H "$headers" "$url")
    fi
    
    status_code=$(echo "$response" | tail -n1)
    response_body=$(echo "$response" | head -n -1)
    
    if [ "$status_code" = "$expected_status" ]; then
        print_status "SUCCESS" "${method} ${endpoint} - Status: ${status_code}"
        echo "$response_body" | jq . 2>/dev/null || echo "$response_body"
        return 0
    else
        print_status "ERROR" "${method} ${endpoint} - Expected: ${expected_status}, Got: ${status_code}"
        echo "$response_body" | jq . 2>/dev/null || echo "$response_body"
        return 1
    fi
}

# Function to extract value from JSON response
extract_value() {
    local json=$1
    local key=$2
    echo "$json" | jq -r ".$key" 2>/dev/null
}

# Function to create test users
create_test_users() {
    print_status "TEST" "Creating test users..."
    
    # Note: In a real scenario, you would need to implement user registration
    # For this test, we'll assume users already exist or create them via direct API
    print_status "WARNING" "Assuming test users already exist in the database"
    print_status "INFO" "Test users:"
    echo "  - ${ADMIN_EMAIL} (Admin)"
    echo "  - ${MODERATOR_EMAIL} (Moderator)"
    echo "  - ${USER_EMAIL} (Regular User)"
}

# Function to authenticate users (placeholder)
authenticate_users() {
    print_status "TEST" "Authenticating users..."
    
    # Note: This is a placeholder. In a real implementation, you would:
    # 1. Call the login endpoint
    # 2. Extract tokens from responses
    # 3. Store tokens for subsequent requests
    
    print_status "WARNING" "Authentication not implemented in this test script"
    print_status "INFO" "For testing, you can:"
    echo "  1. Use the Python test script: python test_role_system.py"
    echo "  2. Test via Swagger UI: ${BASE_URL}/docs"
    echo "  3. Implement proper authentication in the API"
}

# Function to test role creation
test_role_creation() {
    print_status "TEST" "Testing role creation..."
    
    # Create admin role
    local admin_role_data='{
        "name": "test_admin",
        "description": "Test admin role",
        "permissions": ["*"],
        "is_active": true
    }'
    
    api_request "POST" "/roles" "$admin_role_data" "" "201"
    
    # Create moderator role
    local moderator_role_data='{
        "name": "test_moderator",
        "description": "Test moderator role",
        "permissions": ["user:read", "user:update", "content:moderate"],
        "is_active": true
    }'
    
    api_request "POST" "/roles" "$moderator_role_data" "" "201"
    
    # Create user role
    local user_role_data='{
        "name": "test_user",
        "description": "Test user role",
        "permissions": ["profile:read", "profile:update", "resume:read"],
        "is_active": true
    }'
    
    api_request "POST" "/roles" "$user_role_data" "" "201"
}

# Function to test role listing
test_role_listing() {
    print_status "TEST" "Testing role listing..."
    
    # List all roles
    api_request "GET" "/roles" "" "" "200"
    
    # List active roles only
    api_request "GET" "/roles?active_only=true" "" "" "200"
    
    # Search roles
    api_request "GET" "/roles?search=admin" "" "" "200"
}

# Function to test role updates
test_role_updates() {
    print_status "TEST" "Testing role updates..."
    
    # This would require getting a role ID first
    print_status "INFO" "Role update testing requires role ID from previous operations"
    print_status "INFO" "Use Swagger UI at ${BASE_URL}/docs for interactive testing"
}

# Function to test role assignments
test_role_assignments() {
    print_status "TEST" "Testing role assignments..."
    
    # This would require user IDs and role IDs
    print_status "INFO" "Role assignment testing requires user and role IDs"
    print_status "INFO" "Use Swagger UI at ${BASE_URL}/docs for interactive testing"
}

# Function to test role statistics
test_role_statistics() {
    print_status "TEST" "Testing role statistics..."
    
    api_request "GET" "/roles/stats" "" "" "200"
}

# Function to test user role queries
test_user_role_queries() {
    print_status "TEST" "Testing user role queries..."
    
    # This would require user IDs
    print_status "INFO" "User role query testing requires user IDs"
    print_status "INFO" "Use Swagger UI at ${BASE_URL}/docs for interactive testing"
}

# Function to run all tests
run_all_tests() {
    print_status "INFO" "Starting API tests for Role and User models"
    echo "=================================================="
    
    if ! check_server; then
        exit 1
    fi
    
    create_test_users
    authenticate_users
    
    echo ""
    print_status "TEST" "Running API endpoint tests..."
    echo "----------------------------------------"
    
    test_role_creation
    echo ""
    test_role_listing
    echo ""
    test_role_updates
    echo ""
    test_role_assignments
    echo ""
    test_role_statistics
    echo ""
    test_user_role_queries
    
    echo ""
    echo "=================================================="
    print_status "SUCCESS" "API tests completed!"
    print_status "INFO" "For comprehensive testing, use:"
    echo "  - Python test script: python test_role_system.py"
    echo "  - Swagger UI: ${BASE_URL}/docs"
    echo "  - ReDoc: ${BASE_URL}/redoc"
}

# Function to show help
show_help() {
    echo "Role and User Model API Testing Script"
    echo ""
    echo "Usage: $0 [OPTION]"
    echo ""
    echo "Options:"
    echo "  -h, --help     Show this help message"
    echo "  -s, --server   Check server status only"
    echo "  -r, --roles    Test role operations only"
    echo "  -u, --users    Test user operations only"
    echo "  -a, --all      Run all tests (default)"
    echo ""
    echo "Examples:"
    echo "  $0                    # Run all tests"
    echo "  $0 --server          # Check server status"
    echo "  $0 --roles           # Test role operations only"
    echo ""
    echo "Prerequisites:"
    echo "  1. Start the FastAPI server:"
    echo "     cd backend && python -m uvicorn app.main:app --reload"
    echo "  2. Ensure database is initialized"
    echo "  3. Install jq for JSON formatting (optional)"
}

# Main script logic
case "${1:-}" in
    -h|--help)
        show_help
        ;;
    -s|--server)
        check_server
        ;;
    -r|--roles)
        if check_server; then
            test_role_creation
            test_role_listing
            test_role_updates
            test_role_statistics
        fi
        ;;
    -u|--users)
        if check_server; then
            test_user_role_queries
        fi
        ;;
    -a|--all|"")
        run_all_tests
        ;;
    *)
        print_status "ERROR" "Unknown option: $1"
        show_help
        exit 1
        ;;
esac

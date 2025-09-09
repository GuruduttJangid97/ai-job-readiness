#!/usr/bin/env python3
"""
Start the AI Job Readiness API server for testing.

This script starts the FastAPI server with proper configuration
for development and testing purposes.
"""

import uvicorn
import os
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

if __name__ == "__main__":
    print("🚀 Starting AI Job Readiness API Server...")
    print("=" * 50)
    print("📋 Available Endpoints:")
    print("  • Health Check: http://localhost:8000/health")
    print("  • API Docs: http://localhost:8000/docs")
    print("  • ReDoc: http://localhost:8000/redoc")
    print("  • API Info: http://localhost:8000/api/v1/info")
    print("")
    print("🔐 Authentication Endpoints:")
    print("  • Register: POST http://localhost:8000/api/v1/auth/register")
    print("  • Login: POST http://localhost:8000/api/v1/auth/jwt/login")
    print("  • Get Current User: GET http://localhost:8000/api/v1/auth/me")
    print("  • Logout: POST http://localhost:8000/api/v1/auth/jwt/logout")
    print("")
    print("👤 User Management Endpoints:")
    print("  • Get Profile: GET http://localhost:8000/api/v1/users/profile")
    print("  • Update Profile: PUT http://localhost:8000/api/v1/users/profile")
    print("  • List Users: GET http://localhost:8000/api/v1/users/")
    print("")
    print("🔑 Role Management Endpoints:")
    print("  • Create Role: POST http://localhost:8000/api/v1/roles/")
    print("  • List Roles: GET http://localhost:8000/api/v1/roles/")
    print("  • Assign Role: POST http://localhost:8000/api/v1/roles/assign")
    print("")
    print("📄 Resume Management Endpoints:")
    print("  • Create Resume: POST http://localhost:8000/api/v1/resumes/")
    print("  • Upload File: POST http://localhost:8000/api/v1/resumes/upload")
    print("  • List Resumes: GET http://localhost:8000/api/v1/resumes/")
    print("  • Analyze Resume: POST http://localhost:8000/api/v1/resumes/{id}/analyze")
    print("")
    print("📊 Postman Collection:")
    print("  • Import: AI_Job_Readiness_API.postman_collection.json")
    print("")
    print("=" * 50)
    
    # Start the server
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

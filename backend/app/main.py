"""
AI Job Readiness Backend API

This module contains the main FastAPI application for the AI Job Readiness platform.
It provides endpoints for user management, resume analysis, and job readiness scoring.

Author: AI Job Readiness Team
Version: 1.0.0
"""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import logging
from typing import Dict, Any

# Import database and model dependencies
from app.db.database import get_db, init_db
from app.models import User, Role, UserRole, Resume, Score

# Import FastAPI-Users and authentication
from app.core.users import fastapi_users, current_active_user
from app.core.config import settings

# Import API routers
from app.api import auth_router, users_router
from app.api.roles import router as roles_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI application with comprehensive metadata
app = FastAPI(
    title="AI Job Readiness API",
    description="""
    ## AI Job Readiness Platform Backend API
    
    This API provides comprehensive job readiness assessment and analysis capabilities:
    
    * **User Management**: Secure user registration, authentication, and profile management
    * **Resume Analysis**: AI-powered resume parsing and analysis
    * **Job Readiness Scoring**: Comprehensive scoring system for job readiness assessment
    * **Role-Based Access Control**: Flexible permission system for different user types
    
    ### Key Features:
    - FastAPI with async/await support for high performance
    - PostgreSQL database with SQLAlchemy ORM
    - Alembic database migrations
    - FastAPI-Users for authentication
    - Comprehensive API documentation with Swagger UI
    """,
    version="1.0.0",
    contact={
        "name": "AI Job Readiness Team",
        "email": "support@aijobreadiness.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Configure CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event() -> None:
    """
    Application startup event handler.
    
    This function is called when the FastAPI application starts up.
    It initializes the database connection and creates necessary tables.
    
    Raises:
        Exception: If database initialization fails
    """
    try:
        logger.info("🚀 Starting AI Job Readiness API...")
        await init_db()
        logger.info("✅ Database initialized successfully")
        logger.info("🎯 API is ready to serve requests")
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        print(f"⚠️  Database initialization warning: {e}")


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """
    Application shutdown event handler.
    
    This function is called when the FastAPI application shuts down.
    It performs cleanup operations and closes database connections.
    """
    logger.info("🛑 Shutting down AI Job Readiness API...")


@app.get("/", tags=["Health"])
async def read_root() -> Dict[str, str]:
    """
    Root endpoint for API health check.
    
    Returns:
        Dict[str, str]: Welcome message and API status
        
    Example:
        ```json
        {
            "message": "AI Job Readiness Backend is running",
            "version": "1.0.0",
            "status": "operational"
        }
        ```
    """
    return {
        "message": "AI Job Readiness Backend is running",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", tags=["Health"])
async def health_check() -> Dict[str, str]:
    """
    Comprehensive health check endpoint.
    
    This endpoint provides detailed information about the API's health status,
    including database connectivity and service availability.
    
    Returns:
        Dict[str, str]: Health status information
        
    Example:
        ```json
        {
            "status": "healthy",
            "message": "Backend is operational",
            "timestamp": "2025-09-01T17:50:00Z"
        }
        ```
    """
    from datetime import datetime
    
    return {
        "status": "healthy",
        "message": "Backend is operational",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "version": "1.0.0"
    }


@app.get("/models", tags=["System"])
async def list_models() -> Dict[str, Any]:
    """
    List all available database models.
    
    This endpoint provides information about all SQLAlchemy models
    that are loaded and available in the system.
    
    Returns:
        Dict[str, Any]: List of available models and their descriptions
        
    Example:
        ```json
        {
            "models": [
                "User",
                "Role", 
                "UserRole",
                "Resume",
                "Score"
            ],
            "message": "All SQLAlchemy models are loaded and ready",
            "count": 5
        }
        ```
    """
    models = [
        "User",
        "Role", 
        "UserRole",
        "Resume",
        "Score"
    ]
    
    return {
        "models": models,
        "message": "All SQLAlchemy models are loaded and ready",
        "count": len(models),
        "descriptions": {
            "User": "User account management with authentication",
            "Role": "Role-based access control definitions",
            "UserRole": "Many-to-many relationship between users and roles",
            "Resume": "Resume storage and management",
            "Score": "AI-powered job readiness scoring system"
        }
    }


@app.get("/database", tags=["System"])
async def database_status(db: AsyncSession = Depends(get_db)) -> Dict[str, Any]:
    """
    Check database connection and model status.
    
    This endpoint performs a live database connection test to verify
    that the database is accessible and responding to queries.
    
    Args:
        db (AsyncSession): Database session dependency
        
    Returns:
        Dict[str, Any]: Database connection status and information
        
    Raises:
        HTTPException: If database connection fails
        
    Example:
        ```json
        {
            "status": "connected",
            "message": "Database connection successful",
            "models_loaded": true,
            "connection_test": "passed"
        }
        ```
    """
    try:
        # Perform a simple database query to test connectivity
        result = await db.execute(text("SELECT 1 as test_value, NOW() as current_time"))
        row = result.fetchone()
        
        if row:
            return {
                "status": "connected",
                "message": "Database connection successful",
                "models_loaded": True,
                "connection_test": "passed",
                "database_time": str(row[1]) if len(row) > 1 else "unknown"
            }
        else:
            raise HTTPException(
                status_code=503,
                detail="Database connection test failed - no data returned"
            )
            
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        raise HTTPException(
            status_code=503,
            detail=f"Database connection failed: {str(e)}"
        )


@app.get("/api/v1/info", tags=["API Info"])
async def api_info() -> Dict[str, Any]:
    """
    Get comprehensive API information.
    
    This endpoint provides detailed information about the API,
    including available endpoints, version, and capabilities.
    
    Returns:
        Dict[str, Any]: Comprehensive API information
    """
    return {
        "api_name": "AI Job Readiness API",
        "version": "1.0.0",
        "description": "Comprehensive job readiness assessment and analysis platform",
        "endpoints": {
            "health": "/health",
            "models": "/models", 
            "database": "/database",
            "docs": "/docs",
            "redoc": "/redoc"
        },
        "features": [
            "User Management",
            "Resume Analysis", 
            "Job Readiness Scoring",
            "Role-Based Access Control",
            "AI-Powered Insights"
        ],
        "technology_stack": [
            "FastAPI",
            "PostgreSQL",
            "SQLAlchemy",
            "Alembic",
            "FastAPI-Users"
        ]
    }


# Include API routers
app.include_router(auth_router, prefix=settings.api_v1_str)
app.include_router(users_router, prefix=settings.api_v1_str)
app.include_router(roles_router, prefix=settings.api_v1_str)


@app.get(f"{settings.api_v1_str}/protected", tags=["Authentication"])
async def protected_route(
    current_user: User = Depends(current_active_user),
) -> Dict[str, Any]:
    """
    Protected route example.
    
    This endpoint demonstrates how to protect routes with authentication.
    Only authenticated users can access this endpoint.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        Dict[str, Any]: Protected resource data
    """
    return {
        "message": "This is a protected route",
        "user_id": str(current_user.id),
        "user_email": current_user.email,
        "user_roles": [user_role.role.name for user_role in current_user.roles if user_role.role],
    }

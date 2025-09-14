"""
AI Job Readiness Backend API

This module contains the main FastAPI application for the AI Job Readiness platform.
It provides endpoints for user management, resume analysis, and job readiness scoring.

Author: AI Job Readiness Team
Version: 1.0.0
"""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
import logging
from typing import Dict, Any
from datetime import datetime

# Import database and model dependencies
from app.db.database import get_db, init_db
from app.models import User, Role, UserRole, Resume, Score

# Import FastAPI-Users and authentication
from app.core.users import fastapi_users, current_active_user, auth_backend
from app.schemas.user import UserRead, UserCreate, UserUpdate
from app.core.config import settings

# Import API routers
from app.api import auth_router, users_router
from app.api.roles import router as roles_router
from app.api.resume import router as resume_router

# Import utilities
from app.utils.response import create_success_response, create_error_response
from app.utils.decorators import handle_errors, log_execution_time
from app.utils.caching import cache_manager, cached, CACHE_CONFIG
from app.utils.performance import monitor_performance, performance_monitor, system_monitor

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.logging.level.upper()),
    format=settings.logging.format
)
logger = logging.getLogger(__name__)

# Initialize FastAPI application with comprehensive metadata
app = FastAPI(
    title=settings.api.title,
    description=settings.api.description,
    version=settings.api.version,
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
    allow_origins=settings.api.cors_origins,
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
@handle_errors("Failed to get root information")
@log_execution_time
@monitor_performance("root_endpoint")
@cached(ttl=CACHE_CONFIG["system_info"], key_prefix="root")
async def read_root() -> JSONResponse:
    """
    Root endpoint for API health check.
    
    Returns:
        JSONResponse: Welcome message and API status
        
    Example:
        ```json
        {
            "success": true,
            "message": "AI Job Readiness Backend is running",
            "data": {
                "version": "1.0.0",
                "status": "operational",
                "docs": "/docs",
                "health": "/health"
            }
        }
        ```
    """
    return create_success_response(
        message="AI Job Readiness Backend is running",
        data={
            "version": settings.api.version,
            "status": "operational",
            "docs": "/docs",
            "health": "/health"
        }
    )


@app.get("/health", tags=["Health"])
@handle_errors("Health check failed")
@log_execution_time
@monitor_performance("health_check")
@cached(ttl=CACHE_CONFIG["database_status"], key_prefix="health")
async def health_check() -> JSONResponse:
    """
    Comprehensive health check endpoint.
    
    This endpoint provides detailed information about the API's health status,
    including database connectivity and service availability.
    
    Returns:
        JSONResponse: Health status information
        
    Example:
        ```json
        {
            "success": true,
            "message": "Backend is operational",
            "data": {
                "status": "healthy",
                "timestamp": "2025-09-01T17:50:00Z",
                "version": "1.0.0"
            }
        }
        ```
    """
    from datetime import datetime
    
    return create_success_response(
        message="Backend is operational",
        data={
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "version": settings.api.version
        }
    )


@app.get("/models", tags=["System"])
@handle_errors("Failed to list models")
@log_execution_time
async def list_models() -> JSONResponse:
    """
    List all available database models.
    
    This endpoint provides information about all SQLAlchemy models
    that are loaded and available in the system.
    
    Returns:
        JSONResponse: List of available models and their descriptions
        
    Example:
        ```json
        {
            "success": true,
            "message": "All SQLAlchemy models are loaded and ready",
            "data": {
                "models": ["User", "Role", "UserRole", "Resume", "Score"],
                "count": 5,
                "descriptions": {...}
            }
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
    
    return create_success_response(
        message="All SQLAlchemy models are loaded and ready",
        data={
            "models": models,
            "count": len(models),
            "descriptions": {
                "User": "User account management with authentication",
                "Role": "Role-based access control definitions",
                "UserRole": "Many-to-many relationship between users and roles",
                "Resume": "Resume storage and management",
                "Score": "AI-powered job readiness scoring system"
            }
        }
    )


@app.get("/database", tags=["System"])
@handle_errors("Database status check failed")
@log_execution_time
async def database_status(db: AsyncSession = Depends(get_db)) -> JSONResponse:
    """
    Check database connection and model status.
    
    This endpoint performs a live database connection test to verify
    that the database is accessible and responding to queries.
    
    Args:
        db (AsyncSession): Database session dependency
        
    Returns:
        JSONResponse: Database connection status and information
        
    Example:
        ```json
        {
            "success": true,
            "message": "Database connection successful",
            "data": {
                "status": "connected",
                "models_loaded": true,
                "connection_test": "passed",
                "database_time": "2025-09-01T17:50:00Z"
            }
        }
        ```
    """
    # Perform a simple database query to test connectivity
    result = await db.execute(text("SELECT 1 as test_value, NOW() as current_time"))
    row = result.fetchone()
    
    if not row:
        raise HTTPException(
            status_code=503,
            detail="Database connection test failed - no data returned"
        )
    
    return create_success_response(
        message="Database connection successful",
        data={
            "status": "connected",
            "models_loaded": True,
            "connection_test": "passed",
            "database_time": str(row[1]) if len(row) > 1 else "unknown"
        }
    )


@app.get("/api/v1/info", tags=["API Info"])
@handle_errors("Failed to get API information")
@log_execution_time
@monitor_performance("api_info")
@cached(ttl=CACHE_CONFIG["system_info"], key_prefix="api_info")
async def api_info() -> JSONResponse:
    """
    Get comprehensive API information.
    
    This endpoint provides detailed information about the API,
    including available endpoints, version, and capabilities.
    
    Returns:
        JSONResponse: Comprehensive API information
    """
    return create_success_response(
        message="API information retrieved successfully",
        data={
            "api_name": settings.api.title,
            "version": settings.api.version,
            "description": settings.api.description,
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
    )


# Include FastAPI-Users authentication routes
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"]
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"]
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"]
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"]
)

@app.get("/api/v1/performance", tags=["Performance"])
@handle_errors("Failed to get performance metrics")
@log_execution_time
@monitor_performance("performance_metrics")
async def get_performance_metrics() -> JSONResponse:
    """
    Get application performance metrics.
    
    This endpoint provides detailed performance information including
    function execution times, system resources, and optimization suggestions.
    
    Returns:
        JSONResponse: Performance metrics and analysis
    """
    from app.utils.performance import get_performance_summary
    
    try:
        metrics = get_performance_summary()
        return create_success_response(
            message="Performance metrics retrieved successfully",
            data=metrics
        )
    except Exception as e:
        logger.error(f"Error getting performance metrics: {e}")
        return create_error_response(
            message="Failed to retrieve performance metrics",
            error=str(e),
            status_code=500
        )


@app.get("/api/v1/cache/status", tags=["Cache"])
@handle_errors("Failed to get cache status")
@log_execution_time
@monitor_performance("cache_status")
async def get_cache_status() -> JSONResponse:
    """
    Get cache system status and statistics.
    
    Returns:
        JSONResponse: Cache status and health information
    """
    try:
        cache_health = await cache_manager.health_check()
        return create_success_response(
            message="Cache status retrieved successfully",
            data=cache_health
        )
    except Exception as e:
        logger.error(f"Error getting cache status: {e}")
        return create_error_response(
            message="Failed to retrieve cache status",
            error=str(e),
            status_code=500
        )


@app.post("/api/v1/cache/clear", tags=["Cache"])
@handle_errors("Failed to clear cache")
@log_execution_time
@monitor_performance("cache_clear")
async def clear_cache() -> JSONResponse:
    """
    Clear all cache entries.
    
    Returns:
        JSONResponse: Cache clear operation result
    """
    try:
        from app.utils.caching import clear_all_cache
        await clear_all_cache()
        return create_success_response(
            message="Cache cleared successfully",
            data={"cleared_at": datetime.utcnow().isoformat() + "Z"}
        )
    except Exception as e:
        logger.error(f"Error clearing cache: {e}")
        return create_error_response(
            message="Failed to clear cache",
            error=str(e),
            status_code=500
        )


# Include API routers
app.include_router(auth_router, prefix=settings.api.v1_str)
app.include_router(users_router, prefix=settings.api.v1_str)
app.include_router(roles_router, prefix=settings.api.v1_str)
app.include_router(resume_router, prefix=settings.api.v1_str)


@app.get(f"{settings.api.v1_str}/protected", tags=["Authentication"])
@handle_errors("Failed to access protected route")
@log_execution_time
async def protected_route(
    current_user: User = Depends(current_active_user),
    db: AsyncSession = Depends(get_db)
) -> JSONResponse:
    """
    Protected route example.
    
    This endpoint demonstrates how to protect routes with authentication.
    Only authenticated users can access this endpoint.
    
    Args:
        current_user: Current authenticated user
        db: Database session
        
    Returns:
        JSONResponse: Protected resource data
    """
    # Get user roles with proper async loading
    from sqlalchemy import select
    from sqlalchemy.orm import selectinload
    from app.models.role import UserRole, Role
    
    # Query user with roles loaded
    result = await db.execute(
        select(User)
        .options(selectinload(User.roles).selectinload(UserRole.role))
        .where(User.id == current_user.id)
    )
    user_with_roles = result.scalar_one()
    
    return create_success_response(
        message="This is a protected route",
        data={
            "user_id": str(current_user.id),
            "user_email": current_user.email,
            "user_roles": [user_role.role.name for user_role in user_with_roles.roles if user_role.role],
        }
    )

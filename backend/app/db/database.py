"""
Database Configuration and Connection Management

This module provides database configuration, connection management, and session handling
for the AI Job Readiness platform. It uses SQLAlchemy with async/await support for
high-performance database operations.

Key Features:
- Async SQLAlchemy engine and session management
- Environment-based database URL configuration
- Lazy initialization of database connections
- Proper connection cleanup and resource management
- Support for both development and production environments

Author: AI Job Readiness Team
Version: 1.0.0
"""

import os
import logging
from typing import AsyncGenerator, Optional
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import MetaData, text
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging for database operations
logger = logging.getLogger(__name__)

# Create declarative base for SQLAlchemy models
# This base class will be inherited by all our database models
Base = declarative_base()

# Metadata for database migrations and schema management
metadata = MetaData()

# Global variables for lazy initialization of database connections
# These are initialized only when first accessed to improve startup performance
_engine: Optional[AsyncEngine] = None
_AsyncSessionLocal: Optional[sessionmaker] = None


def get_database_url() -> str:
    """
    Get database URL from environment variables or return default configuration.
    
    The database URL is constructed from environment variables to support
    different deployment environments (development, staging, production).
    
    Environment Variables:
        DATABASE_URL: Complete database connection string
        POSTGRES_USER: Database username (default: postgres)
        POSTGRES_PASSWORD: Database password (default: password)
        POSTGRES_HOST: Database host (default: localhost)
        POSTGRES_PORT: Database port (default: 5432)
        POSTGRES_DB: Database name (default: ai_job_readiness)
    
    Returns:
        str: Complete database connection URL
        
    Example:
        >>> get_database_url()
        'postgresql+asyncpg://postgres:password@localhost:5432/ai_job_readiness'
    """
    # Check if complete DATABASE_URL is provided
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        logger.info("Using DATABASE_URL from environment")
        return database_url
    
    # Construct database URL from individual components
    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "password")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    db_name = os.getenv("POSTGRES_DB", "ai_job_readiness")
    
    # Use asyncpg driver for async PostgreSQL operations
    database_url = f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db_name}"
    
    logger.info(f"Constructed database URL: postgresql+asyncpg://{user}:***@{host}:{port}/{db_name}")
    return database_url


def get_engine() -> AsyncEngine:
    """
    Get or create the async SQLAlchemy engine.
    
    This function implements lazy initialization of the database engine.
    The engine is created only when first accessed, which improves
    application startup time and allows for proper configuration.
    
    Returns:
        AsyncEngine: Configured SQLAlchemy async engine
        
    Note:
        The engine is configured with echo=True for development.
        Set echo=False in production for better performance.
    """
    global _engine
    
    if _engine is None:
        database_url = get_database_url()
        
        # Create async engine with optimized settings
        engine_kwargs = {
            "echo": os.getenv("SQL_ECHO", "true").lower() == "true",
            "future": True,
        }
        # SQLite (incl. aiosqlite) does not accept pool_size/max_overflow; use StaticPool for in-memory
        if database_url.startswith("sqlite+"):
            from sqlalchemy.pool import StaticPool
            engine_kwargs.update({
                "connect_args": {"check_same_thread": False},
                "poolclass": StaticPool,
            })
        else:
            engine_kwargs.update({
                "pool_size": 10,
                "max_overflow": 20,
                "pool_pre_ping": True,
                "pool_recycle": 3600,
            })
        _engine = create_async_engine(database_url, **engine_kwargs)
        
        logger.info("✅ Database engine created successfully")
    
    return _engine


def get_async_session_local() -> sessionmaker:
    """
    Get or create the async session factory.
    
    This function creates a sessionmaker that will be used to create
    database sessions. Each session represents a database transaction
    and should be properly closed after use.
    
    Returns:
        sessionmaker: Configured session factory for async sessions
    """
    global _AsyncSessionLocal
    
    if _AsyncSessionLocal is None:
        engine = get_engine()
        
        _AsyncSessionLocal = sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,  # Keep objects accessible after commit
        )
        
        logger.info("✅ Async session factory created successfully")
    
    return _AsyncSessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency function to get database session.
    
    This function is used as a FastAPI dependency to provide database
    sessions to API endpoints. It ensures proper session management
    and cleanup.
    
    Yields:
        AsyncSession: Database session for the current request
        
    Example:
        ```python
        @app.get("/users/")
        async def get_users(db: AsyncSession = Depends(get_db)):
            result = await db.execute(select(User))
            return result.scalars().all()
        ```
    """
    async_session = get_async_session_local()
    
    async with async_session() as session:
        try:
            logger.debug("Database session created")
            yield session
        except Exception as e:
            logger.error(f"Database session error: {e}")
            await session.rollback()
            raise
        finally:
            logger.debug("Database session closed")
            await session.close()


@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Context manager for database sessions.
    
    This function provides a context manager for database sessions
    that can be used outside of FastAPI dependencies.
    
    Yields:
        AsyncSession: Database session
        
    Example:
        ```python
        async with get_db_session() as db:
            result = await db.execute(select(User))
            users = result.scalars().all()
        ```
    """
    async_session = get_async_session_local()
    
    async with async_session() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise
        finally:
            await session.close()


async def init_db() -> None:
    """
    Initialize database tables.
    
    This function creates all database tables defined in the SQLAlchemy
    models. It should be called during application startup to ensure
    the database schema is up to date.
    
    Note:
        In production, use Alembic migrations instead of this function
        for better version control and rollback capabilities.
    """
    try:
        engine = get_engine()
        
        async with engine.begin() as conn:
            # Create all tables defined in Base.metadata
            await conn.run_sync(Base.metadata.create_all)
            
        logger.info("✅ Database tables initialized successfully")
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise


async def close_db() -> None:
    """
    Close database connections and cleanup resources.
    
    This function should be called during application shutdown to
    properly close all database connections and free up resources.
    """
    global _engine, _AsyncSessionLocal
    
    try:
        if _engine is not None:
            await _engine.dispose()
            _engine = None
            logger.info("✅ Database engine disposed successfully")
        
        _AsyncSessionLocal = None
        
    except Exception as e:
        logger.error(f"❌ Error closing database connections: {e}")


async def check_db_connection() -> bool:
    """
    Check if database connection is working.
    
    This function performs a simple database query to verify that
    the database is accessible and responding to requests.
    
    Returns:
        bool: True if connection is successful, False otherwise
    """
    try:
        async with get_db_session() as db:
            result = await db.execute(text("SELECT 1"))
            result.fetchone()
            logger.info("✅ Database connection check successful")
            return True
            
    except Exception as e:
        logger.error(f"❌ Database connection check failed: {e}")
        return False


async def get_db_info() -> dict:
    """
    Get database information and statistics.
    
    This function provides information about the database connection
    and basic statistics that can be useful for monitoring and debugging.
    
    Returns:
        dict: Database information and statistics
    """
    try:
        async with get_db_session() as db:
            # Get database version
            version_result = await db.execute(text("SELECT version()"))
            version = version_result.fetchone()[0]
            
            # Get database size
            size_result = await db.execute(text("""
                SELECT pg_size_pretty(pg_database_size(current_database()))
            """))
            size = size_result.fetchone()[0]
            
            # Get connection count
            conn_result = await db.execute(text("""
                SELECT count(*) FROM pg_stat_activity 
                WHERE datname = current_database()
            """))
            connections = conn_result.fetchone()[0]
            
            return {
                "version": version,
                "size": size,
                "active_connections": connections,
                "status": "connected"
            }
            
    except Exception as e:
        logger.error(f"❌ Error getting database info: {e}")
        return {
            "status": "error",
            "error": str(e)
        }

"""
Database query optimization utilities

This module provides utilities for optimizing database queries,
including query analysis, indexing recommendations, and performance monitoring.

@author AI Job Readiness Team
@version 1.0.0
"""

import time
import asyncio
import logging
from typing import Any, Dict, List, Optional, Tuple, Union
from functools import wraps
from sqlalchemy import text, select, func, and_, or_
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import Select

logger = logging.getLogger(__name__)


class QueryAnalyzer:
    """Analyze and optimize database queries"""
    
    @staticmethod
    def analyze_query(query: Select) -> Dict[str, Any]:
        """Analyze a SQLAlchemy query for optimization opportunities"""
        analysis = {
            "joins": 0,
            "where_clauses": 0,
            "order_by": 0,
            "group_by": 0,
            "having": 0,
            "subqueries": 0,
            "complexity_score": 0
        }
        
        # Basic analysis (simplified)
        query_str = str(query.compile(compile_kwargs={"literal_binds": True}))
        
        analysis["joins"] = query_str.upper().count("JOIN")
        analysis["where_clauses"] = query_str.upper().count("WHERE")
        analysis["order_by"] = query_str.upper().count("ORDER BY")
        analysis["group_by"] = query_str.upper().count("GROUP BY")
        analysis["having"] = query_str.upper().count("HAVING")
        analysis["subqueries"] = query_str.upper().count("SELECT") - 1
        
        # Calculate complexity score
        analysis["complexity_score"] = (
            analysis["joins"] * 2 +
            analysis["where_clauses"] * 1 +
            analysis["order_by"] * 1 +
            analysis["group_by"] * 2 +
            analysis["having"] * 2 +
            analysis["subqueries"] * 3
        )
        
        return analysis


class QueryOptimizer:
    """Optimize database queries for better performance"""
    
    @staticmethod
    def optimize_user_query(
        query: Select,
        include_roles: bool = False,
        include_resumes: bool = False,
        include_scores: bool = False
    ) -> Select:
        """Optimize user-related queries with selective loading"""
        if include_roles:
            query = query.options(selectinload("roles").selectinload("role"))
        
        if include_resumes:
            query = query.options(selectinload("resumes"))
        
        if include_scores:
            query = query.options(selectinload("scores"))
        
        return query
    
    @staticmethod
    def optimize_resume_query(
        query: Select,
        include_user: bool = False,
        include_scores: bool = False
    ) -> Select:
        """Optimize resume-related queries with selective loading"""
        if include_user:
            query = query.options(joinedload("user"))
        
        if include_scores:
            query = query.options(selectinload("scores"))
        
        return query
    
    @staticmethod
    def add_pagination_optimization(query: Select, page: int, per_page: int) -> Select:
        """Add pagination with optimized offset calculation"""
        # Use cursor-based pagination for better performance on large datasets
        offset = (page - 1) * per_page
        return query.offset(offset).limit(per_page)
    
    @staticmethod
    def add_search_optimization(query: Select, search_term: str, search_fields: List[str]) -> Select:
        """Add optimized search with proper indexing hints"""
        if not search_term:
            return query
        
        # Use ILIKE for case-insensitive search
        search_conditions = []
        for field in search_fields:
            search_conditions.append(field.ilike(f"%{search_term}%"))
        
        return query.where(or_(*search_conditions))


class QueryMonitor:
    """Monitor query performance and execution times"""
    
    def __init__(self):
        self.query_stats: Dict[str, Dict[str, Any]] = {}
    
    def track_query(self, query_name: str):
        """Decorator to track query performance"""
        def decorator(func):
            @wraps(func)
            async def async_wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = await func(*args, **kwargs)
                    execution_time = time.time() - start_time
                    self._record_stats(query_name, execution_time, success=True)
                    return result
                except Exception as e:
                    execution_time = time.time() - start_time
                    self._record_stats(query_name, execution_time, success=False, error=str(e))
                    raise
            
            @wraps(func)
            def sync_wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    execution_time = time.time() - start_time
                    self._record_stats(query_name, execution_time, success=True)
                    return result
                except Exception as e:
                    execution_time = time.time() - start_time
                    self._record_stats(query_name, execution_time, success=False, error=str(e))
                    raise
            
            if asyncio.iscoroutinefunction(func):
                return async_wrapper
            else:
                return sync_wrapper
        
        return decorator
    
    def _record_stats(self, query_name: str, execution_time: float, success: bool, error: str = None):
        """Record query statistics"""
        if query_name not in self.query_stats:
            self.query_stats[query_name] = {
                "total_calls": 0,
                "total_time": 0.0,
                "avg_time": 0.0,
                "min_time": float('inf'),
                "max_time": 0.0,
                "success_count": 0,
                "error_count": 0,
                "errors": []
            }
        
        stats = self.query_stats[query_name]
        stats["total_calls"] += 1
        stats["total_time"] += execution_time
        stats["avg_time"] = stats["total_time"] / stats["total_calls"]
        stats["min_time"] = min(stats["min_time"], execution_time)
        stats["max_time"] = max(stats["max_time"], execution_time)
        
        if success:
            stats["success_count"] += 1
        else:
            stats["error_count"] += 1
            if error:
                stats["errors"].append(error)
    
    def get_stats(self, query_name: Optional[str] = None) -> Dict[str, Any]:
        """Get query statistics"""
        if query_name:
            return self.query_stats.get(query_name, {})
        return self.query_stats
    
    def get_slow_queries(self, threshold: float = 1.0) -> List[Dict[str, Any]]:
        """Get queries that exceed the time threshold"""
        slow_queries = []
        for name, stats in self.query_stats.items():
            if stats["avg_time"] > threshold:
                slow_queries.append({
                    "query_name": name,
                    "avg_time": stats["avg_time"],
                    "max_time": stats["max_time"],
                    "total_calls": stats["total_calls"]
                })
        return sorted(slow_queries, key=lambda x: x["avg_time"], reverse=True)


# Global query monitor instance
query_monitor = QueryMonitor()


class DatabaseIndexer:
    """Recommend and manage database indexes"""
    
    RECOMMENDED_INDEXES = {
        "users": [
            "email",  # Unique index for login
            "is_active",  # For filtering active users
            "created_at",  # For sorting and pagination
            "first_name, last_name",  # For name searches
        ],
        "resumes": [
            "user_id",  # Foreign key index
            "is_active",  # For filtering
            "created_at",  # For sorting
            "file_type",  # For filtering by type
        ],
        "scores": [
            "user_id",  # Foreign key index
            "resume_id",  # Foreign key index
            "analysis_type",  # For filtering by type
            "overall_score",  # For sorting by score
            "analysis_date",  # For time-based queries
        ],
        "roles": [
            "name",  # Unique index for role lookup
            "is_active",  # For filtering
        ],
        "user_roles": [
            "user_id",  # Foreign key index
            "role_id",  # Foreign key index
            "user_id, role_id",  # Composite index for lookups
        ]
    }
    
    @staticmethod
    def get_index_recommendations(table_name: str) -> List[str]:
        """Get recommended indexes for a table"""
        return DatabaseIndexer.RECOMMENDED_INDEXES.get(table_name, [])
    
    @staticmethod
    def generate_index_sql(table_name: str, column: str, unique: bool = False) -> str:
        """Generate SQL for creating an index"""
        index_name = f"idx_{table_name}_{column.replace(',', '_').replace(' ', '_')}"
        unique_keyword = "UNIQUE " if unique else ""
        return f"CREATE {unique_keyword}INDEX IF NOT EXISTS {index_name} ON {table_name} ({column});"


class QueryBuilder:
    """Build optimized queries with best practices"""
    
    @staticmethod
    def build_user_list_query(
        search: Optional[str] = None,
        role: Optional[str] = None,
        is_active: Optional[bool] = None,
        include_roles: bool = True
    ) -> Select:
        """Build optimized user list query"""
        from app.models.user import User
        from app.models.role import UserRole, Role
        
        query = select(User)
        
        # Apply filters
        if search:
            search_filter = or_(
                User.first_name.ilike(f"%{search}%"),
                User.last_name.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%"),
            )
            query = query.where(search_filter)
        
        if is_active is not None:
            query = query.where(User.is_active == is_active)
        
        if role:
            query = query.join(UserRole).join(Role).where(Role.name == role)
        
        # Add selective loading
        if include_roles:
            query = query.options(selectinload("roles").selectinload("role"))
        
        return query
    
    @staticmethod
    def build_resume_list_query(
        user_id: str,
        is_active: Optional[bool] = None,
        is_public: Optional[bool] = None,
        include_user: bool = False
    ) -> Select:
        """Build optimized resume list query"""
        from app.models.resume import Resume
        
        query = select(Resume).where(Resume.user_id == user_id)
        
        # Apply filters
        if is_active is not None:
            query = query.where(Resume.is_active == is_active)
        if is_public is not None:
            query = query.where(Resume.is_public == is_public)
        
        # Add selective loading
        if include_user:
            query = query.options(joinedload("user"))
        
        return query.order_by(Resume.created_at.desc())
    
    @staticmethod
    def build_score_analysis_query(
        user_id: Optional[str] = None,
        resume_id: Optional[str] = None,
        analysis_type: Optional[str] = None,
        min_score: Optional[float] = None,
        max_score: Optional[float] = None
    ) -> Select:
        """Build optimized score analysis query"""
        from app.models.score import Score
        
        query = select(Score)
        
        # Apply filters
        if user_id:
            query = query.where(Score.user_id == user_id)
        if resume_id:
            query = query.where(Score.resume_id == resume_id)
        if analysis_type:
            query = query.where(Score.analysis_type == analysis_type)
        if min_score is not None:
            query = query.where(Score.overall_score >= min_score)
        if max_score is not None:
            query = query.where(Score.overall_score <= max_score)
        
        return query.order_by(Score.analysis_date.desc())


class ConnectionPoolOptimizer:
    """Optimize database connection pool settings"""
    
    OPTIMAL_SETTINGS = {
        "pool_size": 10,
        "max_overflow": 20,
        "pool_pre_ping": True,
        "pool_recycle": 3600,
        "pool_timeout": 30,
        "echo": False  # Disable SQL logging in production
    }
    
    @staticmethod
    def get_optimized_engine_kwargs() -> Dict[str, Any]:
        """Get optimized engine configuration"""
        return ConnectionPoolOptimizer.OPTIMAL_SETTINGS.copy()
    
    @staticmethod
    def recommend_pool_settings(
        expected_concurrent_users: int,
        avg_query_time: float = 0.1
    ) -> Dict[str, Any]:
        """Recommend pool settings based on expected load"""
        # Calculate pool size based on concurrent users and query time
        pool_size = max(5, min(20, int(expected_concurrent_users * 0.1)))
        max_overflow = pool_size * 2
        
        return {
            "pool_size": pool_size,
            "max_overflow": max_overflow,
            "pool_pre_ping": True,
            "pool_recycle": 3600,
            "pool_timeout": 30
        }


# Performance monitoring decorators
def monitor_query_performance(query_name: str):
    """Decorator to monitor query performance"""
    return query_monitor.track_query(query_name)


def optimize_query(include_relations: Optional[List[str]] = None):
    """Decorator to optimize queries with selective loading"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # This would be implemented based on specific query needs
            return await func(*args, **kwargs)
        return wrapper
    return decorator


# Utility functions for common optimizations
async def get_optimized_user_list(
    db: AsyncSession,
    page: int = 1,
    per_page: int = 10,
    search: Optional[str] = None,
    role: Optional[str] = None,
    is_active: Optional[bool] = None
) -> Tuple[List[Any], int]:
    """Get optimized user list with pagination"""
    query = QueryBuilder.build_user_list_query(search, role, is_active)
    
    # Get total count efficiently
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # Apply pagination
    query = QueryOptimizer.add_pagination_optimization(query, page, per_page)
    
    # Execute query
    result = await db.execute(query)
    users = result.scalars().all()
    
    return users, total


async def get_optimized_resume_list(
    db: AsyncSession,
    user_id: str,
    page: int = 1,
    per_page: int = 10,
    is_active: Optional[bool] = None,
    is_public: Optional[bool] = None
) -> Tuple[List[Any], int]:
    """Get optimized resume list with pagination"""
    query = QueryBuilder.build_resume_list_query(user_id, is_active, is_public)
    
    # Get total count efficiently
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar()
    
    # Apply pagination
    query = QueryOptimizer.add_pagination_optimization(query, page, per_page)
    
    # Execute query
    result = await db.execute(query)
    resumes = result.scalars().all()
    
    return resumes, total

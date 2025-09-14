"""
Caching utilities for improved performance

This module provides caching functionality using Redis or in-memory caching
to improve API response times and reduce database load.

@author AI Job Readiness Team
@version 1.0.0
"""

import json
import hashlib
from typing import Any, Optional, Union, Callable
from functools import wraps
import asyncio
from datetime import datetime, timedelta

try:
    import redis.asyncio as redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# In-memory cache as fallback
_memory_cache: dict = {}
_cache_ttl: dict = {}


class CacheManager:
    """Centralized cache management with Redis and in-memory fallback"""
    
    def __init__(self):
        self.redis_client: Optional[redis.Redis] = None
        self.use_redis = False
        self._initialize_redis()
    
    def _initialize_redis(self):
        """Initialize Redis connection if available"""
        if REDIS_AVAILABLE and hasattr(settings, 'redis_url'):
            try:
                self.redis_client = redis.from_url(
                    settings.redis_url,
                    encoding="utf-8",
                    decode_responses=True
                )
                self.use_redis = True
                logger.info("✅ Redis cache initialized")
            except Exception as e:
                logger.warning(f"Redis initialization failed: {e}. Using in-memory cache.")
                self.use_redis = False
        else:
            logger.info("Redis not available. Using in-memory cache.")
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        try:
            if self.use_redis and self.redis_client:
                value = await self.redis_client.get(key)
                if value:
                    return json.loads(value)
            else:
                # Check in-memory cache
                if key in _memory_cache:
                    # Check TTL
                    if key in _cache_ttl and datetime.now() < _cache_ttl[key]:
                        return _memory_cache[key]
                    else:
                        # Expired, remove from cache
                        _memory_cache.pop(key, None)
                        _cache_ttl.pop(key, None)
                return None
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None
    
    async def set(self, key: str, value: Any, ttl: int = 300) -> bool:
        """Set value in cache with TTL"""
        try:
            if self.use_redis and self.redis_client:
                await self.redis_client.setex(
                    key, 
                    ttl, 
                    json.dumps(value, default=str)
                )
                return True
            else:
                # Store in memory cache
                _memory_cache[key] = value
                _cache_ttl[key] = datetime.now() + timedelta(seconds=ttl)
                return True
        except Exception as e:
            logger.error(f"Cache set error: {e}")
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete value from cache"""
        try:
            if self.use_redis and self.redis_client:
                await self.redis_client.delete(key)
            else:
                _memory_cache.pop(key, None)
                _cache_ttl.pop(key, None)
            return True
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
            return False
    
    async def clear_pattern(self, pattern: str) -> int:
        """Clear all keys matching pattern"""
        try:
            if self.use_redis and self.redis_client:
                keys = await self.redis_client.keys(pattern)
                if keys:
                    await self.redis_client.delete(*keys)
                return len(keys)
            else:
                # For in-memory cache, we need to check each key
                keys_to_delete = [k for k in _memory_cache.keys() if pattern.replace('*', '') in k]
                for key in keys_to_delete:
                    _memory_cache.pop(key, None)
                    _cache_ttl.pop(key, None)
                return len(keys_to_delete)
        except Exception as e:
            logger.error(f"Cache clear pattern error: {e}")
            return 0
    
    async def health_check(self) -> dict:
        """Check cache health"""
        try:
            if self.use_redis and self.redis_client:
                await self.redis_client.ping()
                return {"status": "healthy", "type": "redis"}
            else:
                return {"status": "healthy", "type": "memory", "size": len(_memory_cache)}
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}


# Global cache manager instance
cache_manager = CacheManager()


def generate_cache_key(prefix: str, *args, **kwargs) -> str:
    """Generate a cache key from prefix and arguments"""
    # Create a hash of the arguments
    key_data = {
        "args": args,
        "kwargs": sorted(kwargs.items())
    }
    key_hash = hashlib.md5(
        json.dumps(key_data, sort_keys=True).encode()
    ).hexdigest()
    return f"{prefix}:{key_hash}"


def cache_key(prefix: str, key_func: Optional[Callable] = None):
    """Decorator to generate cache key for function arguments"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if key_func:
                key = key_func(*args, **kwargs)
            else:
                key = generate_cache_key(prefix, *args, **kwargs)
            return key
        return wrapper
    return decorator


def cached(ttl: int = 300, key_prefix: str = "default"):
    """Decorator to cache function results"""
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = generate_cache_key(key_prefix, *args, **kwargs)
            
            # Try to get from cache
            cached_result = await cache_manager.get(cache_key)
            if cached_result is not None:
                logger.debug(f"Cache hit for key: {cache_key}")
                return cached_result
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            await cache_manager.set(cache_key, result, ttl)
            logger.debug(f"Cached result for key: {cache_key}")
            
            return result
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = generate_cache_key(key_prefix, *args, **kwargs)
            
            # Try to get from cache
            cached_result = asyncio.run(cache_manager.get(cache_key))
            if cached_result is not None:
                logger.debug(f"Cache hit for key: {cache_key}")
                return cached_result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            asyncio.run(cache_manager.set(cache_key, result, ttl))
            logger.debug(f"Cached result for key: {cache_key}")
            
            return result
        
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


def cache_invalidate(pattern: str):
    """Decorator to invalidate cache after function execution"""
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)
            await cache_manager.clear_pattern(pattern)
            logger.debug(f"Cache invalidated for pattern: {pattern}")
            return result
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            asyncio.run(cache_manager.clear_pattern(pattern))
            logger.debug(f"Cache invalidated for pattern: {pattern}")
            return result
        
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


class QueryCache:
    """Database query caching utility"""
    
    @staticmethod
    async def get_cached_query(
        query_key: str,
        query_func: Callable,
        ttl: int = 300,
        *args,
        **kwargs
    ) -> Any:
        """Execute query with caching"""
        cache_key = f"query:{query_key}"
        
        # Try to get from cache
        cached_result = await cache_manager.get(cache_key)
        if cached_result is not None:
            return cached_result
        
        # Execute query
        result = await query_func(*args, **kwargs)
        
        # Cache result
        await cache_manager.set(cache_key, result, ttl)
        
        return result
    
    @staticmethod
    async def invalidate_user_cache(user_id: str):
        """Invalidate all cache entries for a specific user"""
        patterns = [
            f"user:{user_id}:*",
            f"query:user_{user_id}_*",
            f"resume:user_{user_id}_*"
        ]
        
        for pattern in patterns:
            await cache_manager.clear_pattern(pattern)


class ResponseCache:
    """API response caching utility"""
    
    @staticmethod
    def get_response_key(endpoint: str, user_id: Optional[str] = None, **params) -> str:
        """Generate cache key for API response"""
        key_data = {
            "endpoint": endpoint,
            "user_id": user_id,
            "params": sorted(params.items()) if params else {}
        }
        return f"response:{hashlib.md5(json.dumps(key_data, sort_keys=True).encode()).hexdigest()}"
    
    @staticmethod
    async def cache_response(
        key: str,
        response_data: Any,
        ttl: int = 300
    ) -> bool:
        """Cache API response"""
        return await cache_manager.set(key, response_data, ttl)
    
    @staticmethod
    async def get_cached_response(key: str) -> Optional[Any]:
        """Get cached API response"""
        return await cache_manager.get(key)


# Cache configuration
CACHE_CONFIG = {
    "user_profile": 600,  # 10 minutes
    "user_list": 300,     # 5 minutes
    "resume_list": 300,   # 5 minutes
    "resume_detail": 600, # 10 minutes
    "score_data": 1800,   # 30 minutes
    "system_info": 3600,  # 1 hour
    "database_status": 60, # 1 minute
}


async def warm_up_cache():
    """Warm up frequently accessed cache entries"""
    try:
        # Cache system information
        from app.main import get_system_info
        await get_system_info()
        
        logger.info("Cache warm-up completed")
    except Exception as e:
        logger.error(f"Cache warm-up failed: {e}")


async def clear_all_cache():
    """Clear all cache entries"""
    try:
        if cache_manager.use_redis and cache_manager.redis_client:
            await cache_manager.redis_client.flushdb()
        else:
            _memory_cache.clear()
            _cache_ttl.clear()
        
        logger.info("All cache cleared")
    except Exception as e:
        logger.error(f"Cache clear failed: {e}")

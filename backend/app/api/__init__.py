"""
API endpoints for AI Job Readiness Platform

This module contains all API endpoint definitions organized by functionality.
The API is structured with clear separation of concerns and comprehensive
documentation for each endpoint.

Author: AI Job Readiness Team
Version: 1.0.0
"""

from .auth import router as auth_router
from .users import router as users_router

__all__ = ["auth_router", "users_router"]

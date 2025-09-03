"""
Core configuration and utilities for AI Job Readiness Platform

This module contains core configuration, security settings, and utilities
that are used throughout the application.

Author: AI Job Readiness Team
Version: 1.0.0
"""

from .config import settings
from .security import get_password_hash, verify_password

__all__ = ["settings", "get_password_hash", "verify_password"]

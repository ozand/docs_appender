"""
Minimal models for the file combiner backend.

This module provides basic models needed for the application.
"""

from pydantic import BaseModel


class User(BaseModel):
    """Minimal user model for compatibility."""

    id: str = "anonymous"
    email: str = "anonymous@localhost"
    username: str = "anonymous"
    hashed_password: str = ""
    is_active: bool = True
    created_at: str = "2024-01-01T00:00:00"
    updated_at: str = "2024-01-01T00:00:00"


# Global user storage instance for compatibility
user_storage = None

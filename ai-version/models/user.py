"""Pydantic models (DTOs) representing users."""
from typing import Optional

from pydantic import BaseModel


class UserResponse(BaseModel):
    """Returned on signup."""

    id: str
    email: Optional[str] = None
    created_at: Optional[str] = None


class ProfileResponse(BaseModel):
    """Returned by GET /protected/profile."""

    id: str
    email: Optional[str] = None
    created_at: Optional[str] = None

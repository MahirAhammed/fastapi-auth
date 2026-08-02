"""
Auth dependencies for protected routes.

Two layers, as requested:
  1. `get_bearer_token`  - pulls the raw token out of the Authorization header.
  2. `get_current_user`  - verifies that token against Supabase and returns
                            the authenticated user.

Usage on a route:

    @router.get("/protected/profile")
    def profile(user: ProfileResponse = Depends(get_current_user)):
        ...
"""
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.exceptions import MissingTokenError
from models.user import ProfileResponse
from services.auth_service import AuthService

# `auto_error=False` so a missing/malformed header falls through to our own
# MissingTokenError (-> 401 {"error": "Access token required"}) instead of
# FastAPI's default 403. Registering this scheme with FastAPI is also what
# makes the "Authorize" padlock appear in Swagger UI for routes that depend
# on it.
bearer_scheme = HTTPBearer(auto_error=False, description="Supabase access token")


def get_bearer_token(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> str:
    """Layer 1: extract and sanity-check the bearer token from the header."""
    if credentials is None or not credentials.scheme.lower() == "bearer" or not credentials.credentials:
        raise MissingTokenError()
    return credentials.credentials


def get_current_user(token: str = Depends(get_bearer_token)) -> ProfileResponse:
    """Layer 2: verify the token against Supabase and return the user."""
    auth_service = AuthService()
    return auth_service.get_user_from_token(token)

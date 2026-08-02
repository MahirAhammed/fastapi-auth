"""
Business logic for authentication, and the only place in the codebase that
talks to the Supabase Python SDK. Routers should never import `supabase`
directly - they call into this service instead.
"""
from functools import lru_cache
from typing import Optional
from supabase_auth.errors import AuthApiError
# from gotrue.errors import AuthApiError
from supabase import Client, create_client

from core.config import get_settings
from core.exceptions import (
    AppError,
    ConflictError,
    InvalidCredentialsError,
    InvalidTokenError,
)
from models.auth import TokenResponse
from models.user import ProfileResponse, UserResponse


@lru_cache
def get_supabase_client() -> Client:
    """Return a cached Supabase client built from the anon key."""
    settings = get_settings()
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)


class AuthService:
    """Thin, testable wrapper around Supabase's `auth` module."""

    def __init__(self, client: Optional[Client] = None):
        self._client = client or get_supabase_client()

    # -- Sign up ----------------------------------------------------------
    def sign_up(self, email: str, password: str) -> UserResponse:
        try:
            result = self._client.auth.sign_up({"email": email, "password": password})
        except AuthApiError as exc:
            message = str(exc)
            if "already" in message.lower() or "registered" in message.lower():
                raise ConflictError("A user with this email already exists") from exc
            raise AppError(message, status_code=exc.status or 400) from exc

        user = result.user
        if user is None:
            raise AppError("Sign up failed: no user returned by Supabase")

        return UserResponse(
            id=str(user.id),
            email=user.email,
            created_at=str(user.created_at) if user.created_at else None,
        )

    # -- Log in -------------------------------------------------------------
    def sign_in(self, email: str, password: str) -> TokenResponse:
        try:
            result = self._client.auth.sign_in_with_password(
                {"email": email, "password": password}
            )
        except AuthApiError as exc:
            raise InvalidCredentialsError() from exc

        session = result.session
        if session is None:
            raise InvalidCredentialsError()

        return TokenResponse(
            access_token=session.access_token,
            refresh_token=session.refresh_token,
        )

    # -- Verify token / get current user ------------------------------------
    def get_user_from_token(self, access_token: str) -> ProfileResponse:
        try:
            result = self._client.auth.get_user(access_token)
        except AuthApiError as exc:
            raise InvalidTokenError() from exc
        except Exception as exc:  # network/parse errors etc.
            raise InvalidTokenError() from exc

        if result is None or result.user is None:
            raise InvalidTokenError()

        user = result.user
        return ProfileResponse(
            id=str(user.id),
            email=user.email,
            created_at=str(user.created_at) if user.created_at else None,
        )

    # -- Log out --------------------------------------------------------------
    def sign_out(self, access_token: str) -> None:
        """
        Revoke the session tied to `access_token`.

        By the time this is called, `access_token` has already been validated
        by the `get_current_user` dependency, so we know it's a real token.
        We use the Admin auth API's `sign_out`, which accepts a user's JWT
        directly (no refresh token needed) and revokes it server-side. If
        Supabase itself has trouble here we don't fail the request - the
        client already discards the token locally, so surfacing a 500 for a
        best-effort revocation would be misleading.
        """
        try:
            self._client.auth.admin.sign_out(access_token, "global")
        except Exception:
            pass

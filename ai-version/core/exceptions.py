"""
Centralized error handling.

Every error response returned by this API has the shape: {"error": "<message>"}.
Routers/services raise `AppError` (or a subclass) and a single exception
handler registered on the FastAPI app converts it to the correct HTTP response.
"""
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class AppError(Exception):
    """Base application error. Carries an HTTP status code and a message."""

    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class ValidationError(AppError):
    """400 - request payload failed validation (e.g. missing email/password)."""

    def __init__(self, message: str = "Invalid request payload"):
        super().__init__(message, status_code=status.HTTP_400_BAD_REQUEST)


class InvalidCredentialsError(AppError):
    """401 - login attempted with bad email/password."""

    def __init__(self, message: str = "Invalid login credentials"):
        super().__init__(message, status_code=status.HTTP_401_UNAUTHORIZED)


class MissingTokenError(AppError):
    """401 - no/malformed Authorization header on a protected route."""

    def __init__(self, message: str = "Access token required"):
        super().__init__(message, status_code=status.HTTP_401_UNAUTHORIZED)


class InvalidTokenError(AppError):
    """401 - token present but Supabase rejected it (invalid/expired)."""

    def __init__(self, message: str = "Invalid or expired token"):
        super().__init__(message, status_code=status.HTTP_401_UNAUTHORIZED)


class ConflictError(AppError):
    """409 - e.g. user already registered."""

    def __init__(self, message: str = "Resource already exists"):
        super().__init__(message, status_code=status.HTTP_409_CONFLICT)


def register_exception_handlers(app: FastAPI) -> None:
    """Attach exception handlers so every error response is {"error": "..."}."""

    @app.exception_handler(AppError)
    async def app_error_handler(_: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content={"error": exc.message})

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(
        _: Request, exc: RequestValidationError
    ) -> JSONResponse:
        # Pydantic/FastAPI validation failures (missing/invalid fields) -> 400
        first_error = exc.errors()[0] if exc.errors() else None
        if first_error:
            loc = ".".join(str(part) for part in first_error.get("loc", []) if part != "body")
            message = f"{loc}: {first_error.get('msg', 'invalid value')}" if loc else first_error.get(
                "msg", "Invalid request payload"
            )
        else:
            message = "Invalid request payload"
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"error": message})

    @app.exception_handler(Exception)
    async def unhandled_error_handler(_: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "Internal server error"},
        )

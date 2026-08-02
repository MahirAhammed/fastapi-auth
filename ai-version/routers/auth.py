"""HTTP layer for /auth/* routes. No business logic here - delegates to AuthService."""
from fastapi import APIRouter, Depends, status

from core.dependencies import get_bearer_token, get_current_user
from models.auth import LoginRequest, SignUpRequest, TokenResponse
from models.user import ProfileResponse, UserResponse
from services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


def get_auth_service() -> AuthService:
    return AuthService()


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(payload: SignUpRequest, service: AuthService = Depends(get_auth_service)) -> UserResponse:
    return service.sign_up(email=payload.email, password=payload.password)


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login(payload: LoginRequest, service: AuthService = Depends(get_auth_service)) -> TokenResponse:
    return service.sign_in(email=payload.email, password=payload.password)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(
    token: str = Depends(get_bearer_token),
    # Validates the token (401 if invalid/expired) before we attempt sign out.
    _current_user: ProfileResponse = Depends(get_current_user),
    service: AuthService = Depends(get_auth_service),
) -> None:
    service.sign_out(token)
    return None
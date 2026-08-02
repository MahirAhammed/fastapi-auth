"""Protected routes - require a valid Supabase access token via `get_current_user`."""
from fastapi import APIRouter, Depends

from core.dependencies import get_current_user
from models.user import ProfileResponse

router = APIRouter(prefix="/protected", tags=["protected"])


@router.get("/profile", response_model=ProfileResponse)
def profile(current_user: ProfileResponse = Depends(get_current_user)) -> ProfileResponse:
    return current_user


@router.get("/dashboard")
def dashboard(current_user: ProfileResponse = Depends(get_current_user)) -> dict:
    return {
        "message": f"Welcome back, {current_user.email or current_user.id}!",
        "user_id": current_user.id,
        "widgets": ["revenue", "active_sessions", "recent_activity"],
    }

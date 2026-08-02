"""Public routes - no authentication required."""
from fastapi import APIRouter

router = APIRouter(prefix="/public", tags=["public"])


@router.get("/info")
def public_info() -> dict:
    return {"message": "Welcome stranger! This info is public."}

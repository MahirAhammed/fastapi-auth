from fastapi import APIRouter, Depends
from services import auth_service
from core.dependencies import get_current_user
from models.auth import AuthRequest, TokenResponse

router = APIRouter(prefix= "/auth", tags= ["auth"])

@router.post("/signup", status_code= 201)
def sign_up(req: AuthRequest):
    return auth_service.sign_up(req.email, req.password)

@router.post("/login", response_model= TokenResponse, status_code= 200)
def login(req: AuthRequest):
    return auth_service.login(req.email, req.password)

@router.post("/logout", status_code= 204)
def logout(user= Depends(get_current_user)):
    auth_service.logout()
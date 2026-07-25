from typing import Annotated
from fastapi import APIRouter, Header, Depends
from services import auth_service
from core.dependencies import get_current_user
from models.auth import UserMetadataResponse

router = APIRouter(tags= ["profile"])

@router.get("/public/info", status_code= 200)
def public():
    return {"message": "Welcome stranger! This info is public." }

@router.get("/protected/profile", response_model= UserMetadataResponse, status_code= 200)
def protected(user= Depends(get_current_user)):
    return UserMetadataResponse(id= user.id, email= user.email,created_at= user.created_at)

@router.get("/protected/dashboard", status_code= 200)
def protected(user= Depends(get_current_user)):
    return {"message": "Dashboard info"}
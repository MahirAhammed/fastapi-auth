from typing import Annotated
from fastapi import APIRouter, Header
from services import auth_service

router = APIRouter(tags= ["profile"])

@router.get("/public/info", status_code= 200)
def public():
    return {"message": "Welcome stranger! This info is public." }

@router.get("/protected/profile", status_code= 200)
def protected(authorization: Annotated[str | None, Header()] = None):
    auth_service.get_access_token(authorization)
    
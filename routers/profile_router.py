from typing import Annotated
from fastapi import APIRouter, Header
from services import auth_service
from models.auth import UserMetadataResponse

router = APIRouter(tags= ["profile"])

@router.get("/public/info", status_code= 200)
def public():
    return {"message": "Welcome stranger! This info is public." }

@router.get("/protected/profile", status_code= 200)
def protected(authorization: Annotated[str | None, Header()] = None):
    response = auth_service.get_profile(authorization)
    return UserMetadataResponse(
        id= response["id"], 
        email= response["email"],
        created_at= response["created_at"]
    )
    
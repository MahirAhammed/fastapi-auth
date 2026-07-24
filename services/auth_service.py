from supabase_client import supabase;
from models.auth import TokenResponse, UserMetadataResponse
from core.exception import *

def sign_up(email: str, password: str) -> dict:
    if not email or not password:
        raise ValidationError()
    
    response = supabase.auth.sign_up({"email": email, "password": password})
    return response.user


def login(email: str, password: str) -> TokenResponse:
    if not email or not password:
        raise ValidationError()

    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
    except Exception:
        raise InvalidCredentialsError()

    return TokenResponse(
        access_token= response.session.access_token, 
        refresh_token= response.session.refresh_token
    )


def get_access_token(authorization: str) -> UserMetadataResponse:
    if not authorization:
        raise MissingTokenError()
    
    auth_scheme = authorization.split(" ")
    if len(auth_scheme) != 2 or auth_scheme[0] != "Bearer" or not auth_scheme[1]:
        raise InvalidTokenError()
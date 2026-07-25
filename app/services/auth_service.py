from app.supabase_client import supabase;
from app.models.auth import TokenResponse
from app.core.exception import *

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

def logout():
    try:
        supabase.auth.sign_out()
    except Exception:
        raise InvalidTokenError()
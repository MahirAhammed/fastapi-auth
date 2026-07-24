from supabase_client import supabase;
from fastapi import HTTPException
from models.auth import TokenResponse

def sign_up(email: str, password: str) -> dict:
    if not email or not password:
        raise HTTPException(status_code= 400, detail= "Bad Request")
    
    response = supabase.auth.sign_up({"email": email, "password": password})
    return response.user


def login(email: str, password: str) -> TokenResponse:
    if not email or not password:
        raise HTTPException(status_code= 400, detail= "Invalid login credentials")
    
    response = supabase.auth.sign_in_with_password({"email": email, "password": password})
    return TokenResponse(
        access_token= response.session.access_token, 
        refresh_token= response.session.refresh_token
    )
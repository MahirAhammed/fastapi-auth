from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from supabase_auth.errors import AuthApiError
from routers import auth_router, profile_router
from core.exception import CustomException

app = FastAPI(title= "Auth-practice", version= "0.1.0")
app.include_router(auth_router.router)
app.include_router(profile_router.router)

@app.exception_handler(CustomException)
async def custom_exception_handler(_, ex: CustomException):
    return JSONResponse(status_code=ex.status_code, content={"error": ex.message})

@app.exception_handler(HTTPException)
async def http_exception_handler(_, ex: HTTPException):
    return JSONResponse(status_code= ex.status_code, content= {"error": ex.detail})

@app.exception_handler(AuthApiError)
async def auth_api_exception_handler(_, ex: AuthApiError):
    return JSONResponse(status_code= 401, content= {"error": ex.message})
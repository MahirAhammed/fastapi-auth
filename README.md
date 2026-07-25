# FastAPI Auth
A lightweight FastAPI backend using Supabase as the authentication provider. It includes signup, login, logout, and token-protected routes, with Supabase issuing and validating JWTs on the server's behalf.

## File structure
app/
├── core/
│   ├── exceptions.py       # custom error classes (CustomException and subclasses)
│   ├── config.py           # loads and validates environment variables
│   └── dependencies.py     # auth guards (HTTPBearer, get_current_user)
├── models/                 # Pydantic request/response DTOs
├── routers/                # Exposed endpoints
├── services/               # Implementation of business logic
├── supabase_client.py      # shared Supabase client instance
└── main.py                 # app entrypoint

## Environment variables
- Copy .env.example to .env and replace in real values:

|Variable	    | Description    |
|---------------|----------------|
|SUPABASE_URL | Supabase project URL (Settings -> API -> Project URL), no trailing slash|
|SUPABASE_KEY | Supabase anon/public key (Settings -> API -> Project API keys)|

## Install & Run it
> Setup a python virtual env and install dependencies:
```bash
python3 -m venv venv
source /venv/bin/activate
pip instal -r requirements.txt
```

> Run the application
```bash
uvicorn app.main:app --reload
```

## API Reference

### Public Endpoints

| Method | Endpoint | Request Body | Success Response | Error Responses |
|--------|----------|--------------|------------------|--------------------|
| POST   | `/auth/signup`  | `{"email": string, "password": string}`     | `201` user object (`id`, `email`, `created_at`, ...) | `400` `{"error": "email and password are required"}` |
| POST   | `/auth/login` | `{"email": string, "password": string}` | `200` `{"access_token": string, "refresh_token": string}` | `400` `{"error": "email and password are required"}`, `401` `{"error": "Invalid login credentials"}` |

### Protected Endpoints

> All protected endpoints require `Authorization: Bearer <access_token>`.

| Method | Endpoint | Request Body | Success Response | Error Responses |
|--------|--------- |:-------------:|-----------------|--------------------------------|
| POST   | `/auth/logout` | — | `204` No Content | `401` `{"error": "Access token required"}`, `401` `{"error": "Invalid or expired token"}`           |
| GET    | `/protected/profile`    | —             | `200` `{"id": string, "email": string, "created_at": string}` | `401` `{"error": "Access token required"}` , `401` `{"error": "Invalid or expired token"}`           |
| GET    | `/protected/dashboard`  | — | `200` `{"message": "Dashboard info"`                                    | `401` `{"error": "Access token required"}`, `401` `{"error": "Invalid or expired token"}`           |


## Swagger-UI
- Interactive docs available at `http://127.0.0.1:8000/docs` after running the application
[Swagger](/swagger.png)
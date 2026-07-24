from fastapi import FastAPI
from supabase import create_client, Client
from supabase.client import ClientOptions
from config import SUPABASE_URL, SUPABASE_KEY

app = FastAPI(title= "Auth-practice", version= "0.1.0")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY,
    options=ClientOptions(
        postgrest_client_timeout=10,
        storage_client_timeout=10,
    )
)
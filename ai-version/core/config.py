"""
Application configuration.

Loads Supabase credentials and other settings from environment variables
(via a .env file in local development).
"""
import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Simple settings container populated from environment variables."""

    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")  # anon/public key
    APP_NAME: str = os.getenv("APP_NAME", "Supabase Auth API")

    def validate(self) -> None:
        missing = [
            name
            for name, value in (
                ("SUPABASE_URL", self.SUPABASE_URL),
                ("SUPABASE_KEY", self.SUPABASE_KEY),
            )
            if not value
        ]
        if missing:
            raise RuntimeError(
                f"Missing required environment variable(s): {', '.join(missing)}. "
                "Copy .env.example to .env and fill in your Supabase project values."
            )


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.validate()
    return settings

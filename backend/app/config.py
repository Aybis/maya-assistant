"""Application configuration settings"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Application
    APP_NAME: str = "Maya Assistant"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # CORS
    CORS_ORIGINS: str = "http://localhost:3000"

    # Supabase
    SUPABASE_URL: str
    SUPABASE_KEY: Optional[str] = None  # Anon key (for backward compatibility)
    SUPABASE_ANON_KEY: Optional[str] = None
    SUPABASE_SERVICE_ROLE_KEY: Optional[str] = None  # Service role key (bypasses RLS)
    SUPABASE_JWT_SECRET: str

    def get_supabase_key(self) -> str:
        """Get the appropriate Supabase key (prefers service role for backend)"""
        # Prefer service role key for backend operations (bypasses RLS)
        if self.SUPABASE_SERVICE_ROLE_KEY:
            return self.SUPABASE_SERVICE_ROLE_KEY
        # Fall back to SUPABASE_KEY or SUPABASE_ANON_KEY
        return self.SUPABASE_KEY or self.SUPABASE_ANON_KEY or ""

    # OpenAI
    OPENAI_API_KEY: Optional[str] = None

    # Anthropic Claude
    ANTHROPIC_API_KEY: Optional[str] = None

    # Google Gemini
    GOOGLE_API_KEY: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True

    def get_cors_origins(self) -> list[str]:
        """Parse CORS origins from comma-separated string"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]


# Global settings instance
settings = Settings()

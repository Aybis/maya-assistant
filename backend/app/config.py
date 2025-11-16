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
    SUPABASE_KEY: str
    SUPABASE_JWT_SECRET: str

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

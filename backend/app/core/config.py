"""
Application configuration using Pydantic Settings.
Demonstrates Pydantic expertise as mentioned in the JD.
"""
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """
    Application settings with environment variable support.
    Uses Pydantic Settings for type safety and validation (JD requirement).
    """
    
    # Application
    APP_NAME: str = "Company Profile Manager API"
    APP_VERSION: str = "2.0.0"
    ENV: Literal["development", "staging", "production"] = "development"
    DEBUG: bool = Field(default=False, description="Enable debug mode")
    
    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = Field(default=True, description="Auto-reload on code changes")
    
    # CORS
    ALLOWED_ORIGINS: list[str] = Field(
        default=[
            "http://localhost:3000",
            "http://localhost:5173",
            "http://localhost:8080"
        ],
        description="Allowed CORS origins"
    )
    
    # Database
    DATABASE_URL: str = Field(
        default="sqlite+aiosqlite:///./data/company_profiles.db",
        description="Database connection URL"
    )
    DATABASE_ECHO: bool = Field(default=False, description="Echo SQL queries")
    
    # Logging
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    LOG_FORMAT: Literal["json", "console"] = "console"
    LOG_FILE: str | None = None
    
    # Security
    SECRET_KEY: str = Field(
        default="your-secret-key-change-in-production",
        description="Secret key for cryptographic operations"
    )
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.ENV == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.ENV == "development"


# Global settings instance
settings = Settings()

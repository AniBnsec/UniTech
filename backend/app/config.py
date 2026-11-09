"""Application configuration settings."""

from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    APP_NAME: str = "ThreatShield API"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str
    ASYNC_DATABASE_URL: str = ""
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # JWT Authentication
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION: int = 86400  # 24 hours in seconds
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:3000"
    
    # API Keys - AI/LLM
    OPENAI_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    
    # Threat Intelligence APIs
    URLHAUS_API_URL: str = "https://urlhaus-api.abuse.ch/v1/"
    GOOGLE_SAFE_BROWSING_API_KEY: str = ""
    VIRUSTOTAL_API_KEY: str = ""
    PHISHTANK_API_KEY: str = ""
    
    # Blockchain
    BLOCKCHAIN_RPC_URL: str = ""
    PRIVATE_KEY: str = ""
    CONTRACT_ADDRESS: str = ""
    ETHERSCAN_API_KEY: str = ""
    
    # Security Settings
    RATE_LIMIT_ENABLED: bool = True
    MAX_REQUESTS_PER_MINUTE: int = 60
    BLOCK_PRIVATE_IPS: bool = True
    ALLOW_LOCALHOST: bool = False
    
    # Timeouts
    HTTP_TIMEOUT: int = 30
    DNS_TIMEOUT: int = 10
    TLS_TIMEOUT: int = 15
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()

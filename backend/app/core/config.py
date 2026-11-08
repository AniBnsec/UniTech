import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AegisTrust - Digital Threat & Trust Intelligence"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    # AI / LLM Integration
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # Web3 / Blockchain Settings
    WEB3_PROVIDER_URI: str = os.getenv("WEB3_PROVIDER_URI", "http://127.0.0.1:8545")
    CONTRACT_ADDRESS: str = os.getenv("CONTRACT_ADDRESS", "0x5FbDB2315678afecb367f032d93F642f64180aa3")
    WALLET_PRIVATE_KEY: str = os.getenv("WALLET_PRIVATE_KEY", "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80")
    
    # Security Engine Constants
    MAX_REDIRECTS: int = 5
    HTTP_TIMEOUT_SECONDS: float = 4.0
    DNS_TIMEOUT_SECONDS: float = 2.5
    SSL_TIMEOUT_SECONDS: float = 3.0
    
    # CORS
    CORS_ORIGINS: list[str] = ["*"]

settings = Settings()


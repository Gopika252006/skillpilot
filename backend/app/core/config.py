import os
from pydantic import BaseModel
from typing import List

class Settings(BaseModel):
    PROJECT_NAME: str = "SkillPilot"
    PROJECT_TAGLINE: str = "Your AI-powered personal learning intelligence"
    API_V1_STR: str = "/api"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "codepilot-super-secret-key-for-dev-challenge-2026-hacktoberfest")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./codepilot.db")
    
    # Open-weight AI settings
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "ollama")  # "ollama", "openai_compatible", "local"
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "llama3.2:3b")  # default developer laptop model
    AI_TIMEOUT_SECONDS: int = int(os.getenv("AI_TIMEOUT_SECONDS", "30"))
    
    # Storage settings
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "./uploads")
    MAX_FILE_SIZE_MB: int = 15
    ALLOWED_EXTENSIONS: List[str] = [".pdf", ".txt", ".md", ".png", ".jpg", ".jpeg", ".webp"]
    
    # CORS: Explicit allowed origins (never wildcard '*' with credentials)
    CORS_ORIGINS: List[str] = [
        origin.strip()
        for origin in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000"
        ).split(",")
        if origin.strip()
    ]

settings = Settings()

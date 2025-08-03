from pydantic_settings import BaseSettings
from typing import Optional, List
import os
from pathlib import Path

class Settings(BaseSettings):
    # Base paths
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    UPLOAD_DIR: Path = BASE_DIR / "uploads"
    DATA_PATH: Path = BASE_DIR / "data"
    ML_MODEL_PATH: Path = BASE_DIR / "models"
    LOG_FILE: Path = BASE_DIR / "logs" / "app.log"
    
    # Database
    database_url: str = os.getenv("DATABASE_URL", "postgresql://dataops_user:dataops_password@localhost:5432/dataops_db")
    
    # Security
    secret_key: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Email settings
    smtp_host: Optional[str] = os.getenv("SMTP_HOST")
    smtp_port: int = int(os.getenv("SMTP_PORT", "587"))
    smtp_user: Optional[str] = os.getenv("SMTP_USER")
    smtp_password: Optional[str] = os.getenv("SMTP_PASSWORD")
    
    # CORS settings
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://*.vercel.app",
        "https://*.vercel.app/*"
    ]
    
    # API settings
    api_v1_prefix: str = "/api/v1"
    project_name: str = "DataOps Inspector"
    version: str = "1.0.0"
    
    class Config:
        env_file = ".env"

settings = Settings()

# Ensure directories exist
try:
    settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    settings.DATA_PATH.mkdir(parents=True, exist_ok=True)
    settings.ML_MODEL_PATH.mkdir(parents=True, exist_ok=True)
    settings.LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
except Exception as e:
    print(f"Warning: Could not create directories: {e}") 
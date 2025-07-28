from pydantic_settings import BaseSettings
from typing import Optional, List
import os

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://dataops_user:dataops_password@localhost:5432/dataops_db"
    
    # Security
    SECRET_KEY: str = "your-super-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Email Configuration
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_USE_TLS: bool = True
    
    # Application
    DEBUG: bool = True
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1"]
    
    # File Upload
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 100 * 1024 * 1024  # 100MB
    
    # ML Configuration
    ML_MODEL_PATH: str = "models"
    DATA_PATH: str = "data"
    DRIFT_THRESHOLD: float = 0.1
    PERFORMANCE_THRESHOLD: float = 0.8
    
    # Monitoring
    ALERT_EMAIL_RECIPIENTS: List[str] = ["admin@company.com"]
    ALERT_WEBHOOK_URL: Optional[str] = None
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/dataops.log"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create settings instance
settings = Settings()

# Ensure directories exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.ML_MODEL_PATH, exist_ok=True)
os.makedirs(settings.DATA_PATH, exist_ok=True)
os.makedirs(os.path.dirname(settings.LOG_FILE), exist_ok=True) 
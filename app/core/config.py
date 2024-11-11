from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    
    DATABASE_URL: str
    SQLALCHEMY_DATABASE_URI: str
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra='allow',
    )
    
    # Apis Configuration
    PROJECT_NAME: str = "Ranking Tenis de mesa"
    API_VERSION: str = "v1"
    API_V1_STR: str = f"/api/{API_VERSION}"
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

settings = Settings()
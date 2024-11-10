from typing import Optional
from pydantic import BaseSettings, PostgresDsn, validator
from functools import lru_cache
import secrets
from typing import Any, Dict, List

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "SpinMaster API"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    ALGORITHM: str = "HS256"
    
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: str = "5432"
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )
    
    # Redis Settings
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    
    # Ranking System
    INITIAL_RATING: int = 1000
    MIN_MATCHES_FOR_RANKING: int = 5
    K_FACTOR: int = 32  # For ELO calculation
    
    # Tournament Settings
    MIN_PLAYERS_FOR_TOURNAMENT: int = 4
    MAX_PLAYERS_FOR_TOURNAMENT: int = 32
    TOURNAMENT_VICTORY_BONUS: int = 50
    
    # Cache Settings
    CACHE_EXPIRE_MINUTES: int = 15
    RANKING_CACHE_KEY: str = "rankings"
    STATISTICS_CACHE_KEY: str = "statistics"
    
    # Rate Limiting
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_MINUTES: int = 1
    
    class Config:
        case_sensitive = True
        env_file = ".env"


# Create a cached instance of settings
@lru_cache()
def get_settings() -> Settings:
    return Settings()


# Export settings instance
settings = get_settings()
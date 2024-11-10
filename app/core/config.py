from typing import Any, List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra='allow'
    )

    # Conexão com banco de dados
    POSTGRES_HOST: str = "postgres"  # Nome do serviço no docker-compose
    POSTGRES_USER: str = "postgres"  # Usuário da aplicação
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "spinmaster"
    POSTGRES_PORT: str = "5432"
    API_VERSION: str = "v1"
    PROJECT_NAME: str = "Tenis de Mesa"
    API_V1_STR: str = "/api/v1"
    
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",        # React default
        "http://localhost:8000",        # API itself
        "http://localhost",
        "http://localhost:4200",        # Angular default
        "http://localhost:8080",        # Vue default
        "https://localhost",
        "https://localhost:3000",
        "https://localhost:8000",
        "*"                            # Allow all origins in development
    ]
    

    @property
    def DATABASE_URL(self) -> str:
        """Gera a URL de conexão com o banco"""
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

settings = Settings()
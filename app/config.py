from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # Pydantic will check: 1) .env file, 2) environment variables, 3) use default
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "postgres"
    POSTGRES_HOST: str = "db"
    POSTGRES_PORT: int = 5432

    SECRET_KEY: str 
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8", 
    )

    @property
    def database_url(self) -> str:
        base_url = f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        
        return base_url
    

settings = Settings()
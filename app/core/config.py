from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "Insighta"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    PORT: int = 8000
    WORKERS: int = 2

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int

    MONGO_URI: str
    MONGO_DB_NAME: str

    ENVIRONMENT: str = "dev"

    BACKEND_CORS_ORIGINS: List[str] = Field(default_factory=list)

    ADMIN_EMAIL: str
    ADMIN_PWD: str

    JWT_SECRET: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_DAYS: int

    OPENAI_API_KEY: str

    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_CHANNEL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="forbid",
    )

settings = Settings()

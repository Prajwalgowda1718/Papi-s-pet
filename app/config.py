from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env")

    # Core
    APP_ENV: str = "development"
    DEBUG: bool = True
    GEMINI_API_KEY: str

    # Cost control
    DAILY_COST_LIMIT: float = 5.0
    MONTHLY_COST_LIMIT: float = 15.0
    TOKEN_COST_RATE: float = 0.00002

    # Rate limiting
    MAX_REQUESTS_PER_MINUTE: int = 10

    # Semantic cache
    SIMILARITY_THRESHOLD: float = 0.85


settings = Settings()

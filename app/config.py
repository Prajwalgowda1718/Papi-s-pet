import os
from dotenv import load_dotenv


load_dotenv()


class Settings:
    APP_ENV: str = os.getenv("APP_ENV", "development")
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    DAILY_COST_LIMIT: int = int(os.getenv("DAILY_COST_LIMIT", 30))
    MONTHLY_COST_LIMIT: int = int(os.getenv("MONTHLY_COST_LIMIT", 500))


settings = Settings()

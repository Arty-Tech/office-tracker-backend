from pydantic import BaseSettings


class Settings(BaseSettings):
    
    PROJECT_NAME: str = "Office Tracker"
    PROJECT_VERSION: str = "0.0.1"
    DATABASE_URL: str = "postgresql+asyncpg://user:password@postgres/time_tracker_db"
    SECRET_KEY: str = "whothebestiamthebestohyeah"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

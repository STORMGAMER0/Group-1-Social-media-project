from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    APP_NAME: str = "Mini Social Media Feed"

    class Config:
        env_file = ".env"

settings = Settings()

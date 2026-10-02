from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "PocketSmart AI"
    app_env: str = "development"
    secret_key: str = "change-this-development-secret"
    database_url: str = "sqlite:///./data/pocketsmart.db"
    ai_mode: str = "mock"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    cors_origins: str = "http://127.0.0.1:8000,http://localhost:8000"
    max_image_mb: int = Field(default=5, ge=1, le=20)
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    @property
    def cors_origin_list(self): return [x.strip() for x in self.cors_origins.split(",") if x.strip()]
    @property
    def database_path(self):
        return self.database_url.removeprefix("sqlite:///")

@lru_cache
def get_settings(): return Settings()

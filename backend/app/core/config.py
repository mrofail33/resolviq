from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Resolviq"
    database_url: str = "postgresql+psycopg://resolviq:resolviq@localhost:5432/resolviq"
    ai_provider: str = "mock"
    openai_api_key: str | None = None
    openai_model: str = "gpt-4.1-mini"
    upload_dir: str = "uploads"
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    demo_api_key: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()

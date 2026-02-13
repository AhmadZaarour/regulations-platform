from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Regulations Platform API"
    env: str = "local"  # local|staging|prod
    log_level: str = "INFO"

    # Security / Auth
    secret_key: str = "secret_key"  # REQUIRED (must come from .env)
    jwt_algorithm: str = "HS256"
    access_token_exp_minutes: int = 30
    refresh_token_exp_days: int = 14

    model_config = SettingsConfigDict(
        env_file=".env.example",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()

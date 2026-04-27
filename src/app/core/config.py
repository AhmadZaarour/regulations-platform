from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Regulations Platform API"
    env: str = "local"  # local|staging|prod
    log_level: str = "INFO"

    secret_key: str = "dev-only-change-me"  # <-- add this
    access_token_exp_minutes: int = 30
    refresh_token_exp_days: int = 7
    jwt_algorithm: str = "HS256"

    postgres_db: str = "regs"
    postgres_user: str = "regs"
    postgres_password: str = "regs"
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def redis_url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


settings = Settings()

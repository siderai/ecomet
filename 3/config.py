from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    clickhouse_url: str = Field(default="http://localhost:8123")
    clickhouse_user: str = Field(...)
    clickhouse_password: str = Field(...)
    clickhouse_db: str = Field(default="test")

    github_token: str = Field(...)
    max_concurrent_requests: int = Field(default=20, ge=1, le=100)
    requests_per_second: int = Field(default=100, ge=1, le=5000)
    top_repositories_limit: int = Field(default=100, ge=1, le=100)

    batch_size: int = Field(default=100, ge=1, le=10000)

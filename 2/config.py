from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    github_token: str = Field(...)
    max_concurrent_requests: int = Field(default=10, ge=1, le=100)
    requests_per_second: int = Field(default=5, ge=1, le=100)
    top_repositories_limit: int = Field(default=100, ge=1, le=100)

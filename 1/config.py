from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    db_host: str = Field(...)
    db_port: int = Field(default=5432)
    db_user: str = Field(...)
    db_password: str = Field(...)
    db_name: str = Field(...)
    db_pool_min_size: int = Field(default=5, ge=1, le=50)
    db_pool_max_size: int = Field(default=20, ge=1, le=100)
    db_timeout: float = Field(default=30.0)
    db_command_timeout: float = Field(default=60.0)

    app_host: str = Field(default="0.0.0.0")
    app_port: int = Field(default=8000)

    @model_validator(mode='after')
    def validate_pool_sizes(self) -> 'Settings':
        if self.db_pool_min_size > self.db_pool_max_size:
            raise ValueError(
                f"db_pool_min_size ({self.db_pool_min_size}) must be <= "
                f"db_pool_max_size ({self.db_pool_max_size})"
            )
        return self

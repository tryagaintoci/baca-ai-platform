from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "BACA AI Platform"
    app_version: str = "0.4.0"
    debug: bool = True
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    database_host: str
    database_port: int
    database_name: str
    database_user: str
    database_password: str

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
    )

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+psycopg://"
            f"{self.database_user}:{self.database_password}"
            f"@{self.database_host}:{self.database_port}/"
            f"{self.database_name}"
        )


settings = Settings()

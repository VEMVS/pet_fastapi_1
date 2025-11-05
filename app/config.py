from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_username: str
    database_port: int
    database_password: str
    database_host: str
    database_name: str
    secret_key: str
    access_token_expire_minutes: int
    algorithm: str

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )

settings = Settings()
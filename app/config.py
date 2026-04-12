from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    lm_api_token: str
    model_name: str
    model_context_length: int
    model_temperature: float
    model_api_url: str

    app_host: str
    app_port: int
    debug: bool

    rate_limit_requests: int
    queue_max_connections: int

    pandoc_path: str
    pdftotext_path: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()

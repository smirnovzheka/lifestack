from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    anthropic_api_key: str
    api_token: str
    database_url: str = "sqlite:///./data/lifestack.db"
    cors_origins: str = "http://localhost:3000,http://localhost"

    model_config = {"env_file": ".env"}

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]


settings = Settings()

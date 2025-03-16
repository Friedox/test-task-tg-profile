from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    postgres_user: str = Field(..., alias="POSTGRES_USER")
    postgres_password: str = Field(..., alias="POSTGRES_PASSWORD")
    postgres_db: str = Field(..., alias="POSTGRES_DB")
    postgres_host: str = Field("db", alias="DB_HOST")
    postgres_port: int = Field(5432, alias="DB_PORT")
    telegram_bot_token: str = Field(..., alias="BOT_TOKEN")

    @property
    def db_url(self) -> str:
        return (
            f"postgres://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    class Config:
        env_file = ".env"
        populate_by_name = True


settings = Settings()

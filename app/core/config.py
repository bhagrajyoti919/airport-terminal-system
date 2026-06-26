from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    APP_NAME: str

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    DEBUG: bool = False

    class Config:
        env_file = ".env"


settings = Settings()
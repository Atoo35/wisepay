from pydantic import SecretStr
from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="./.env",env_file_encoding="utf-8")

    AI_MODEL:str
    GEMINI_API_KEY: SecretStr
    SPLITWISE_API_KEY: SecretStr
    SPLITWISE_API_SECRET: SecretStr
    REDIRECT_URI: str

    DB_HOST:str
    DB_NAME:str
    DB_USER:str
    DB_PASSWORD:SecretStr
    DB_PORT:int

    # External APIs
    PAYMAN_API_KEY:SecretStr

settings = Settings()
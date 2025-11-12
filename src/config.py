import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


env_path = ".env.test" if "PYTEST_VERSION" in os.environ else ".env.dev"
load_dotenv(env_path)


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str

    model_config = SettingsConfigDict(env_file=env_path, env_file_encoding="utf-8")


settings = Settings(_env_file=env_path, _env_file_encoding="utf-8")  # type: ignore[call-arg]
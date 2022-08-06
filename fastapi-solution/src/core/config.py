from logging import config as logging_config

from pydantic import BaseSettings, Field

from core.logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)


class ElasticSearchSettings(BaseSettings):
    host: str = Field(default="localhost", env="ELASTIC_HOST")
    port: str = Field(default="9200", env="ELASTIC_PORT")


class RedisSettings(BaseSettings):
    host: str = Field(default="localhost", env="REDIS_HOST")
    port: str = Field(default="6379", env="REDIS_PORT")


class ServicesSettings(BaseSettings):
    elasticsearch: ElasticSearchSettings = ElasticSearchSettings()
    redis: RedisSettings = RedisSettings()


class ProjectSettings(BaseSettings):
    name: str = Field(default="movies", env="PROJECT_NAME")
    base_dir: str = Field(default="", env="PROJECT_BASE_DIR")

    class Config:
        fields = {"name": {"env": "PROJECT_NAME"}, "base_dir": {"env": "PROJECT_BASE_DIR"}}

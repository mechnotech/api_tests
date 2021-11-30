from pydantic import BaseSettings, Field
from dotenv import load_dotenv

load_dotenv()


class TestSettings(BaseSettings):
    es_host: str = Field('127.0.0.1', env='ELASTIC_HOST')
    es_port: int = Field(9200, env='ELASTIC_PORT')
    redis_host: str = Field('127.0.0.1', env='REDIS_HOST')
    redis_port: int = Field(6379, env='REDIS_PORT')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

from pydantic import BaseSettings, Field
from dotenv import load_dotenv

load_dotenv(dotenv_path='.dev.env')


class TestSettings(BaseSettings):

    es_host: str = Field('127.0.0.1', env='ELASTIC_HOST')
    es_port: int = Field(9200, env='ELASTIC_PORT')
    redis_host: str = Field('127.0.0.1', env='REDIS_HOST')
    redis_port: int = Field(6379, env='REDIS_PORT')
    api_host: str = Field('127.0.0.1', env='FAST_API_HOST')
    api_port: str = Field(8000, env='FAST_API_PORT')


config = TestSettings()
print('*'*50, config.redis_host, '*'*50)
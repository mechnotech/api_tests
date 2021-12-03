import os

from pydantic import BaseSettings


class TestSettings(BaseSettings):

    es_host: str = os.getenv('ELASTIC_HOST', '127.0.0.1')
    es_port: int = os.getenv('ELASTIC_PORT', 9200)
    redis_host: str = os.getenv('REDIS_HOST', '127.0.0.1')
    redis_port: int = os.getenv('REDIS_PORT', 6379)
    api_host: str = os.getenv('FAST_API_HOST', '127.0.0.1')
    api_port: str = os.getenv('FAST_API_PORT', 8000)


config = TestSettings()
SERVICE_URL = f'http://{config.api_host}:{config.api_port}/api/v1/'

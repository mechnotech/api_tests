import logging

import requests
from redis import Redis

from settings import config
from utils.backoff_decorator import backoff

my_logger = logging.getLogger('my_logger')
my_handler = logging.StreamHandler()
my_logger.addHandler(my_handler)
my_logger.setLevel(logging.INFO)


@backoff(logy=my_logger)
def ping_redis():
    my_logger.info(f'--------------- Connecting Redis HOST={config.redis_host} ---------------------')
    connection = Redis(config.redis_host, socket_connect_timeout=1)
    connection.ping()
    my_logger.info('=================== Redis ready =====================')



@backoff(logy=my_logger)
def ping_es():
    my_logger.info(f'--------------- Connecting ES HOST={config.es_host} ---------------------')
    res = requests.get(f'http://{config.es_host}:{config.es_port}')
    if res.json()['tagline'] != 'You Know, for Search':
        my_logger.warning('Wait for ES!!!')
        raise Exception
    my_logger.info('++++++++++++++++ ES ready ++++++++++++++++++++')


if __name__ == '__main__':
    ping_redis()
    ping_es()

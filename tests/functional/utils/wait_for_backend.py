import logging
import time

import requests
from redis import Redis

from tests.functional.settings import config
from tests.functional.utils.backoff_decorator import backoff

my_logger = logging.getLogger('my_logger')
my_handler = logging.StreamHandler()
my_logger.addHandler(my_handler)
my_logger.setLevel(logging.INFO)


@backoff(logy=my_logger)
def ping_redis():
    connection = Redis(config.redis_host, socket_connect_timeout=1)
    connection.ping()
    my_logger.info('=================== Redis ready =====================')
    time.sleep(2)

@backoff(logy=my_logger)
def ping_es():
    res = requests.get(f'http://{config.es_host}:{config.es_port}')
    if res.json()['tagline'] != 'You Know, for Search':
        my_logger.warning('Wait for ES!!!')
        raise Exception
    my_logger.info('++++++++++++++++ ES ready ++++++++++++++++++++')
    time.sleep(2)


if __name__ == '__main__':
    ping_redis()
    ping_es()

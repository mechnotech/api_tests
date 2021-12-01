import logging

import requests
from redis import Redis

from backoff_decorator import backoff

my_logger = logging.getLogger('my_logger')
my_handler = logging.StreamHandler()
my_logger.addHandler(my_handler)
my_logger.setLevel(logging.INFO)


@backoff(logy=my_logger)
def ping_redis():
    connection = Redis('redis', socket_connect_timeout=1)
    connection.ping()
    my_logger.info('Redis ready')


@backoff(logy=my_logger)
def ping_es():
    res = requests.get('http://elasticsearch:9200')
    if res.json()['tagline'] != 'You Know, for Search':
        my_logger.warning('Wait for ES!!!')
        raise Exception
    my_logger.info('ES ready')


if __name__ == '__main__':
    ping_redis()
    ping_es()

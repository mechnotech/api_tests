import json
import os

from elasticsearch import Elasticsearch

from tests.funcional.settings import TestSettings

dir_path = os.path.dirname(os.path.realpath(__file__))

indexes_schemes = {
    'movies': 'movie_scheme_es.json',
    'genres': 'genre_scheme_es.json',
    'persons': 'person_scheme_es.json'
}
fixtures_files = {
    'genres': 'genres_fixtures.txt',
    'persons': 'persons_fixtures.txt',
    'movies': 'movies_fixtures.txt'
}

conf = TestSettings()


class ESConnector:

    def __init__(self):
        self.connection = Elasticsearch(host=conf.es_host, port=conf.es_port)
        self.connection.cluster.health(wait_for_status='yellow', request_timeout=1)

    def load(self, index: str, block: list):
        body = ''.join(block)
        self.connection.bulk(body=body, index=index, params={'filter_path': 'items.*.error'})

    def is_index_exist(self, index: str):
        return self.connection.indices.exists(index=index)

    def create_index(self, index: str, file_name: str):
        with open(f'{dir_path}/../testdata/{file_name}', 'r') as f:
            self.connection.indices.create(index=index, body=json.load(f))
            return self.connection.indices.get(index=index)

    def __del__(self):
        self.connection.close()


def create_indexes():
    es_connect = ESConnector()
    for index, scheme in indexes_schemes.items():
        if not es_connect.is_index_exist(index=index):
            es_connect.create_index(index=index, file_name=scheme)


def apply_fixtures():
    es_connect = ESConnector()
    for index, fixtures in fixtures_files.items():
        with open(f'{dir_path}/../testdata/{fixtures}', 'r') as f:
            es_connect.load(index=index, block=f.readlines())


def apply_test_set():
    create_indexes()
    apply_fixtures()


if __name__ == '__main__':
    apply_test_set()

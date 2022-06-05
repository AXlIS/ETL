import json

from backoff import backoff
from elasticsearch import Elasticsearch


class ESSaver:
    def __init__(self, config):
        self.config = config
        self.client = self.get_client()
        self.dataset = []
        self.counter = 0

    def get_client(self):
        return Elasticsearch(self.config)

    @backoff()
    def create_index(self, file, index_name) -> None:
        """Создание индекса, если он отсутствует"""
        with open(file, 'r') as f:
            mapping = json.load(f)
            if not self.client.indices.exists(index=index_name):
                self.client.indices.create(index=index_name, body=mapping)

    def save_dataset(self, data, index_name, dataset_length) -> None:
        """Сохранение данных"""
        for item in data:
            self.dataset.extend([
                json.dumps({
                    "index": {"_index": index_name, "_id": item.get("id")}
                }),
                json.dumps(item)
            ])
            self.counter += 1
            if len(self.dataset) == dataset_length or self.counter == len(data):
                self.save(index_name)
                self.dataset = []

    @backoff()
    def save(self, index_name) -> None:
        self.client.bulk(body='\n'.join(self.dataset) + '\n', index=index_name)

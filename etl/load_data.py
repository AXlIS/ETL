from datetime import datetime
from time import sleep

from config import dsl, es_config
from es_saver import ESSaver
from state import JsonFileStorage, State
from tasks import tasks


def load_from_postgres(loader, state_key) -> list:
    """Загрузка данных из Postgresql"""
    return loader(dsl, state_key).load()


def save_to_es(data, index_name, schema, state_key) -> None:
    """Сохранение данных в Elasticsearch"""
    es = ESSaver(es_config)
    es.create_index(schema, index_name)
    es.save_dataset(data, index_name, 100)
    State(JsonFileStorage('volumes/etl_state.json')).set_state(state_key, str(datetime.now()))


if __name__ == '__main__':
    while True:
        for task in tasks:
            save_to_es(load_from_postgres(task['class_loader'], task['state_key']), task['index_name'], task['schema'],
                       task['state_key'])

        sleep(15)

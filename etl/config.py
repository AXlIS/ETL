import os

from dotenv import load_dotenv

load_dotenv()

dsl = {
    'dbname': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'host': os.environ.get('DB_HOST', '127.0.0.1'),
    'port': os.environ.get('DB_PORT', 5432)
}

es_config = [{
    'scheme': os.environ.get('ELASTIC_SCHEME'),
    'host': os.environ.get('ELASTIC_HOST'),
    'port': int(os.environ.get('ELASTIC_PORT')),
}]

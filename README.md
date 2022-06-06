# ETL
 
Сервис для выгрузки данных по фильмам, актерам и жанрам из Postgresql в Elasticsearch.

## Основные компоненты системы
- PostgreSQL — реляционное хранилище данных.
- Elasticsearch — движок полнотекстового поиска.
- Admin — админка для работы с данными 

## Используемые технологии
- Django
- Elasticsearch
- PostgreSQL

## Запуск и наполнение базы данными
```shell
make full_upload
```
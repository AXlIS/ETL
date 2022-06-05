import logging

# Создаем объект-логгер с именем app.main:
logger = logging.getLogger('etl.main')

# Создаем объект форматирования:
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s ")

# Создаем файловый обработчик логирования (можно задать кодировку):
# Создаем файловый обработчик логирования (можно задать кодировку):
fh = logging.FileHandler("volumes/etl.main.log", encoding='utf-8')
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)

# Добавляем в логгер новый обработчик событий и устанавливаем уровень логирования
logger.addHandler(fh)
logger.setLevel(logging.INFO)
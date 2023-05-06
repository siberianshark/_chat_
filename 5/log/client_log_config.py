import logging
import os
from logging import handlers

log_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log')
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

log_formatter = logging.Formatter(
    '%(asctime)s %(levelname)s %(module)s %(message)s')

# Создание именованного логгера
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Создание обработчика лога, который будет записывать лог в файл
log_file = os.path.join(log_directory, 'client.log')
file_handler = logging.FileHandler(log_file)

# Настройка формата сообщения
file_handler.setFormatter(log_formatter)

# Добавление обработчика к логгеру
logger.addHandler(file_handler)

# Настройка ротации лог-файлов
if __name__ == '__main__':
    file_handler = handlers.TimedRotatingFileHandler(
        log_file, when='midnight', backupCount=8, encoding=None)
    file_handler.setFormatter(log_formatter)
    logger.addHandler(file_handler)
"""
    Конфигурационный файл
"""
# TODO перенести этот файл в tests
import os
from yarl import URL
# dotenv - это небольшой пакет, который считывает пары ключ-значение из файла .env,
# и загружает необходимые вашему приложению переменные окружения
from dotenv import load_dotenv

from src.const import EnvName

# находим путь абсолютный путь до src
# относительный путь работает нестабильно - если запускать скрипты из разных файлов
curr_dir = os.path.dirname(__file__) # путь до текущего файла /home/pcuser/PycharmProjects/school_testing/src
src_path = os.path.join(curr_dir, '..') # перемещяемся вверх на одну папку /home/pcuser/PycharmProjects/school_testing/src/..

# в зависимости от окружения загружаем нужный нам файл с .env
_ENVIRONMENT_NAME = os.getenv("ENVIRONMENT_NAME") or "development"
load_dotenv(f"{src_path}/env_folder/{_ENVIRONMENT_NAME}/.env")

# -------- SET VARIABLES from ENV ----------
# создание объекта URL
# в API_URL лежит http://127.0.0.1:5000/api
base_url = URL(os.getenv(EnvName.API_URL))  # BASE_URL - основной URL сервиса

if __name__ == "__main__":
    # для теста
    print(base_url)
    print(os.getcwd())

"""
    Конфигурационный файл
"""
# TODO перенести этот файл в tests
import os
from yarl import URL
from dotenv import load_dotenv

from src.const import EnvName

# в зависимости от окружения загружаем нужный нам файл с .env
_ENVIRONMENT_NAME = os.getenv("ENVIRONMENT_NAME") or "development"
load_dotenv(f"../env_folder/{_ENVIRONMENT_NAME}/.env")

# -------- SET VARIABLES from ENV ----------
base_url = URL(os.getenv(EnvName.API_URL))  # BASE_URL - основной URL сервиса

if __name__ == "__main__":
    # для теста
    print(base_url)
    print(os.getcwd())

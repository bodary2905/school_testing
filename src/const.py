"""
    Константы необходимые для работы сервиса
"""

from enum import auto
from strenum import StrEnum


class EnvName(StrEnum):
    """Названия ENV переменных в файле .env"""
    # base_url
    BASE_URL = auto()
    API_URL = auto()
    # db
    DB_NAME = auto()
    DB_USER = auto()
    DB_PASSWORD = auto()
    DB_HOST = auto()
    DB_PORT = auto()
    # user1 credentials
    USER1_NAME = auto()
    USER1_PASSWORD = auto()

"""
    API-пути для данной сущности
"""
from enum import Enum
from strenum import StrEnum

from src.config import base_url
from src.api_entity.api_path import VersionNumber
from src.api_entity.User import entity_name


class UserPath(StrEnum):
    """Локальные пути"""
    register = f"{entity_name}/register"
    login = f"{entity_name}/login"


class UserFullPath(Enum):
    """Полные пути"""
    register = base_url / VersionNumber.v1 / UserPath.register
    login = base_url / VersionNumber.v1 / UserPath.login


if __name__ == "__main__":
    # для теста
    print(UserFullPath.login.value)
    print(base_url)

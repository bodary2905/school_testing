"""
    API-пути для данной сущности
"""
from enum import Enum
from strenum import StrEnum

from src.config import base_url
from src.api_entity.api_path import ModuleName
from src.api_entity.User import entity_name

# TODO все переделать
class UserPath(StrEnum):
    """Локальные пути"""
    register = f"{entity_name}/register"
    confirmRegistration = f"{entity_name}/confirmRegistration"
    loginWithoutCaptcha = f"{entity_name}/loginWithoutCaptcha"
    loginToService = f"{entity_name}/loginToService"
    getUser = f"{entity_name}/getUser"
    getItems = f"{entity_name}/getItems"
    delete = f"{entity_name}/delete"


class UserFullPath(Enum):
    """Полные пути"""
    register = base_url / ModuleName.auth / UserPath.register
    confirmRegistration = base_url / ModuleName.auth / UserPath.confirmRegistration
    loginWithoutCaptcha = base_url / ModuleName.auth / UserPath.loginWithoutCaptcha
    loginToService = base_url / ModuleName.auth / UserPath.loginToService
    getUser = base_url / ModuleName.core / UserPath.getUser
    getItems = base_url / ModuleName.core / UserPath.getItems
    delete = base_url / ModuleName.core / UserPath.delete


if __name__ == "__main__":
    # для теста
    print(UserFullPath.getItems.value)

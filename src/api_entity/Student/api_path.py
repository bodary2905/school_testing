"""
    API-пути для данной сущности
"""
from enum import Enum
from strenum import StrEnum

from src.config import base_url
from src.api_entity.api_path import VersionNumber
from src.api_entity.Student import entity_name

class StudentPath(StrEnum):
    """Локальные пути"""
    create = f"{entity_name}"
    get = f"{entity_name}"
    getItems = f"{entity_name}"
    put = f"{entity_name}"
    delete = f"{entity_name}"
class StudentFullPath(Enum):
    """Полные пути"""
    create = base_url / VersionNumber.v1 / StudentPath.create
    get = base_url / VersionNumber.v1 / StudentPath.get
    getItems = base_url / VersionNumber.v1 / StudentPath.getItems
    put = base_url / VersionNumber.v1 / StudentPath.put
    delete = base_url / VersionNumber.v1 / StudentPath.delete

if __name__ == "__main__":
    # для теста
    print(StudentFullPath.create.value) # так как тип Enum для получения значения необходимо писать .get.value
    print(StudentFullPath.get.value)
    print(StudentFullPath.getItems.value)
    print(StudentFullPath.put.value)
    print(StudentFullPath.delete.value)


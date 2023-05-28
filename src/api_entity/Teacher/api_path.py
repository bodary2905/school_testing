"""
    API-пути для данной сущности
"""
from enum import Enum
from strenum import StrEnum

from src.config import base_url
from src.api_entity.api_path import VersionNumber
from src.api_entity.Teacher import entity_name

class TeacherPath(StrEnum):
    """Локальные пути"""
    create = f"{entity_name}"
    get = f"{entity_name}"
    getItems = f"{entity_name}"
    put = f"{entity_name}"
    delete = f"{entity_name}"
class TeacherFullPath(Enum):
    """Полные пути"""
    create = base_url / VersionNumber.v1 / TeacherPath.create
    get = base_url / VersionNumber.v1 / TeacherPath.get
    getItems = base_url / VersionNumber.v1 / TeacherPath.getItems
    put = base_url / VersionNumber.v1 / TeacherPath.put
    delete = base_url / VersionNumber.v1 / TeacherPath.delete

if __name__ == "__main__":
    # для теста
    print(TeacherFullPath.create.value)
    print(TeacherFullPath.get.value)
    print(TeacherFullPath.getItems.value)
    print(TeacherFullPath.put.value)
    print(TeacherFullPath.delete.value)


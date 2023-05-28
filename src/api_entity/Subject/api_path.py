"""
    API-пути для данной сущности
"""
from enum import Enum
from strenum import StrEnum

from src.config import base_url
from src.api_entity.api_path import VersionNumber
from src.api_entity.Subject import entity_name

class SubjectPath(StrEnum):
    """Локальные пути"""
    create = f"{entity_name}"
    get = f"{entity_name}"
    getItems = f"{entity_name}"
    put = f"{entity_name}"
    delete = f"{entity_name}"
class SubjectFullPath(Enum):
    """Полные пути"""
    create = base_url / VersionNumber.v1 / SubjectPath.create
    get = base_url / VersionNumber.v1 / SubjectPath.get
    getItems = base_url / VersionNumber.v1 / SubjectPath.getItems
    put = base_url / VersionNumber.v1 / SubjectPath.put
    delete = base_url / VersionNumber.v1 / SubjectPath.delete

if __name__ == "__main__":
    # для теста
    print(SubjectFullPath.create.value)
    print(SubjectFullPath.get.value)
    print(SubjectFullPath.getItems.value)
    print(SubjectFullPath.put.value)
    print(SubjectFullPath.delete.value)


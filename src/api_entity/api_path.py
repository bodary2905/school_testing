"""
    Базовые api-пути для всех api-сущностей
"""
from strenum import StrEnum
from enum import auto

# TODO переделать в VersionNumber
class ModuleName(StrEnum):
    """Название модуля"""
    auth = auto()
    core = auto()


if __name__ == "__main__":
    # для локального теста
    print(ModuleName.auth)

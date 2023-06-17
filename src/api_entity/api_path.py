"""
    Базовые api-пути для всех api-сущностей
"""
from strenum import StrEnum
from enum import auto


class VersionNumber(StrEnum):
    """Номер версии"""
    v1 = auto()


if __name__ == "__main__":
    # для локального теста
    print(VersionNumber.v1)

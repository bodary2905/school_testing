"""
    Базовые модели - для всех API сущностей
"""
from pydantic import BaseModel as PydanticBaseModel, Extra


class BaseModel(PydanticBaseModel):
    """Переопределяем BaseModel для глобального изменения настроек"""

    class Config:
        extra = Extra.ignore  # игнорировать лишние поля при создании модели

    def exclude_optional_dict(self, **kwargs):
        """Реализация опции exclude_optional - НЕ включать в dict НЕ определенные Optional поля"""
        return union(self.dict(**kwargs, exclude_unset=True), self.dict(**kwargs, exclude_none=True))


def union(source, destination):
    """Вспомогательная функция для реализация опции exclude_optional"""
    for key, value in source.items():
        if isinstance(value, dict):
            node = destination.setdefault(key, {})
            union(value, node)
        else:
            destination[key] = value

    return destination

"""
    Константы для API сущностей
"""
import jwt
import dpath
from dataclasses import dataclass
from pydantic.types import UUID4

from src.api_entity.api_path import ModuleName


@dataclass
class UserCredential:
    """Учетные данные для пользователей с различными ролями"""
    email: str
    password: str
    token: str = ""


if __name__ == "__main__":
    # для теста
    pass

"""
    Константы для API сущностей
"""
import dpath
from dataclasses import dataclass


@dataclass
class UserCredential:
    """Учетные данные для пользователей с различными ролями"""
    name: str
    password: str
    token: str = ""


if __name__ == "__main__":
    # для теста
    pass

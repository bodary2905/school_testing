"""
    Константы для API сущностей
"""
import dpath
from dataclasses import dataclass


@dataclass
class UserCredential:
    """Учетные данные для пользователей с различными ролями"""
    email: str
    password: str
    token: str = ""


if __name__ == "__main__":
    # для теста
    pass
    import os
    from src.const import EnvName
    import src.config


    class UserCredential1:
        def __init__(self, email, password, token=None):
            self.email = email
            self.password = password
            self.token = token


    user1_credential = UserCredential1(email="demo1", password="demo2")
    print(user1_credential.email)
    print(user1_credential.password)

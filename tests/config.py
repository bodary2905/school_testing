"""
    Конфигурационный файл
"""

import os

import src.config
from src.const import EnvName
from src.api_entity.const import UserCredential

# -------- CREDENTIAL ---------
# учетные данные для User1
# создаем экземпляр класса UserCredential
user1_credential = UserCredential(
    email=os.getenv(EnvName.USER1_EMAIL), # email = "eqywo@mailto.plus"
    password=os.getenv(EnvName.USER1_PASSWORD),
)


if __name__ == "__main__":
    # для теста

    print(user1_credential.email)

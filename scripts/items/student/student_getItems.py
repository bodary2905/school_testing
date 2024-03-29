import requests
import json
import random

from scripts.items.const import api_url

# открываем json-файл с токенами юзеров
with open("../user/json_files/tokens.json", "r") as file:
    # получаем словарь с токенами
    tokens = json.load(file)
    # получаем случайный токен из словаря tokens
    token = random.choice(list(tokens.values()))
    # формируем хэдере авторизации
    auth = {"Authorization": token}
    # отправляем pfgjc getItems и возвращаем всех студентов
    response = requests.get(f"{api_url}students", headers=auth)
    # проверяем статус код
    assert response.status_code == 200, "Wrong status_code during student_getItems"
    body = response.json()
    print(body)

if __name__ == "__main__":
    import os

    # получаем имя текущего .py файла по указанному пути
    filename = os.path.basename(__file__)
    # выводим сообщение об успехе
    print(f"{filename} worked success!")

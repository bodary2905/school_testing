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
    # отправляем pfgjc getItems и возвращаем все предметы
    response = requests.get(f"{api_url}subjects", headers=auth)
    # проверяем статус код
    assert response.status_code == 200, f"Wrong status_code during subject_getItems\nStatus code: {response.status_code}\nResponse: {response.text}"
    body = response.json()
    print(body)

if __name__ == "__main__":
    import os

    # получаем имя файла user_register.py по указанному пути
    filename = os.path.basename(__file__)
    # выводим сообщение об успехе
    print(f"{filename} worked success!")

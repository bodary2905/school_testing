import requests
import json
import random

from scripts.items.const import api_url

# создаем пустой список для записи в него id-в студентов из файла
subject_ids = []
# открываем json-файл, в котором хранятся id-ки созданных студентов
with open("json_files/subject_ids.json", "r") as file2:
    # получаем словарь с id-ми
    ids = json.load(file2)
    for id in ids.values():
        subject_ids.append(id)  # записываем id-ки студентов в список

# открываем json-файл с токенами юзеров
with open("../user/json_files/tokens.json", "r") as file:
    # получаем словарь с токенами
    tokens = json.load(file)
    # получаем случайный токен из словаря tokens
    token = random.choice(list(tokens.values()))
    # формируем хэдере авторизации
    auth = {"Authorization": token}
    # через цикл for просматриваем каждый предмет
    for subject_id in subject_ids:
        url = f"{api_url}subjects/{subject_id}"
        response = requests.get(url, headers=auth)
        # проверяем статус код
        assert response.status_code == 200, f"Wrong status_code during subject_get\nStatus code: {response.status_code}\nResponse: {response.text}"
        body = response.json()
        print(body)

if __name__ == "__main__":
    import os

    # получаем имя файла user_register.py по указанному пути
    filename = os.path.basename(__file__)
    # выводим сообщение об успехе
    print(f"{filename} worked success!")

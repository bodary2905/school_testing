import requests
import json
import random

from scripts.items.const import api_url

# создаем пустой список для записи в него id-в студентов из файла
teacher_ids = []
# открываем json-файл, в котором хранятся id-ки студентов
with open("json_files/teacher_ids.json", "r") as file2:
    # получаем словарь с id-ми
    ids = json.load(file2)
    for id in ids.values():
        teacher_ids.append(id)  # записываем id-ки студентов в список

# открываем json-файл с токенами
with open("../user/json_files/tokens.json", "r") as file:
    # получаем словарь с токенами
    tokens = json.load(file)
    # получаем случайный токен из словаря tokens
    token = random.choice(list(tokens.values()))
    # формируем хэдере авторизации
    auth = {"Authorization": token}
    # открываем json-файл с данными для изменения студентов
    with open("json_files/teachers_update.json", "r") as file:
        # получаем словарь с данными для изменения студентов
        teacher_update = json.load(file)
        # через цикл for изменяем студентов
        for teacher, teacher_id in zip(teacher_update.values(), teacher_ids):
            response = requests.put(f"{api_url}teachers/{teacher_id}", json=teacher, headers=auth)
            # проверяем статус код
            assert response.status_code == 200, f"Wrong status_code during teacher_update\nStatus code: {response.status_code}\nResponse: {response.text}"
            body = response.json()
            # сравниваем значения отправленные на сервер с полученными значениями
            assert teacher["first_name"] == body["first_name"], "request first_name is NOT equal to response first_name"
            assert teacher["last_name"] == body["last_name"], "request last_name is NOT equal to response last_name"

if __name__ == "__main__":
    import os

    # получаем имя файла user_register.py по указанному пути
    filename = os.path.basename(__file__)
    # выводим сообщение об успехе
    print(f"{filename} worked success!")

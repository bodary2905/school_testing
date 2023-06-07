"""
    Скрипты для ...
"""

import requests
import json
import random

from scripts.items.const import api_url

# создаем пустые списки для записи в них id-ки и email-в созданных юзеров
teacher_ids = []
email_addresses = []

# открываем json-файл с токенами
with open("../user/json_files/tokens.json", "r") as file:
    # получаем словарь с токенами
    tokens = json.load(file)
    # получаем случайный токен из словаря tokens
    token = random.choice(list(tokens.values()))
    # формируем хэдере авторизации
    auth = {"Authorization": token}
    # открываем json-файл со  студентами
    with open("json_files/teachers.json", "r") as file2:
        # получаем словарь с токенами
        teachers = json.load(file2)
        # через цикл for создаем студентов
        for teacher in teachers.values():
            response = requests.post(f"{api_url}teachers", json=teacher, headers=auth)
            assert response.status_code == 201, f"Wrong status_code during create_teacher\nStatus code:{response.status_code}\nResponse{response.text}"
            body = response.json()  # получаем ответ в виде json-объекта
            # сравниваем значения, отправленные на сервер и значения, полученные в ответе
            assert teacher["first_name"] == body["first_name"], "request first_name is NOT equal to response first_name"
            assert teacher["last_name"] == body["last_name"], "request last_name is NOT equal to response last_name"
            assert teacher["email_address"] == body[
                "email_address"], "request email_address is NOT equal to response email_address"
            # заполняем списки id-ми и email-ми студентов, полученными в ответе
            teacher_ids.append(body["staff_id"])
            email_addresses.append(body["email_address"])

# создаем пустой словарь для записи в него email-в и id-в студентов
teacher_id_dict = {}
# открываем пустой json-файл для записи email-в и id-в студентов
with open("json_files/teacher_ids.json", "w") as file:
    # через цикл for заполняем словарь teacher_id_dict
    for email_address, teacher_id in zip(email_addresses, teacher_ids):
        teacher_id_dict[email_address] = teacher_id  # заполняем словарь
    teacher_id_json = json.dumps(teacher_id_dict, indent=4)  # преобразуем словарь в json с отступом=4
    file.write(teacher_id_json)  # записываем в файл словарь json

if __name__ == "__main__":
    import os

    # получаем имя файла user_register.py по указанному пути
    filename = os.path.basename(__file__)
    # выводим сообщение об успехе
    print(f"{filename} worked success!")

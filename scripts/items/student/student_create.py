"""
    Скрипты для ...
"""

import requests
import json
import random

from scripts.items.const import api_url

# создаем пустые списки для записи в них id-ки и email-в созданных юзеров
student_ids = []
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
    with open("../json_files/students.json", "r") as file2:
        # получаем словарь с токенами
        students = json.load(file2)
        # через цикл for создаем студентов
        for student in students.values():
            response = requests.post(f"{api_url}students", json=student, headers=auth)
            assert response.status_code == 201, "Wrong status_code during create_student"
            body = response.json()  # получаем ответ в виде json-объекта
            # сравниваем значения, отправленные на сервер и значения, полученные в ответе
            assert student["first_name"] == body["first_name"], "request first_name is NOT equal to response first_name"
            assert student["last_name"] == body["last_name"], "request last_name is NOT equal to response last_name"
            assert student["email_address"] == body[
                "email_address"], "request email_address is NOT equal to response email_address"
            # заполняем списки id-ми и email-ми студентов, полученными в ответе
            student_ids.append(body["student_id"])
            email_addresses.append(body["email_address"])

# создаем пустой словарь для записи в него email-в и id-в студентов
student_id_dict = {}
# открываем пустой json-файл для записи email-в и id-в студентов
with open("../json_files/student_ids.json", "w") as file:
    # через цикл for заполняем словарь student_id_dict
    for email_address, student_id in zip(email_addresses, student_ids):
        student_id_dict[email_address] = student_id  # заполняем словарь
    student_id_json = json.dumps(student_id_dict, indent=4)  # преобразуем словарь в json с отступом=4
    file.write(student_id_json)  # записываем в файл словарь json

if __name__ == "__main__":
    import os

    # получаем имя файла user_register.py по указанному пути
    filename = os.path.basename(__file__)
    # выводим сообщение об успехе
    print(f"{filename} worked success!")

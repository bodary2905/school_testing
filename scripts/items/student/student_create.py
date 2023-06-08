"""
    Скрипты для ...
"""

import requests
import json
import random

from scripts.items.const import api_url

# создаем пустой список для записи id-в предметов
subjects_ids = []
# открываем json-файл с  id-ми предметов
with open("../subject/json_files/subject_ids.json", "r") as file:
    # получаем словарь с id-ми exbntktq
    ids = json.load(file)
    # с помощью цикла for записываем id-ки учителей
    for id in ids.values():
        subjects_ids.append(id)

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
    with open("json_files/students.json", "r") as file2:
        # получаем словарь с токенами
        students = json.load(file2)
        # через цикл for создаем студентов
        for student in students.values():
            # случайным образом формируем список из id-в предметов для дополнительных предметов
            random_subject_ids = random.sample(subjects_ids, random.randint(0, len(subjects_ids)))
            # переводим в строку random_subject_ids и записываем значение в дополнительные предметы
            student["minors"] = ", ".join(map(str, random_subject_ids))
            # случайным образом выбираем id-к для основного предмета
            student["major_id"] = random.choice(subjects_ids)
            # создаем студентов
            response = requests.post(f"{api_url}students", json=student, headers=auth)
            # проверяем статус код
            assert response.status_code == 201, "Wrong status_code during create_student"
            body = response.json()  # получаем ответ в виде json-объекта
            # сравниваем значения, отправленные на сервер и значения, полученные в ответе
            assert student["first_name"] == body["first_name"], "request first_name is NOT equal to response first_name"
            assert student["last_name"] == body["last_name"], "request last_name is NOT equal to response last_name"
            assert student["email_address"] == body[
                "email_address"], "request email_address is NOT equal to response email_address"
            assert student["major_id"] == body["major"][
                "subject_id"], "request major_id is NOT equal to response subject_id"
            # создаем пустой список с id-ми дополнительных предметов
            minor_ids = []
            # через цикл for собираем id-ки дополнительных предметов из ответа
            for minor in body["minors"]:
                minor_ids.append(minor["subject_id"])
            # сортируем и сравниваем отправленные и полученные дополнительные предметы
            random_subject_ids.sort()
            minor_ids.sort()
            assert random_subject_ids == minor_ids, "request minors is NOT equal to response minors"

            # заполняем списки id-ми и email-ми студентов, полученными в ответе
            student_ids.append(body["student_id"])
            email_addresses.append(body["email_address"])

# создаем пустой словарь для записи в него email-в и id-в студентов
student_id_dict = {}
# открываем пустой json-файл для записи email-в и id-в студентов
with open("json_files/student_ids.json", "w") as file:
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

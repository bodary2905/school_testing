"""
    Скрипты для ...
"""

import requests
import json
import random

from scripts.items.const import api_url

# создаем пустые списки для записи в них id-ков и name-в созданных предметов
names = []
subject_ids = []

# создаем пустой список для записи id-в учителей
teacher_ids = []
# открываем json-файл с  id-ми учиттилей
with open("../teacher/json_files/teacher_ids.json", "r") as file:
    # получаем словарь с id-ми exbntktq
    ids = json.load(file)
    # с помощью цикла for записываем id-ки учителей
    for id in ids.values():
        teacher_ids.append(id)
print(teacher_ids)

# открываем json-файл с токенами
with open("../user/json_files/tokens.json", "r") as file:
    # получаем словарь с токенами
    tokens = json.load(file)
    # получаем случайный токен из словаря tokens
    token = random.choice(list(tokens.values()))
    # формируем хэдере авторизации
    auth = {"Authorization": token}
    # открываем json-файл с предметами
    with open("json_files/subjects.json", "r") as file2:
        # получаем словарь с предметами
        subjects = json.load(file2)
        # через цикл for добавляем id-ки учителей в словарь с предметами и создаем предметы
        for subject, id in zip(subjects.values(), teacher_ids):
            subject["teacher_id"] = id
            print(subject)
            response = requests.post(f"{api_url}subjects", json=subject, headers=auth)
            assert response.status_code == 201, f"Wrong status_code during create_subject\nStatus code:{response.status_code}\nResponse{response.text}"
            body = response.json()  # получаем ответ в виде json-объекта
            # сравниваем значения, отправленные на сервер и значения, полученные в ответе
            assert subject["name"] == body["name"], "request name is NOT equal to response name"
            assert subject["description"] == body[
                "description"], "request description is NOT equal to response description"
            assert subject["teacher_id"] == body[
                "teacher"]["staff_id"], "request teacher_id is NOT equal to response staff_id"
            # заполняем списки id-ми и email-ми студентов, полученными в ответе
            names.append(body["name"])
            subject_ids.append(body["subject_id"])

# создаем пустой словарь для записи в него name-в и id-в предметов
subject_id_dict = {}
# открываем пустой json-файл для записи email-в и id-в студентов
with open("json_files/subject_ids.json", "w") as file:
    # через цикл for заполняем словарь teacher_id_dict
    for name, subject_id in zip(names, subject_ids):
        subject_id_dict[name] = subject_id  # заполняем словарь
    subject_id_json = json.dumps(subject_id_dict, indent=4)  # преобразуем словарь в json с отступом=4
    file.write(subject_id_json)  # записываем в файл словарь json

if __name__ == "__main__":
    import os

    # получаем имя файла user_register.py по указанному пути
    filename = os.path.basename(__file__)
    # выводим сообщение об успехе
    print(f"{filename} worked success!")

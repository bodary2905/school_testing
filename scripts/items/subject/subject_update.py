import requests
import json
import random

from scripts.items.const import api_url

# создаем пустой список для записи id-в учителей
teacher_ids = []
# открываем json-файл с  id-ми учиттилей
with open("../teacher/json_files/teacher_ids.json", "r") as file:
    # получаем словарь с id-ми exbntktq
    ids = json.load(file)
    # с помощью цикла for записываем id-ки учителей
    for id in ids.values():
        teacher_ids.append(id)

# создаем пустой список для записи в него id-в предметов из файла
subjects_ids = []
# открываем json-файл, в котором хранятся id-ки предметов
with open("json_files/subject_ids.json", "r") as file2:
    # получаем словарь с id-ми
    ids = json.load(file2)
    for id in ids.values():
        subjects_ids.append(id)  # записываем id-ки предметов в список

# открываем json-файл с токенами
with open("../user/json_files/tokens.json", "r") as file:
    # получаем словарь с токенами
    tokens = json.load(file)
    # получаем случайный токен из словаря tokens
    token = random.choice(list(tokens.values()))
    # формируем хэдере авторизации
    auth = {"Authorization": token}
    # открываем json-файл с данными для изменения предметов
    with open("json_files/subjects_update.json", "r") as file:
        # получаем словарь с данными для изменения предметов
        subject_update = json.load(file)
        # через цикл for в словарь с предметами добавляем id-ки учитилей и изменяем предметы
        for subject, subject_id in zip(subject_update.values(), subjects_ids):
            subject["teacher_id"] = random.choice(teacher_ids)
            response = requests.put(f"{api_url}subjects/{subject_id}", json=subject, headers=auth)
            # проверяем статус код
            assert response.status_code == 200, f"Wrong status_code during subject_update\nStatus code: {response.status_code}\nResponse: {response.text}"
            body = response.json()
            # сравниваем значения отправленные на сервер с полученными значениями
            assert subject["name"] == body["name"], "request name is NOT equal to response name"
            assert subject["description"] == body[
                "description"], "request description is NOT equal to response description"
            assert subject["teacher_id"] == body["teacher"][
                "staff_id"], "request teacher_id is NOT equal to response staff_id"

if __name__ == "__main__":
    import os

    # получаем имя файла user_register.py по указанному пути
    filename = os.path.basename(__file__)
    # выводим сообщение об успехе
    print(f"{filename} worked success!")

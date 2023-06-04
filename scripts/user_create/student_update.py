import requests
import json
import random

api_url = "http://127.0.0.1:5000/api/v1/students"

student_ids = []
with open("json_files/student_ids.json", "r") as file2:
    ids = json.load(file2)
    for id in ids.values():
        student_ids.append(id)  # записываем id-ки студентов в список

with open("json_files/tokens.json", "r") as file:
    # получаем словарь с токенами
    tokens = json.load(file)
    # получаем случайный токен из словаря tokens
    token = random.choice(list(tokens.values()))
    # формируем хэдере авторизации
    auth = {"Authorization": token}
    with open("json_files/students_update.json", "r") as file:
        students_update = json.load(file)
        for student, student_id in zip(students_update.values(), student_ids):
            response = requests.put(f"{api_url}/{student_id}", json=student, headers=auth)
            # проверяем статус код
            assert response.status_code == 200, "Wrong status_code during student_update"
            body = response.json()
            # сравниваем значения отправленные на сервер с полученными значениями
            assert student["first_name"] == body["first_name"], "request first_name is NOT equal to response first_name"
            assert student["last_name"] == body["last_name"], "request last_name is NOT equal to response last_name"

if __name__ == "__main__":
    import os

    filename = os.path.basename(__file__)
    print(f"{filename} worked success!")

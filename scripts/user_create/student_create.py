import requests
import json
import random

api_url = "http://127.0.0.1:5000/api/v1/students"

student_ids = []
email_addresses = []
with open("tokens.json", "r") as file:
    # получаем словарь с токенами
    tokens = json.load(file)
    # получаем случайный токен из словаря tokens
    token = random.choice(list(tokens.values()))
    # формируем хэдере авторизации
    auth = {"Authorization": token}
    with open("students.json", "r") as file2:
        students = json.load(file2)
        for student in students.values():
            response = requests.post(api_url, json=student, headers=auth)
            assert response.status_code == 201, "Wrong status_code during create_student"
            body = response.json()
            assert student["first_name"] == body["first_name"], "request first_name is NOT equal to response first_name"
            assert student["last_name"] == body["last_name"], "request last_name is NOT equal to response last_name"
            assert student["email_address"] == body[
                "email_address"], "request email_address is NOT equal to response email_address"
            student_ids.append(body["student_id"])
            email_addresses.append(body["email_address"])

student_id_dict = {}
with open("student_ids.json", "w") as file:
    for email_address, student_id in zip(email_addresses, student_ids):
        student_id_dict[email_address] = student_id  # заполняем словарь
    student_id_json = json.dumps(student_id_dict, indent=4)  # преобразуем словарь в json с отступом=4
    file.write(student_id_json)  # записываем в файл словарь json

if __name__ == "__main__":
    pass

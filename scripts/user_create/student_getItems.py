import requests
import json
import random

api_url = "http://127.0.0.1:5000/api/v1/students"

with open("json_files/tokens.json", "r") as file:
    # получаем словарь с токенами
    tokens = json.load(file)
    # получаем случайный токен из словаря tokens
    token = random.choice(list(tokens.values()))
    # формируем хэдере авторизации
    auth = {"Authorization": token}
    with open("json_files/students_update.json", "r") as file:
        response = requests.get(api_url, headers=auth)
        # проверяем статус код
        assert response.status_code == 200, "Wrong status_code during student_getItems"
        body = response.json()
        print(body)

if __name__ == "__main__":
    import os

    filename = os.path.basename(__file__)
    print(f"{filename} worked success!")

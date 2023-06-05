import requests
import json

from const import api_url_auth

# открываем json-файл с юзерами
with open("json_files/users.json", "r") as file:
    # получаем словарь с юзерами
    users = json.load(file)
    # через цикл for регистрируем user-ов
    for user in users.values():
        response = requests.post(f"{api_url_auth}register", json=user)
        assert response.status_code == 201, "Wrong status_code during register"

if __name__ == "__main__":
    import os

    # получаем имя файла user_register.py по указанному пути
    filename = os.path.basename(__file__)
    # выводим сообщение об успехе
    print(f"{filename} worked success!")

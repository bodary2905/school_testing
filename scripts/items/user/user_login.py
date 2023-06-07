import requests
import json

from const import api_url_auth

# создаем пустые списки для записи в них имен и токенов юзеров
usernames = []
tokens = []

# открываем json-файл с юзерами
with open("json_files/users.json", "r") as file:
    # получаем словарь с юзерами
    users = json.load(file)
    # через цикл for логинем items-ов
    for user in users.values():
        response = requests.post(f"{api_url_auth}login", json=user)
        assert response.status_code == 200, "Wrong status_code during login"
        body = response.json()  # получаем ответ в виде json объекта
        tokens.append(f"{body['token']}")  # добавляем токены в список
        usernames.append(user["username"])  # добавляем юзеров в список

# создаем пустой словарь для записи в него токенов юзеров после логина
token_dict = {}
# открываем пустой json-файл для записи имен и токенов юзеров
with open("json_files/tokens.json", "w") as file:
    # через цикл for заполняем словарь token_dict
    for username, token in zip(usernames, tokens):  # функция zip объединяет элементы из двух списков
        token_dict[username] = token  # заполняем словарь
    token_json = json.dumps(token_dict, indent=4)  # преобразуем словарь в json с отступом=4
    file.write(token_json)  # записываем в файл словарь json с токенами юзеров

if __name__ == "__main__":
    import os

    # получаем имя файла user_login.py по указанному пути
    filename = os.path.basename(__file__)
    # выводим сообщение об успехе
    print(f"{filename} worked success!")

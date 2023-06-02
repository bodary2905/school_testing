import requests
import json

api_url = "http://127.0.0.1:5000/api/v1/auth/login"

usernames = []
tokens = []

# открываем json-файл
with open("users.json", "r") as file:
    # получаем словарь с юзерами
    users = json.load(file)
    # через цикл for логинем user-ов
    for user in users.values():
        response = requests.post(api_url, json=user)
        assert response.status_code == 200, "Wrong status_code during login"
        body = response.json()  # получаем ответ в виде json
        tokens.append(f"{body['token']}")  # добавляем токены в список
        usernames.append(user["username"])  # добавляем юзеров в список

token_dict = {}
with open("tokens.json", "w") as file:
    for username, token in zip(usernames, tokens):
        token_dict[username] = token  # заполняем словарь
    token_json = json.dumps(token_dict, indent=4)  # преобразуем словарь в json с отступом=4
    file.write(token_json)  # записываем в файл словарь json

if __name__ == "__main__":
    import os

    filename = os.path.basename(__file__)
    print(f"{filename} worked success!")

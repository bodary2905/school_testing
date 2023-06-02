import requests
import json

api_url = "http://127.0.0.1:5000/api/v1/auth/register"
# открываем json-файл
file = open("users.json")
# получаем словарь с юзерами
users = json.load(file)

# через цикл for создаем user-ов
for user in users:
    response = requests.post(api_url, json=users[user])
    assert response.status_code == 201, "Wrong status_code during register"

if __name__ == "__main__":
    pass

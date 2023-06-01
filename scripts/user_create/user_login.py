import requests
import os

# a = os.getcwd()
# b = os.path.dirname(a)
# # c = os.path.join(os.getcwd(), "user_create", "users.txt")
# d = os.path.join(b, "user_create", "users.txt")
#
# print(a)
# print(b)
# # print(f"{c}")
# print(d)

api_url = "http://127.0.0.1:5000/api/v1/auth/login"

usernames = []
tokens = []

# with open(f"{d}") as file:
with open("users.txt", 'r') as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        line_split = line.split(",")
        username = line_split[0].strip()
        password = line_split[1].strip()
        body_request = {
            "username": username,
            "password": password
        }

        response_login = requests.post(api_url, json=body_request)  # получаем объект response
        assert response_login.status_code == 200, "Wrong status_code during login"
        body_response_login = response_login.json()  # получаем ответ в виде json
        tokens.append(f"{body_response_login['token']}")
        usernames.append(username)

with open("tokens.txt", "w") as file:
    for username, token in zip(usernames, tokens):
        file.write(f"{username}: {token}\n")

print(tokens)

if __name__ == "__main__":
    pass

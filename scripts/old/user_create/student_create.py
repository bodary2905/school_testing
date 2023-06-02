import requests
import json

api_url = "http://127.0.0.1:5000/api/v1/auth/students"

file = open("students.json")
dict_1 = json.load(file)  # возвращаем словарь

for student in dict_1:
    body = dict_1[student]  # получаем body для каждого студента

# print(dict_2)
# for i in _dict:
#     v = _dict[i]
#     print(v)
# file.close()

if __name__ == "__main__":
    pass

# with open("students.json", 'r') as file:
#     lines = file.readlines()
#     for line in lines:
#         line = line.strip()  # удаляем пробелы вначале и вконце
#         line_split = line.split(":")
#         username = line_split[0].strip()
#         password = line_split[1].strip()
#         body_request = {
#             "username": username,
#             "password": password
#         }
#
#         response_login = requests.post(api_url, json=body_request)  # получаем объект response
#         assert response_login.status_code == 200, "Wrong status_code during login"
#         body_response_login = response_login.json()  # получаем ответ в виде json
#         tokens.append(f"{body_response_login['token']}")
#         usernames.append(username)

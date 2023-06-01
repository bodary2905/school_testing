import requests

api_url = "http://127.0.0.1:5000/api/v1/auth/register"

with open("users.txt") as file:
    lines = file.readlines()
    for line in lines:
        line = line.strip()
        line_split = line.split(",")
        body_request = {
            "username": line_split[0].strip(),
            "password": line_split[1].strip()
        }
        response_register = requests.post(api_url, json=body_request)  # получаем объект response
        assert response_register.status_code == 201, "Wrong status_code during register"
        body_response_register = response_register.json()  # получаем ответ в виде json

if __name__ == "__main__":
    pass

import requests
import json

from const import api_url_auth
from src.db_client import create_connection, execute_read_query
from src import config
import os

# открываем json-файл с юзерами
with open("json_files/users.json", "r") as file:
    # получаем словарь с юзерами
    users = json.load(file)
    # через цикл for регистрируем items-ов
    for user in users.values():
        response = requests.post(f"{api_url_auth}register", json=user)
        assert response.status_code == 201, "Wrong status_code during register"
        db_credential = (
            os.getenv("DB_NAME"),
            os.getenv("DB_USER"),
            os.getenv("DB_PASSWORD"),
            os.getenv("DB_HOST"),
            int(os.getenv("DB_PORT"))
        )
        connection = create_connection(*db_credential)
        connection.set_session(readonly=True, autocommit=True)
        user_for_select = user["username"]
        select_user = f"select * from users where username = '{user_for_select}'"
        result = execute_read_query(connection, select_user)
        print(f"{user_for_select} there is in table users")
        connection.close()

if __name__ == "__main__":
    # получаем имя файла user_register.py по указанному пути
    filename = os.path.basename(__file__)
    # выводим сообщение об успехе
    print(f"{filename} worked success!")

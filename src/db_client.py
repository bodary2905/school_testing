"""
    Клиент для подключения к DB Postgress
"""

import psycopg2
from psycopg2 import OperationalError

from src.const import EnvName


def create_connection(db_name, db_user, db_password, db_host, db_port):
    """Создаем connection к Postgress"""
    connection = None
    # пытаемся подключиться к бд
    # TODO отрефакторить
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        # TODO подумать нужно ли пробрасывать ошибку дальше
        print(f"The error '{e}' occurred")
    return connection


# Создадим функцию, которая возвращает результат запроса
def execute_read_query(connection, query):
    """Послылаем SQL запрос и ждем ответ от БД"""
    try:
        with connection:
            with connection.cursor() as cursor:  # cursor - класс для взаимодействия с бд
                # С помощью метода execute объекта cursor
                # можно выполнить любую операцию или запрос к базе данных
                cursor.execute(query)
                result = cursor.fetchall()  # получаем результат запроса с помощью fetchall()
                return result
    except Exception as e:
        # TODO подумать нужно ли пробрасывать ошибку дальше
        print(f"The error '{e}' occurred")


# Создадим функцию БЕЗ возвращения результата запроса
def execute_query(connection, query):
    """Послылаем SQL запрос и НЕ ждем ответ от БД"""
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
    except Exception as e:
        # TODO подумать нужно ли пробрасывать ошибку дальше
        print(f"The error '{e}' occurred")


if __name__ == "__main__":
    # для теста
    import os
    from src import config

    db_credential = (
        os.getenv(EnvName.DB_NAME),
        os.getenv(EnvName.DB_USER),
        os.getenv(EnvName.DB_PASSWORD),
        os.getenv(EnvName.DB_HOST),
        int(os.getenv(EnvName.DB_PORT))
    )
    connection = create_connection(*db_credential)
    connection.set_session(readonly=False, autocommit=True)
    # delete_student = "delete from students where email_address = 'student_01@mail.ru'"
    # delete_students = "delete from students"
    # result = execute_query(connection, delete_students)
    select_students = "select * from students"
    result = execute_read_query(connection, select_students)
    print(result)
    # select_users = "SELECT * FROM users"
    # result = execute_read_query(connection, select_users)
    # print(result[3])
    connection.close()

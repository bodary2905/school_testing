"""
    Клиент для подключения к DB Postgress
"""

import psycopg2
from psycopg2 import OperationalError


def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
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
        print(f"The error '{e}' occurred")
    return connection


def execute_read_query(connection, query):
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                return result
    except Exception as e:
        print(f"The error '{e}' occurred")


def execute_query(connection, query):
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
    except Exception as e:
        print(f"The error '{e}' occurred")


if __name__ == "__main__":
    import os
    from src import config

    db_credential = (
        os.getenv("DB_NAME"),
        os.getenv("DB_USER"),
        os.getenv("DB_PASSWORD"),
        os.getenv("DB_HOST"),
        int(os.getenv("DB_PORT"))
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

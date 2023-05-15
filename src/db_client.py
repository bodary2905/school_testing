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


if __name__ == "__main__":
    import os
    from src import config
    from src.const import EnvName

    db_credential = (
        os.getenv(EnvName.DB_NAME1),
        os.getenv(EnvName.DB_USER),
        os.getenv(EnvName.DB_PASSWORD),
        os.getenv(EnvName.DB_HOST),
        int(os.getenv(EnvName.DB_PORT))
    )
    connection = create_connection(*db_credential)
    connection.set_session(readonly=True, autocommit=True)
    select_users = "SELECT * FROM customers"
    result = execute_read_query(connection, select_users)
    print(result[3])
    connection.close()

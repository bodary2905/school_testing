from src.db_client import create_connection, execute_query

items = [
    "users",
    "students",
    "person",
    "teachers",
    "subjects",
    "student_subject"
]

if __name__ == "__main__":
    import os
    # для всех скриптов с os.getenv делаем импорт конфигов
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

    for item in items:
        delete_sql = f"delete from {item}"
        result = execute_query(connection, delete_sql)
        assert result is None, f"Check table {item} error delete"

    connection.close()

    # получаем имя файла user_register.py по указанному пути
    filename = os.path.basename(__file__)
    # выводим сообщение об успехе
    print(f"{filename} worked success!")

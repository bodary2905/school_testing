# Автотесты для приложения [School App and API](https://github.com/bodary2905/flask-school-app-and-api)

В данном репозитории находятся пример реализации backend-автотестов на **Python**. Текущий результат не является
финальным,
поэтому возможны некоторые изменения. Документации тоже пока нет - все в процессе)

Автотесты написаны с помощью "самописного" фрэймворка реализованного на основе библиотек `pydantic`,
`pydantic-factories`, `faker`, `requests`. Для управления библиотеками и виртуальным окружением используется `poetry`.
Для запуска тестов используется `pytest`

Пока нет подробной документации, можно посмотреть следующие вещи:

1. [Код фрэймворка](src) и [реализация оберток над API-сущностями](src/api_entity) для приложения **School App and API**
2. [Некоторое подобие чек-листа](tests/CRUD_items.md) для проверки CRUD для каждой API-сущности
3. [Некоторое подобие чек-листа](tests/scenario_for_items.md) для проверки бизнес-сценариев
4. Сами тесты лежат в папке [tests](tests). Для каждой API-сущности - своя папка
5. В [CONTRIBUTING.MD](CONTRIBUTING.md) - будет написано как развернуть проект, запустить тесты

"""
    Базовые настройки фабрик для генерации request body по pydantic моделям
"""
from faker import Faker

# настраиваем кастомный faker
faker = Faker("ru-RU")


# # для debug-а настраиваем const random seed
# Faker.seed(5)
# ModelFactory.seed_random = 5


class BaseParams:
    """Базовая настройки для всех фабрик"""
    __faker__ = faker
    # для Optional полей - будет сгенерировано значение
    __allow_none_optionals__ = False
    # BaseFactory - фабрика по умолчанию
    __auto_register__ = True

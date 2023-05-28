import json
from pydantic.types import ClassVar
from pydantic_factories import ModelFactory, Ignore, Use, Require

from src.api_entity import schema_func
from src.api_entity.Student.model import StudentModel_create_for_factory, StudentModel_update_for_factory
from src.api_entity.factory import BaseParams, faker

class StudentFactory_create(BaseParams, ModelFactory):
    """Базовая фабрика - для CREATE запроса и для сравнения"""
    __model__ = StudentModel_create_for_factory
    schema: ClassVar[dict] = StudentModel_create_for_factory.schema()

    # поля
    major_id = Require()
    minors = Require()

    # генерируем данные с помощью faker
    @classmethod
    def first_name(cls) -> str:
        # получаем ограничения для поля из json-схемы
        max_length = schema_func.get_field_maxLength("first_name", cls.schema)
        return cls.__faker__.first_name()[:max_length]
    @classmethod
    def last_name(cls) -> str:
        # получаем ограничения для поля из json-схемы
        max_length = schema_func.get_field_maxLength("last_name", cls.schema)
        return cls.__faker__.last_name()[:max_length]
    @classmethod
    def email_address(cls) -> str:
        # получаем ограничения для поля из json-схемы
        return cls.__faker__.unique.email()
class StudentFactory_update(BaseParams, ModelFactory):
    __model__ = StudentModel_update_for_factory
    schema: ClassVar[dict] = StudentModel_update_for_factory.schema()
    @classmethod
    def first_name(cls) -> str:
        # получаем ограничения для поля из json-схемы
        max_length = schema_func.get_field_maxLength("first_name", cls.schema)
        return cls.__faker__.first_name()[:max_length]
    @classmethod
    def last_name(cls) -> str:
        # получаем ограничения для поля из json-схемы
        max_length = schema_func.get_field_maxLength("last_name", cls.schema)
        return cls.__faker__.last_name()[:max_length]

if __name__ == "__main__":
    # для теста
    student_1 = StudentFactory_create.build(major_id="SB12", minors="SB2")
    print(student_1.dict())
    student_1_upd = StudentFactory_update.build(major_id="SB3", minors="SB4")
    print(student_1_upd.dict())



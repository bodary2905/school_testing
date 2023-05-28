import json
from pydantic.types import ClassVar
from pydantic_factories import ModelFactory, Ignore, Use, Require

from src.api_entity import schema_func
from src.api_entity.Teacher.model import TeacherModel_create_for_factory, TeacherModel_update_for_factory
from src.api_entity.factory import BaseParams, faker

class TeacherFactory_create(BaseParams, ModelFactory):
    """Базовая фабрика - для CREATE запроса и для сравнения"""
    __model__ = TeacherModel_create_for_factory
    schema: ClassVar[dict] = TeacherModel_create_for_factory.schema()

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
class TeacherFactory_update(BaseParams, ModelFactory):
    __model__ = TeacherModel_update_for_factory
    schema: ClassVar[dict] = TeacherModel_update_for_factory.schema()
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
    teacher_1 = TeacherFactory_create.build(teacher_id="TC12")
    print(teacher_1.dict())
    teacher_1_upd = TeacherFactory_update.build(teacher_id="TC13")
    print(teacher_1_upd.dict())



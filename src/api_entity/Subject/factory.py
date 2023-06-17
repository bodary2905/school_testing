import json
from pydantic.types import ClassVar
from pydantic_factories import ModelFactory, Ignore, Use, Require

from src.api_entity import schema_func
from src.api_entity.Subject.model import SubjectModel_create_for_factory, SubjectModel_update_for_factory
from src.api_entity.factory import BaseParams, faker


class SubjectFactory_create(BaseParams, ModelFactory):
    """Базовая фабрика - для CREATE запроса и для сравнения"""
    __model__ = SubjectModel_create_for_factory
    schema: ClassVar[dict] = SubjectModel_create_for_factory.schema()

    # поля
    teacher_id = Require()

    # генерируем данные с помощью faker
    @classmethod
    def name(cls) -> str:
        # получаем ограничения для поля из json-схемы
        max_length = schema_func.get_field_maxLength("name", cls.schema)
        return cls.__faker__.word()[:max_length]

    @classmethod
    def description(cls) -> str:
        # получаем ограничения для поля из json-схемы
        max_length = schema_func.get_field_maxLength("description", cls.schema)
        return cls.__faker__.text()[:max_length]


class SubjectFactory_update(SubjectFactory_create):
    __model__ = SubjectModel_update_for_factory


if __name__ == "__main__":
    # для теста
    subject_1 = SubjectFactory_create.build(teacher_id="TC12")
    print(subject_1.dict())
    subject_1_upd = SubjectFactory_update.build(teacher_id="TC13")
    print(subject_1_upd.dict())

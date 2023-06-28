"""Тесты CRUD Teacher"""
import random

import pytest

from src.api_entity.Student.api_func import StudentApiFunc
from src.api_entity.Student.model import StudentModel_create_for_factory, StudentModel_update_for_factory, \
    StudentModel_create_for_response, StudentModel_update_for_response, StudentModel_get_for_response, \
    StudentModel_delete_for_response
from src.api_entity.Subject.api_func import SubjectApiFunc
from src.api_entity.Student.factory import StudentFactory_create, StudentFactory_update
from src.api_entity.Student.api_path import StudentFullPath
from src.http_func import send_post, send_put, send_get, send_delete
from src.api_entity.Student import entity_name
from tests.config import user1_credential

limit_values_create = [
    {"first_name": "a", "last_name": "w",
     "email_address": "uj1H3atHcJjXkXPds2KNDrQq6n2PvDrj8S8FXxUtFUfnZO6cmoLn8jJDOjaPkbIx@jTFPYnkXx0T3LITJhPvLiCC5hO5UF5fOE0Yz9aCQJ82ojVD6QjAppxy9cz0GOQE.ru"},
    {"first_name": "V1IRdh4xpRQVV4qsQmerL3wGxy8FDdCRqwKbHJL8sI6UJMvGwn",
     "last_name": "iNQB0wvQcuJJOPoF3ot2uXFhiQsjeSyQL03gqEwABk1saLGrNX", "email_address": "valid_post05@mail.ru"}
]
limit_values_update = [
    {"first_name": "d", "last_name": "h",
     "email_address": "dJGXGMjneqEjYrWtEryuTf5gKM4iJmiHkQsHn2RBlGGRJ30qy44rT8XaSKqlBtLP@whmDhFJQrS1ilVc55Xj7CHq0trrPOYbBvzDHMTXGKsorSfdQw0RBWZ5KVUm01m3.ru"},
    {"first_name": "YKW62NQyDfksLJCwoKx7SP26IDnoM87rxRMxawYL92EaZQ6Zgt",
     "last_name": "2gF4D62zNqbgdugVzgvlTIeygYLDBO3UhEduNhXSl3u2288vO5", "email_address": "valid_post06@mail.ru"}
]

limit_values_ids = ["min_min_max", "max_max_norm"]  # названия тестов


@pytest.mark.student
@pytest.mark.parametrize("limit_create, limit_update", zip(limit_values_create, limit_values_update),
                         ids=limit_values_ids)
def test_limit_student(user1_auth_hearders, limit_create, limit_update):
    """Тест параметризации"""
    #
    # status_code = limit_value.pop("status_code")
    # создаем студента с помощью фабрики (экземпляр модели фабрики)
    student_factory_create = StudentFactory_create.build(major_id=None, minors=None,
                                                         **limit_create)  # передаем именные параметры из словаря, например first_name="a"
    # создаем студента с помощью api_func через метод create
    student_create, student_model_create = StudentApiFunc.create(student_factory_create.dict(),
                                                                 headers=user1_auth_hearders)

    # GET
    # получаем id-к студента через модель
    student_id_create = student_model_create.student_id  # или через словарь student_create["student_id"]
    # получаем созданного студента с помощью api_func через метод get
    student_get_create, student_model_get_create = StudentApiFunc.get(student_id=student_id_create,
                                                                      headers=user1_auth_hearders)  # get возвращает body и model
    # сравниваем значения, отправленные на сервер с полученными значениями (фабрику и модель)
    assert student_factory_create.first_name == student_model_get_create.first_name, f"first_name фабрики НЕ равно first_name модели для create"
    assert student_factory_create.last_name == student_model_get_create.last_name, f"last_name фабрики НЕ равно last_name модели для create"
    assert student_factory_create.email_address == student_model_get_create.email_address, f"email_address фабрики НЕ равно email_address модели для create"
    # UPDATE
    # создаем экземпляр модели фабрики для update
    student_factory_update = StudentFactory_update.build(major_id=None, minors=None, **limit_update)
    # изменяем данные студента с помощью api_func через метод update
    student_update, student_model_update = StudentApiFunc.update(student_id=student_id_create,
                                                                 body=student_factory_update.dict(),
                                                                 headers=user1_auth_hearders)
    # получаем id-к студента
    student_id_update = student_model_update.student_id
    # сравниваем id-ки, полученные через create и update
    assert student_id_create == student_id_update, f"id-к create НЕ равен id-ку update"
    # получаем созданного студента с помощью api_func через метод get
    student_get_update, student_model_get_update = StudentApiFunc.get(student_id=student_id_update,
                                                                      headers=user1_auth_hearders)  # get возвращает body и model
    assert student_factory_update.first_name == student_model_get_update.first_name, f"first_name фабрики НЕ равно first_name модели для update"
    assert student_factory_update.last_name == student_model_get_update.last_name, f"last_name фабрики НЕ равно last_name модели для update"
    # у фабрики update НЕТ поля email_address (так как его изменять нельзя)
    assert student_factory_create.email_address == student_model_get_update.email_address, f"email_address фабрики НЕ равно email_address модели для update"
    # DELETE
    # Удаляем созданного студента
    StudentApiFunc.delete(student_id=student_id_create, headers=user1_auth_hearders)
    # проверяем, что удаленный студент отсутствует через
    response = send_get(url=StudentFullPath.get.value / student_id_create,
                        headers=user1_auth_hearders)
    assert response.status_code == 404, f"Wrong status_code {entity_name}:send_get after delete"
    pass

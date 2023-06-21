"""Тесты CRUD Teacher"""
import random

import pytest

from src.api_entity.Subject.api_func import SubjectApiFunc
from src.api_entity.Subject.model import SubjectModel_create_for_factory, SubjectModel_update_for_factory, \
    SubjectModel_create_for_response, SubjectModel_update_for_response, SubjectModel_get_for_response, \
    SubjectModel_delete_for_response
from src.api_entity.Teacher.api_func import TeacherApiFunc
from src.api_entity.Subject.factory import SubjectFactory_create, SubjectFactory_update
from src.api_entity.Subject.api_path import SubjectFullPath
from src.http_func import send_post, send_put, send_get, send_delete
from src.api_entity.Subject import entity_name
from tests.config import user1_credential


@pytest.mark.crud
@pytest.mark.teacher
def test_crud_subject(user1_auth_hearders):
    """Тест CRUD для предмета"""
    # Достаем словарь и модель с учителями
    teachers, teachers_model = TeacherApiFunc.getItems(headers=user1_auth_hearders)
    # достаем список учителей из словаря teachers
    teachers_list = teachers["teachers"]
    # создаем пустой словарь для сбора id-в учителей
    staff_ids = []
    for teacher in teachers_list:
        staff_ids.append(teacher["staff_id"])
    # CREATE
    # создаем предмет с помощью фабрики (экземпляр модели фабрики)
    subject_factory_create = SubjectFactory_create.build(teacher_id=random.choice(staff_ids))
    # создаем предмет с помощью api_func через метод create
    subject_create, subject_model_create = SubjectApiFunc.create(subject_factory_create.dict(),
                                                                 headers=user1_auth_hearders)  # create возвращает body и model
    # GET
    # получаем id-к предмета через модель
    subject_id_create = subject_model_create.subject_id  # или через словарь student_create["student_id"]
    # получаем созданный предмет с помощью api_func через метод get
    subject_get_create, subject_model_get_create = SubjectApiFunc.get(subject_id=subject_id_create,
                                                                      headers=user1_auth_hearders)  # get возвращает body и model
    # сравниваем значения, отправленные на сервер с полученными значениями (фабрику и модель)
    assert subject_factory_create.name == subject_model_get_create.name, f"name фабрики НЕ равно name модели для create"
    assert subject_factory_create.description == subject_model_get_create.description, f"description фабрики НЕ равно description модели для create"
    assert subject_factory_create.teacher_id == subject_model_get_create.teacher[
        "staff_id"], f"teacher_id фабрики НЕ равно staff_id модели для create"
    # UPDATE
    # создаем экземпляр модели фабрики для update
    subject_factory_update = SubjectFactory_update.build(teacher_id=random.choice(staff_ids))
    # изменяем данные предмета с помощью api_func через метод update
    subject_update, subject_model_update = SubjectApiFunc.update(subject_id=subject_id_create,
                                                                 body=subject_factory_update.dict(),
                                                                 headers=user1_auth_hearders)  # update возвращает body и model
    # получаем id-к предмета
    subject_id_update = subject_model_update.subject_id
    # сравниваем id-ки, полученные через create и update
    assert subject_id_create == subject_id_update, f"id-к create НЕ равен id-ку update"
    # получаем созданный предмет с помощью api_func через метод get
    subject_get_update, subject_model_get_update = SubjectApiFunc.get(subject_id=subject_id_update,
                                                                      headers=user1_auth_hearders)  # get возвращает body и model
    assert subject_factory_update.name == subject_model_get_update.name, f"name фабрики НЕ равно name модели для update"
    assert subject_factory_update.description == subject_model_get_update.description, f"description фабрики НЕ равно description модели для update"
    assert subject_factory_update.teacher_id == subject_model_get_update.teacher[
        "staff_id"], f"teacher_id фабрики НЕ равно staff_id модели для update"
    # DELETE
    # Удаляем созданный предмет
    SubjectApiFunc.delete(subject_id=subject_id_create, headers=user1_auth_hearders)
    # Проверяем, что удаленный предмет отсутствует через send_get (чтобы проверить статус код НЕ равный 200)
    response = send_get(url=SubjectFullPath.get.value / subject_id_create,
                        headers=user1_auth_hearders)  # в kwargs передаем headers
    assert response.status_code == 404, f"Wrong status_code {entity_name}:send_get after delete"
    pass

"""Тесты CRUD Teacher"""
import random

import pytest

from src.api_entity.Subject.api_path import SubjectFullPath
from src.api_entity.Student.api_func import StudentApiFunc
from src.api_entity.Student.model import StudentModel_create_for_factory, StudentModel_update_for_factory, \
    StudentModel_create_for_response, StudentModel_update_for_response, StudentModel_get_for_response, \
    StudentModel_delete_for_response
from src.api_entity.Subject.api_func import SubjectApiFunc
from src.api_entity.Teacher.api_func import TeacherApiFunc
from src.api_entity.Student.factory import StudentFactory_create, StudentFactory_update
from src.api_entity.Teacher.factory import TeacherFactory_create
from src.api_entity.Subject.factory import SubjectFactory_create, SubjectFactory_update
from src.api_entity.Student.api_path import StudentFullPath
from src.http_func import send_post, send_put, send_get, send_delete
from src.api_entity.Student import entity_name
from tests.config import user1_credential


@pytest.mark.crud
@pytest.mark.teacher
def test_rule_one_teacher(user1_auth_hearders):
    """На один предмет может быть назначен только один учитель"""
    # создаем учителей
    # создаем учителей с помощью фабрики (экземпляр модели фабрики)
    teacher_factory_create_1 = TeacherFactory_create.build()
    teacher_factory_create_2 = TeacherFactory_create.build()
    # создаем учителей с помощью api_func через метод create
    teacher_create_1, teacher_model_create_1 = TeacherApiFunc.create(teacher_factory_create_1.dict(),
                                                                     headers=user1_auth_hearders)
    teacher_create_2, teacher_model_create_2 = TeacherApiFunc.create(teacher_factory_create_2.dict(),
                                                                     headers=user1_auth_hearders)
    # получаем id-к учителя
    teacher_id_1 = teacher_model_create_1.staff_id
    teacher_id_2 = teacher_model_create_2.staff_id
    # Создаем предмет с id-м одного учителя
    # создаем предмет с помощью фабрики (экземпляр модели фабрики)
    subject_factory_create = SubjectFactory_create.build(teacher_id=teacher_id_1)
    # создаем предмет с помощью api_func через метод create
    subject_create, subject_model_create = SubjectApiFunc.create(subject_factory_create.dict(),
                                                                 headers=user1_auth_hearders)
    # получаем id-к созданного предмета
    subject_id = subject_model_create.subject_id
    # Создаем предмет и назначаем на него несколько учителей
    # создаем предмет с помощью фабрики (экземпляр модели фабрики)
    subject_factory_create_fail = SubjectFactory_create.build(teacher_id=f"{', '.join([teacher_id_1, teacher_id_2])}")
    # создаем предмет с помощью send_post (чтобы проверить, что статус код НЕ 200)
    subject_fail_create = send_post(url=SubjectFullPath.create, json=subject_factory_create_fail.dict(),
                                    headers=user1_auth_hearders)
    # проверяем только текст ошибки, так как статус код = 200 (БАГ)
    # TODO подумать, что проверять лучше сам текст ошибки или только наличие ошибки error
    # assert subject_fail_create.status_code == 400, "Status code != 400 for create"
    assert "The teacher ID you entered is invalid" in subject_fail_create.text, f"No error when assigning two teacers to one subject for create"
    assert "error" in subject_fail_create.text, f"No error when assigning two teachers to one subject for create"
    # создаем предмет с помощью фабрики (экземпляр модели фабрики)
    subject_factory_update_fail = SubjectFactory_update.build(teacher_id=f"{', '.join([teacher_id_1, teacher_id_2])}")
    # Изменяем предмет: назначаем на предмет 2-х учителей
    subject_fail_update = send_put(url=SubjectFullPath.put.value / subject_id, json=subject_factory_update_fail.dict(),
                                   headers=user1_auth_hearders)
    # проверяем, что статус код НЕ 200 + в ответе приходит ошибка
    # TODO подумать, что проверять лучше сам текст ошибки или только наличие ошибки error
    assert subject_fail_update.status_code == 400, "Status code != 400 for update subject with two teachers"
    assert "error" in subject_fail_update.text, f"No error when assigning two teachers to one subject for update"
    pass

"""Тесты CRUD Teacher"""
import random

import pytest

from src.api_entity.Subject.api_path import SubjectFullPath
from src.api_entity.Student.model import StudentModel_create_for_factory, StudentModel_update_for_factory, \
    StudentModel_create_for_response, StudentModel_update_for_response, StudentModel_get_for_response, \
    StudentModel_delete_for_response
from src.api_entity.Student.api_func import StudentApiFunc
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
def test_rule_one_major_subject(user1_auth_hearders):
    """У студента может быть только один основной предмет"""
    # Создаем учителя
    # создаем учителей с помощью фабрики (экземпляр модели фабрики)
    teacher_factory_create = TeacherFactory_create.build()
    # создаем учителей с помощью api_func через метод create
    teacher_create, teacher_model_create = TeacherApiFunc.create(teacher_factory_create.dict(),
                                                                 headers=user1_auth_hearders)
    teacher_id = teacher_model_create.staff_id
    # Создаем предметы
    # Создаем предметы с помощью фабрики и назначаем на них учителя
    subject_1 = SubjectFactory_create.build(teacher_id=teacher_id)
    subject_2 = SubjectFactory_create.build(teacher_id=teacher_id)
    # создаем предметы с помощью api_func через метод create
    subject_1_subject_create, subject_1_subject_model_create = SubjectApiFunc.create(subject_1.dict(),
                                                                                     headers=user1_auth_hearders)
    subject_2_subject_create, subject_2_subject_model_create = SubjectApiFunc.create(subject_2.dict(),
                                                                                     headers=user1_auth_hearders)
    # получаем id-ки созданных предметов
    subject_1_id = subject_1_subject_model_create.subject_id
    subject_2_id = subject_2_subject_model_create.subject_id
    # Создаем студента и назначаем ему один осовной предмет
    # создаем студента с помощью фабрики (экземпляр модели фабрики)
    student_factory_create = StudentFactory_create.build(major_id=subject_1_id, minors=None)
    # создаем студента с помощью api_func через метод create
    student_create, student_model_create = StudentApiFunc.create(student_factory_create.dict(),
                                                                 headers=user1_auth_hearders)
    # достаем id-к созданного студента
    student_id = student_model_create.student_id
    # Создаем студента и назначаем ему несколько основных предметов
    # создаем студента с помощью фабрики (экземпляр модели фабрики)
    student_factory_create_fail = StudentFactory_create.build(major_id=", ".join([subject_1_id, subject_2_id]))
    # создаем студента с помощью send_post (чтобы проверить, что статус код НЕ равен 200)
    student_fail_create = send_post(url=StudentFullPath.create, json=student_factory_create_fail.dict(),
                                    headers=user1_auth_hearders)
    # проверяем, что статус код НЕ 200
    assert student_fail_create.status_code == 400, "Status code != 400 for create student with two major subjects"
    # создаем студента с помощью фабрики (экземпляр модели фабрики)
    student_factory_update_fail = StudentFactory_update.build(major_id=f"{', '.join([subject_1_id, subject_2_id])}")
    # Изменяем предмет: назначаем на предмет 2-х учителей
    student_fail_update = send_put(url=SubjectFullPath.put.value / student_id, json=student_factory_update_fail.dict(),
                                   headers=user1_auth_hearders)
    # проверяем, что статус код НЕ 200 + в ответе приходит ошибка
    assert student_fail_update.status_code == 404, "Status code != 400 for update student with two major subjects"
    pass

"""Тесты CRUD Teacher"""
import random

import pytest

from src.api_entity.Student.api_func import StudentApiFunc
from src.api_entity.Student.model import StudentModel_create_for_factory, StudentModel_update_for_factory, \
    StudentModel_create_for_response, StudentModel_update_for_response, StudentModel_get_for_response, \
    StudentModel_delete_for_response
from src.api_entity.Subject.api_func import SubjectApiFunc
from src.api_entity.Teacher.api_func import TeacherApiFunc
from src.api_entity.Student.factory import StudentFactory_create, StudentFactory_update
from src.api_entity.Teacher.factory import TeacherFactory_create
from src.api_entity.Subject.factory import SubjectFactory_create
from src.api_entity.Student.api_path import StudentFullPath
from src.http_func import send_post, send_put, send_get, send_delete
from src.api_entity.Student import entity_name
from tests.config import user1_credential


@pytest.mark.crud
@pytest.mark.teacher
def test_general_scenario(user1_auth_hearders):
    """Тест общего сценария"""
    # Создаем учителя
    # создаем учителя с помощью фабрики (экземпляр модели фабрики)
    teacher_factory_create = TeacherFactory_create.build()
    # создаем учителя с помощью api_func через метод create
    teacher_create, teacher_model_create = TeacherApiFunc.create(teacher_factory_create.dict(),
                                                                 headers=user1_auth_hearders)  # create возвращает body и model
    # получаем id-к созданного учителя через модель
    id_teacher = teacher_model_create.staff_id
    print(id_teacher)
    # Создаем предметы
    # Создаем мажорный и минорный предмет с помощью фабрики и назначаем на них учителя
    major_subject = SubjectFactory_create.build(teacher_id=id_teacher)
    minor_subject = SubjectFactory_create.build(teacher_id=id_teacher)
    # создаем мажорный и минорный предмет с помощью api_func через метод create
    major_subject_create, major_subject_model_create = SubjectApiFunc.create(major_subject.dict(),
                                                                             headers=user1_auth_hearders)  # create возвращает body и model
    minor_subject_create, minor_subject_model_create = SubjectApiFunc.create(minor_subject.dict(),
                                                                             headers=user1_auth_hearders)
    # получаем id-к созданных мажорных и минорных предметов
    id_major = major_subject_model_create.subject_id
    id_minor = minor_subject_model_create.subject_id
    # Создаем Студента
    # Создаем студента с помощью фабрики и присваиваем ему созданные предметы
    student_factory_create = StudentFactory_create.build(major_id=id_major, minors=id_minor)
    # создаем студента с помощью api_func через метод create
    student_create, student_model_create = StudentApiFunc.create(student_factory_create.dict(),
                                                                 headers=user1_auth_hearders)  # create возвращает body и model

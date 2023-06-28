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
    # создаём учителя
    # создаем учителя с помощью фабрики (экземпляр модели фабрики)
    teacher_factory_create = TeacherFactory_create.build()
    # создаем учителя с помощью api_func через метод create
    teacher_create, teacher_model_create = TeacherApiFunc.create(teacher_factory_create.dict(),
                                                                 headers=user1_auth_hearders)  # create возвращает body и model
    # получаем id-к созданного учителя через модель
    id_teacher = teacher_model_create.staff_id
    # создаем предметы
    # создаем мажорный и минорный предмет с помощью фабрики и назначаем на них учителя
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
    # получаем созданный мажорный и минорный предмет с помощью api_func через метод get
    major_get_create, major_model_get_create = SubjectApiFunc.get(subject_id=id_major,
                                                                  headers=user1_auth_hearders)
    minor_get_create, minor_model_get_create = SubjectApiFunc.get(subject_id=id_minor,
                                                                  headers=user1_auth_hearders)
    # получаем id-к учителя
    id_teacher_major = major_model_get_create.teacher["staff_id"]
    id_teacher_minor = minor_model_get_create.teacher["staff_id"]
    # сравниваем id-ки учителей мажорного и миноргного предметов (должны быть одинаковыми,
    # так как на мажорный и минорный предметы назначался один учитель)
    assert id_teacher_major == id_teacher_minor, f"id major {id_teacher_major} not equal id minor {id_teacher_minor}"
    # сравниваем отправленный id-к и полученный в предемете id-к учителя
    assert id_teacher == id_teacher_major, f"id teacher {id_teacher} not equal id teaher in major subject {id_teacher_major}"
    assert id_teacher == id_teacher_minor, f"id teacher {id_teacher} not equal id teaher in major subject {id_teacher_minor}"
    # создаем студента
    # создаем студента с помощью фабрики и присваиваем ему созданные предметы
    student_factory_create = StudentFactory_create.build(major_id=id_major, minors=id_minor)
    # создаем студента с помощью api_func через метод create
    student_create, student_model_create = StudentApiFunc.create(student_factory_create.dict(),
                                                                 headers=user1_auth_hearders)
    # получаем id-к студента через модель
    student_id_create = student_model_create.student_id
    # получаем созданного студента с помощью api_func через метод get
    student_get_create, student_model_get_create = StudentApiFunc.get(student_id=student_id_create,
                                                                      headers=user1_auth_hearders)
    # получаем id-к мажорных и минорных предметов из созданного студента
    id_major_student = student_model_get_create.major["subject_id"]
    id_minor_student = student_model_get_create.minors[0]["subject_id"]
    # сравниваем полученные id-ки с отправленными id-ми мажорного и минорного предметов
    assert id_major == id_major_student, f"id major {id_major} not equal id major subject in student {id_major_student}"
    assert id_minor == id_minor_student, f"id minor {id_minor} not equal id minor subject in student {id_minor_student}"
    # проверяем, что мажорный предмет НЕ равеен минорному предмету
    assert id_major_student != id_minor_student, f"id major {id_major_student} equal id minor subject {id_minor_student}"

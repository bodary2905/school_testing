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


@pytest.mark.crud
@pytest.mark.teacher
def test_crud_student(user1_auth_hearders):
    """Вспомогательные шаги для теста"""
    # получаем существующие предметы в виде словаря и модели
    subjects, subjects_model = SubjectApiFunc.getItems(headers=user1_auth_hearders)
    # достаем список с предметами
    list_subjects = subjects["subjects"]
    # создаем пустой список для сборки id-в предметов
    subject_ids = []
    # с помощью цикла for собираем id-ки предметов
    for subject in list_subjects:
        subject_ids.append(subject["subject_id"])
    # CREATE
    # вывбираем случайный id-к из списка с id-ми предметов
    major_id = random.choice(subject_ids)
    # случайным образом формируем список из id-в предметов для дополнительных предметов
    list_minors = random.sample(subject_ids, random.randint(0, len(subject_ids)))
    # переводим в строку список list_minors и записываем значение в дополнительные предметы
    minors = ", ".join(map(str, list_minors))
    # создаем студента с помощью фабрики (экземпляр модели фабрики)
    student_factory_create1 = StudentFactory_create.build(major_id=major_id, minors=minors)
    # создаем студента с помощью api_func через метод create
    student_create1, student_model_create1 = StudentApiFunc.create(student_factory_create1.dict(),
                                                                   headers=user1_auth_hearders)  # create возвращает body и model
    # выбираем случайный id-к из списка с id-ми предметов
    major_id_upd = random.choice(subject_ids)
    # случайным образом формируем список из id-в предметов для дополнительных предметов
    list_minors_upd = random.sample(subject_ids, random.randint(0, len(subject_ids)))
    # переводим в строку список list_minors и записываем значение в дополнительные предметы
    minors_upd = ", ".join(map(str, list_minors_upd))

    """Тест Email уникален"""
    # достаем email созданного студента
    email = student_model_create1.email_address
    # создаем словарь со студентом и записываем в него существующий email
    student_fail_create = {
        "first_name": "student_name_fail",
        "last_name": "student_last_name_fail",
        "email_address": email,
        "major_id": major_id,
        "minors": minors
    }
    # пытаемся создать студента с почтой, которая уже существует в системе
    create_student_fail = send_post(url=StudentFullPath.create, json=student_fail_create, headers=user1_auth_hearders)
    # проверяем только статус код
    # выводится некорректный текст ошибки при сочетании minors > 1-го и неуникального email (БАГ)
    assert create_student_fail.status_code == 400, "Unique email test for student_create not work"
    # создаем второго студента, чтобы проверить уникальность почты через update
    student_factory_create2 = StudentFactory_create.build(major_id=major_id, minors=minors)
    student_create2, student_model_create2 = StudentApiFunc.create(student_factory_create2.dict(),
                                                                   headers=user1_auth_hearders)
    # достаем id-к 2-го созданного студента
    student_id_2 = student_model_create2.student_id
    # создаем словарь со студентом и записываем в него существующий email
    # student_fail_update = {
    #     "first_name": "student_name_fail",
    #     "last_name": "student_last_name_fail",
    #     "email_address": email,
    #     "major_id": major_id_upd,
    #     "minors": minors_upd
    # }
    student_fail_update = {
        "email_address": email
    }
    # пытаемся изменить студента с email уже существующем в системе
    update_student_fail = send_put(url=StudentFullPath.put.value / student_id_2,
                                   json=student_fail_update, headers=user1_auth_hearders)
    # проверяем статус код
    assert update_student_fail.status_code == 400, "Unique email test for student_update not work"

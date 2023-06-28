"""Тесты CRUD Teacher"""

import pytest

from src.api_entity.Teacher.api_func import TeacherApiFunc
from src.api_entity.Teacher.model import TeacherModel_create_for_factory, TeacherModel_update_for_factory, \
    TeacherModel_create_for_response, TeacherModel_update_for_response, TeacherModel_get_for_response, \
    TeacherModel_delete_for_response
from src.api_entity.Teacher.factory import TeacherFactory_create, TeacherFactory_update
from src.api_entity.Teacher.api_path import TeacherFullPath
from src.http_func import send_post, send_put, send_get, send_delete
from src.api_entity.Teacher import entity_name
from tests.config import user1_credential


@pytest.mark.crud
@pytest.mark.teacher
def test_crud_teaher(user1_auth_hearders):
    """Вспомогательные шаги для теста"""
    # CREATE
    # создаем учителя с помощью фабрики (экземпляр модели фабрики)
    teacher_factory_create = TeacherFactory_create.build()
    # создаем учителя с помощью api_func через метод create
    teacher_create, teacher_model_create = TeacherApiFunc.create(teacher_factory_create.dict(),
                                                                 headers=user1_auth_hearders)
    """Тест Email уникален"""
    # достаем email созданного учителя
    email = teacher_model_create.email_address
    # создаем словарь с учителем и записываем в него существующий email
    teacher_fail_create = {
        "first_name": "teacher_name_fail",
        "last_name": "teacher_last_name_fail",
        "email_address": email
    }
    # пытаемся создать учителя с почтой, которая уже существует в системе
    create_teacher_fail = send_post(url=TeacherFullPath.create, json=teacher_fail_create,
                                    headers=user1_auth_hearders)
    # проверяем статус код
    assert create_teacher_fail.status_code == 400, "Unique email test for teacher_create not work"
    # создаем второго учителя, чтобы проверить уникальность почты через update
    teacher_factory_create2 = TeacherFactory_create.build()
    teacher_create2, teacher_model_create2 = TeacherApiFunc.create(teacher_factory_create2.dict(),
                                                                   headers=user1_auth_hearders)
    # достаем id-к 2-го созданного учителя
    teacher_id_2 = teacher_model_create2.staff_id
    # создаем словарь с учителем и записываем в него существующий email
    teacher_fail_update = {
        "email_address": email
    }
    # пытаемся изменить студента с email уже существующем в системе
    update_teacher_fail = send_put(url=TeacherFullPath.put.value / teacher_id_2,
                                   json=teacher_fail_update, headers=user1_auth_hearders)
    # проверяем статус код
    assert update_teacher_fail.status_code == 400, "Unique email test for teacher_update not work"

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
def test_teaher_auth(user1_auth_hearders):
    """Вспомогательные шаги для тестов"""
    # Создаем учителя авторизованным пользователем для последующих тестов
    # создаем учителя с помощью фабрики (экземпляр модели фабрики)
    teacher_factory_create = TeacherFactory_create.build()
    # создаем учителя с помощью api_func через метод create
    teacher_create, teacher_model_create = TeacherApiFunc.create(teacher_factory_create.dict(),
                                                                 headers=user1_auth_hearders)
    # достаем id-к чителя
    teacher_id = teacher_model_create.staff_id
    # Создаем экземпляр модели измененного учителя для последующих тестов
    teacher_factory_update = TeacherFactory_update.build()

    """Тест доступа CRUD учителя только для авторизованного пользователя"""
    # CREATE
    # создаем учителя с помощью фабрики (экземпляр модели фабрики)
    teacher_factory_create = TeacherFactory_create.build()
    # пытаемся создать учителя через send_post неавторизованным пользователем
    create_teacher_fail = send_post(url=TeacherFullPath.create, json=teacher_factory_create.dict())
    # проверяем, что статус код 401 и НЕ 200
    assert create_teacher_fail.status_code == 401, f"Status code for create teacher without auth not equal 401"
    assert create_teacher_fail.status_code != 200, f"Create teacher passed without auth"
    # GET
    # пытаемся посмотреть созданного учителя неавторизованным пользователем
    get_teacher_fail = send_get(url=TeacherFullPath.get.value / teacher_id)
    # проверяем, что статус код 401 и НЕ 200
    assert get_teacher_fail.status_code == 401, f"Status code for get teacher without auth not equal 401"
    assert get_teacher_fail.status_code != 200, f"Get teacher passed without auth"
    # GETITEMS
    # пытаемся посмотреть учителей через send_get неавторизованным пользователем
    getitems_teacher_fail = send_get(url=TeacherFullPath.getItems.value)
    # проверяем, что статус код 401 и НЕ 200
    assert getitems_teacher_fail.status_code == 401, f"Status code for getItems teacher without auth not equal 401"
    assert getitems_teacher_fail.status_code != 200, f"GetItems teacher passed without auth"
    # UPDATE
    # пытаемся изменить учителя неавторизованным пользователем
    update_teacher_fail = send_put(url=TeacherFullPath.put.value / teacher_id, json=teacher_factory_update.dict())
    # проверяем, что статус код 401 и НЕ 200
    assert get_teacher_fail.status_code == 401, f"Status code for update teacher without auth not equal 401"
    assert get_teacher_fail.status_code != 200, f"Update teacher passed without auth"
    # DELETE
    # пытаемся удалить созданного учителя неавторизованным пользователем
    delete_teacher_fail = send_delete(url=TeacherFullPath.delete.value / teacher_id)
    # проверяем, что статус код 401 и НЕ 200
    assert get_teacher_fail.status_code == 401, f"Status code for delete teacher without auth not equal 401"
    assert get_teacher_fail.status_code != 200, f"Delete teacher passed without auth"

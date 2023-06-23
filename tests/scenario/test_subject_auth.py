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
def test_subject_auth(user1_auth_hearders):
    """Вспомогательные шаги для теста"""
    # Достаем словарь и модель с учителями
    teachers, teachers_model = TeacherApiFunc.getItems(headers=user1_auth_hearders)
    # достаем список учителей из словаря teachers
    teachers_list = teachers["teachers"]
    # создаем пустой словарь для сбора id-в учителей
    staff_ids = []
    for teacher in teachers_list:
        staff_ids.append(teacher["staff_id"])
    # Создаем предмет авторизованным пользователем для последующих тестов
    # создаем предмет с помощью фабрики (экземпляр модели фабрики)
    subject_factory_create = SubjectFactory_create.build(teacher_id=random.choice(staff_ids))
    # создаем предмет с помощью api_func через метод create
    subject_create, subject_model_create = SubjectApiFunc.create(subject_factory_create.dict(),
                                                                 headers=user1_auth_hearders)
    # получаем id-к предмета через модель
    subject_id_create = subject_model_create.subject_id
    # создаем экземпляр модели фабрики для update для последующих тестов
    subject_factory_update = SubjectFactory_update.build(teacher_id=random.choice(staff_ids))

    """Тест доступа CRUD предмета только для авторизованного пользователя"""
    # CREATE
    # пытаемся создать предмет неавторизованным пользователем
    create_subject_fail = send_post(url=SubjectFullPath.create, json=subject_factory_create.dict())
    # проверяем, что статус код 401 и НЕ 200
    assert create_subject_fail.status_code == 401, f"Status code for create subject without auth not equal 401"
    assert create_subject_fail.status_code != 200, f"Create subject passed without auth"
    # GET
    # пытаемся посмотреть созданный предмет неавторизованным пользователем
    get_subject_fail = send_get(url=SubjectFullPath.get.value / subject_id_create)  # в kwargs передаем headers
    # проверяем, что статус код 401 и НЕ 200
    assert get_subject_fail.status_code == 401, f"Status code for get subject without auth not equal 401"
    assert get_subject_fail.status_code != 200, f"Get subject passed without auth"
    # GETITEMS
    # пытаемся посмотреть предметы через send_get неавторизованным пользователем
    getitems_subject_fail = send_get(url=SubjectFullPath.getItems.value)
    # проверяем, что статус код 401 и НЕ 200
    assert getitems_subject_fail.status_code == 401, f"Status code for getItems subject without auth not equal 401"
    assert getitems_subject_fail.status_code != 200, f"GetItems subject passed without auth"
    # UPDATE
    # пытаемся изменить предмет неавторизованным пользователем
    update_subject_fail = send_put(url=SubjectFullPath.put.value / subject_id_create,
                                   json=subject_factory_update.dict())
    # проверяем, что статус код 401 и НЕ 200
    assert update_subject_fail.status_code == 401, f"Status code for update subject without auth not equal 401"
    assert update_subject_fail.status_code != 200, f"Update subject passed without auth"
    # DELETE
    # пытаемся удалить созданный предмет неавторизованным пользователем
    delete_subject_fail = send_delete(url=SubjectFullPath.delete.value / subject_id_create)
    # проверяем, что статус код 401 и НЕ 200
    assert delete_subject_fail.status_code == 401, f"Status code for delete subject without auth not equal 401"
    assert delete_subject_fail.status_code != 200, f"Delete subject passed without auth"

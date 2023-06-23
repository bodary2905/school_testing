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
def test_student_auth(user1_auth_hearders):
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
    student_factory_create = StudentFactory_create.build(major_id=major_id, minors=minors)
    # создаем студента с помощью api_func через метод create
    student_create, student_model_create = StudentApiFunc.create(student_factory_create.dict(),
                                                                 headers=user1_auth_hearders)  # create возвращает body и model
    # получаем id-к студента через модель
    student_id_create = student_model_create.student_id
    # создаем экземпляр модели фабрики для update для последующих тестов
    # вывбираем случайный id-к из списка с id-ми предметов
    major_id_upd = random.choice(subject_ids)
    # случайным образом формируем список из id-в предметов для дополнительных предметов
    list_minors_upd = random.sample(subject_ids, random.randint(0, len(subject_ids)))
    # переводим в строку список list_minors и записываем значение в дополнительные предметы
    minors_upd = ", ".join(map(str, list_minors_upd))
    # создаем экземпляр модели фабрики для update
    student_factory_update = StudentFactory_update.build(major_id=major_id_upd, minors=minors_upd,
                                                         headers=user1_auth_hearders)

    """Тест доступа CRUD студента только для авторизованного пользователя"""
    # CREATE
    # пытаемся создать студента неавторизованным пользователем
    create_student_fail = send_post(url=StudentFullPath.create, json=student_factory_create.dict())
    # проверяем, что статус код 401 и НЕ 200
    assert create_student_fail.status_code == 401, f"Status code for create student without auth not equal 401"
    assert create_student_fail.status_code != 200, f"Create student passed without auth"
    # GET
    # пытаемся посмотреть созданного студента неавторизованным пользователем
    get_student_fail = send_get(url=StudentFullPath.get.value / student_id_create)
    # проверяем, что статус код 401 и НЕ 200
    assert get_student_fail.status_code == 401, f"Status code for get student without auth not equal 401"
    assert get_student_fail.status_code != 200, f"Get student passed without auth"
    # GETITEMS
    # пытаемся посмотреть студентов через send_get неавторизованным пользователем
    getitems_student_fail = send_get(url=StudentFullPath.getItems.value)
    # проверяем, что статус код 401 и НЕ 200
    assert getitems_student_fail.status_code == 401, f"Status code for getitems student without auth not equal 401"
    assert getitems_student_fail.status_code != 200, f"GetItems student passed without auth"
    # UPDATE
    # пытаемся изменить сдудента неавторизованным пользователем
    update_student_fail = send_put(url=StudentFullPath.put.value / student_id_create,
                                   json=student_factory_update.dict())
    # проверяем, что статус код 401 и НЕ 200
    assert update_student_fail.status_code == 401, f"Status code for update student without auth not equal 401"
    assert update_student_fail.status_code != 200, f"Update student passed without auth"
    # DELETE
    # пытаемся удалить созданного студента неавторизованным пользователем
    delete_student_fail = send_delete(url=StudentFullPath.delete.value / student_id_create)
    # проверяем, что статус код 401 и НЕ 200
    assert delete_student_fail.status_code == 401, f"Status code for delete student without auth not equal 401"
    assert delete_student_fail.status_code != 200, f"Delete student passed without auth"

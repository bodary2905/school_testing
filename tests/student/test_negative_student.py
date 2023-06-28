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

negative_values_1 = [
    {"first_name": "", "last_name": "surname", "email_address": "valid_post2@mail.ru", "status_code": 400},
    {"first_name": "name", "last_name": "", "email_address": "valid_post3@mail.ru", "status_code": 400},
    {"first_name": "name", "last_name": "surname", "email_address": "", "status_code": 400},
    {"first_name": "h7XsfZvtM2JLFYmZPhzjl9Mc8xi0hjuE96uhjpnWakjMTxAtEri", "last_name": "surname",
     "email_address": "valid_post4@mail.ru",
     "status_code": 400},
    {"first_name": "name", "last_name": "wKtBcqPDxmSX9MX0IicIYzsoD9HNkYz6UhKM96wGXI6AsI4fG6M",
     "email_address": "valid_post4@mail.ru",
     "status_code": 400},
    {"first_name": "name", "last_name": "", "email_address": "notvalid@post3@mail.ru", "status_code": 400},
    {"first_name": "name", "last_name": "", "email_address": "notvalidpost3mail.ru", "status_code": 400},
    {"first_name": "name", "last_name": "", "email_address": "@mail.ru", "status_code": 400},
    {"first_name": "name", "last_name": "", "email_address": "notvalidpost3@", "status_code": 400},
    {"first_name": "name", "last_name": "", "email_address": "notvalidpost3@mail", "status_code": 400},
    {"first_name": "name", "last_name": "", "email_address": "notvalidpost3@.ru", "status_code": 400},
    {"first_name": "name", "last_name": "", "email_address": "notvalidpost3@mailru", "status_code": 400}

]
negative_values_1_ids = ["first_name is empty", "last_name is empty", "email_address is empty",
                         "first_name contains 51 characters", "last_name contains 51 characters",
                         "email contains two @", "email does not contain @", "email does not contain name before @",
                         "email does not contain domain @", "email contains incorrect domain",
                         "email does not contain domain name before dot", "email does not contain dot in domain"]
negative_values_2 = [
    {"student_id": "ST", "status_code": 404},
    {"student_id": "123", "status_code": 404}
]
negative_values_3 = [
    {"major_id": "SB", "status_code": 400},
    {"major_id": "456", "status_code": 400}
]
negative_values_4 = [
    {"minors": "SB", "status_code": 400},
    {"minors": "789", "status_code": 400}
]


# @pytest.mark.negative
@pytest.mark.student
@pytest.mark.parametrize("negative", negative_values_1, ids=negative_values_1_ids)
def test_negative_1_student(user1_auth_hearders, negative):
    """Тест параметризации"""
    # записываем статус код из набора тестовых данных в переменную и удаляем его из словаря negative
    status_code = negative.pop("status_code")
    # создаем студента с помощью фабрики (экземпляр модели фабрики)
    student_factory_create = StudentFactory_create.build(major_id=None, minors=None)
    # пытаемся создать студента с негативными полями
    create_student_fail = send_post(url=StudentFullPath.create, json=student_factory_create.dict(),
                                    headers=user1_auth_hearders)
    # проверяем статус код
    assert create_student_fail.status_code == status_code, f"Wrong status_code for negative test student\n" \
                                                           f"Expected status_code: {status_code}"
    # """Тест CRUD для студента"""
    # # получаем существующие предметы в виде словаря и модели
    # subjects, subjects_model = SubjectApiFunc.getItems(headers=user1_auth_hearders)
    # # достаем список с предметами
    # list_subjects = subjects["subjects"]
    # # создаем пустой список для сборки id-в предметов
    # subject_ids = []
    # # с помощью цикла for собираем id-ки предметов
    # for subject in list_subjects:
    #     subject_ids.append(subject["subject_id"])
    # # CREATE
    # # вывбираем случайный id-к из списка с id-ми предметов
    # major_id = random.choice(subject_ids)
    # # случайным образом формируем список из id-в предметов для дополнительных предметов
    # list_minors = random.sample(subject_ids, random.randint(0, len(subject_ids)))
    # # переводим в строку список list_minors и записываем значение в дополнительные предметы
    # minors = ", ".join(map(str, list_minors))
    # # создаем студента с помощью фабрики (экземпляр модели фабрики)
    # student_factory_create = StudentFactory_create.build(major_id=major_id, minors=minors)
    # # создаем студента с помощью api_func через метод create
    # student_create, student_model_create = StudentApiFunc.create(student_factory_create.dict(),
    #                                                              headers=user1_auth_hearders)  # create возвращает body и model
    # # GET
    # # получаем id-к студента через модель
    # student_id_create = student_model_create.student_id  # или через словарь student_create["student_id"]
    # # получаем созданного студента с помощью api_func через метод get
    # student_get_create, student_model_get_create = StudentApiFunc.get(student_id=student_id_create,
    #                                                                   headers=user1_auth_hearders)  # get возвращает body и model
    # # сравниваем значения, отправленные на сервер с полученными значениями (фабрику и модель)
    # assert student_factory_create.first_name == student_model_get_create.first_name, f"first_name фабрики НЕ равно first_name модели для create"
    # assert student_factory_create.last_name == student_model_get_create.last_name, f"last_name фабрики НЕ равно last_name модели для create"
    # assert student_factory_create.email_address == student_model_get_create.email_address, f"email_address фабрики НЕ равно email_address модели для create"
    # assert student_factory_create.major_id == student_model_get_create.major[
    #     "subject_id"], "major_id фабрики НЕ равно major модели для create"
    # # проверка для поля minors
    # # достаем id-ки минорных предметов
    # minor_ids = []
    # for minor in student_model_get_create.minors:
    #     minor_ids.append(minor["subject_id"])
    # # сортируем списки с отправленными и полученными minors
    # list_minors.sort()
    # minor_ids.sort()
    # # сравниваем отправленные minors с полученными minors
    # assert list_minors == minor_ids, f"отправленные минорные предемты {list_minors} НЕ равны полученным {minor_ids} для create"
    # # GETITEMS
    # # получаем студентов
    # students, students_model = StudentApiFunc.getItems(headers=user1_auth_hearders, params={"limit": 100})
    # # проверяем, что созданный студент есть в списке по email и id-ку
    # assert any(
    #     student["email_address"] == student_factory_create.email_address for student in students["students"]), \
    #     f"{student_factory_create.email_address} not found in list with students"
    # assert any(
    #     student["student_id"] == student_model_get_create.student_id for student in students["students"]), \
    #     f"{student_model_get_create.student_id} not found in list with students"
    # # UPDATE
    # # вывбираем случайный id-к из списка с id-ми предметов
    # major_id_upd = random.choice(subject_ids)
    # # случайным образом формируем список из id-в предметов для дополнительных предметов
    # list_minors_upd = random.sample(subject_ids, random.randint(0, len(subject_ids)))
    # # переводим в строку список list_minors и записываем значение в дополнительные предметы
    # minors_upd = ", ".join(map(str, list_minors_upd))
    # # создаем экземпляр модели фабрики для update
    # student_factory_update = StudentFactory_update.build(major_id=major_id_upd, minors=minors_upd)
    # # изменяем данные студента с помощью api_func через метод update
    # student_update, student_model_update = StudentApiFunc.update(student_id=student_id_create,
    #                                                              body=student_factory_update.dict(),
    #                                                              headers=user1_auth_hearders)  # update возвращает body и model
    # # получаем id-к студента
    # student_id_update = student_model_update.student_id
    # # сравниваем id-ки, полученные через create и update
    # assert student_id_create == student_id_update, f"id-к create НЕ равен id-ку update"
    # # получаем созданного студента с помощью api_func через метод get
    # student_get_update, student_model_get_update = StudentApiFunc.get(student_id=student_id_update,
    #                                                                   headers=user1_auth_hearders)  # get возвращает body и model
    # assert student_factory_update.first_name == student_model_get_update.first_name, f"first_name фабрики НЕ равно first_name модели для update"
    # assert student_factory_update.last_name == student_model_get_update.last_name, f"last_name фабрики НЕ равно last_name модели для update"
    # # у фабрики update НЕТ поля email_address (так как его изменять нельзя)
    # assert student_factory_create.email_address == student_model_get_update.email_address, f"email_address фабрики НЕ равно email_address модели для update"
    # assert student_factory_update.major_id == student_model_get_update.major[
    #     "subject_id"], "major_id фабрики НЕ равно major модели для update"
    # # проверка для поля minors
    # # достаем id-ки минорных предметов
    # minor_ids_upd = []
    # for minor in student_model_get_update.minors:
    #     minor_ids_upd.append(minor["subject_id"])
    # # сортируем списки с отправленными и полученными minors
    # list_minors_upd.sort()
    # minor_ids_upd.sort()
    # # сравниваем отправленные minors с полученными minors
    # assert list_minors_upd == minor_ids_upd, f"отправленные минорные предемты {list_minors_upd} НЕ равны полученным {minor_ids_upd} для update"
    # # DELETE
    # # Удаляем созданного студента
    # StudentApiFunc.delete(student_id=student_id_create, headers=user1_auth_hearders)
    # # Проверяем, что удаленный студент отсутствует через send_get (так как через StudentApiFunc get возвращается словарь
    # # и модель провалидированные через модель ответа для get-запроса со статус кодом 200, а НЕ 404)
    # response = send_get(url=StudentFullPath.get.value / student_id_create,
    #                     headers=user1_auth_hearders)  # в kwargs передаем headers
    # assert response.status_code == 404, f"Wrong status_code {entity_name}:send_get after delete"
    # pass

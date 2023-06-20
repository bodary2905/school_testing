import dpath

from src.data_func import get_response_body
from src.http_func import send_post, send_put, send_get, send_delete
from src.api_entity.Student.factory import StudentFactory_create, StudentFactory_update
from src.api_entity.Student.model import StudentModel_create_for_factory, StudentModel_update_for_factory, \
    StudentModel_create_for_response, StudentModel_update_for_response, StudentModel_get_for_response, \
    StudentModel_delete_for_response
from src.api_entity.Student.api_path import StudentFullPath
from src.api_entity.Student import entity_name


class StudentApiFunc:
    @staticmethod
    def create(student_dict, **kwargs):
        """Создаем Student"""
        _body = student_dict
        response = send_post(url=StudentFullPath.create, json=_body, **kwargs)
        assert response.status_code == 201, f"Wrong status code {entity_name}: create"
        body = get_response_body(response, err_msg=f"{entity_name}:create")
        # валидируем (создаем экземпляр модели)
        model = StudentModel_create_for_response.parse_obj(body)
        return body, model

    @staticmethod
    def get(student_id, **kwargs):  # аннотируем функцию (указываем возвращаемый тип)
        """Получаем student_body через get"""
        response = send_get(url=StudentFullPath.get.value / student_id, **kwargs)  # в kwargs передаем headers
        assert response.status_code == 200, f"Wrong status_code {entity_name}:get"
        # получаем body из ответа в виде словаря
        body = get_response_body(response, err_msg=f"{entity_name}:get")
        # валидируем (создаем экземпляр модели)
        model = StudentModel_get_for_response.parse_obj(body)
        return body, model

    # @staticmethod
    # def getItens(s**kwargs):  # аннотируем функцию (указываем возвращаемый тип)
    #     """Получаем student_body через get"""
    #     response = send_get(url=StudentFullPath.get.value / student_id, **kwargs)  # в kwargs передаем headers
    #     assert response.status_code == 200, f"Wrong status_code {entity_name}:get"
    #     # получаем body из ответа в виде словаря
    #     body = get_response_body(response, err_msg=f"{entity_name}:get")
    #     # валидируем (создаем экземпляр модели)
    #     model = StudentModel_get_for_response.parse_obj(body)
    #     return body, model

    @staticmethod
    def update(student_id, body, **kwargs):
        response = send_put(url=StudentFullPath.put.value / student_id, json=body, **kwargs)
        assert response.status_code == 200, f"Wrong statuse_code {entity_name}:update\nResponse:{response.text}"
        body = get_response_body(response, err_msg=f"{entity_name}:update")
        # валидируем (создаем экземпляр модели)
        model = StudentModel_update_for_response.parse_obj(body)
        return body, model

    @staticmethod
    def delete(student_id, **kwargs):
        response = send_delete(url=StudentFullPath.delete.value / student_id, **kwargs)
        assert response.status_code == 200, f"Wrong status_code {entity_name}:delete\nResponse:{response.text}"
        body = get_response_body(response, err_msg=f"{entity_name}:delete")
        # валидируем (создаем экземпляр модели)
        model = StudentModel_delete_for_response.parse_obj(body)
        return body, model


if __name__ == "__main__":
    # для теста
    from tests.login import get_auth_header_user1

    # получаем хэдер Authorization
    auth = get_auth_header_user1()
    # CREATE
    # создаем студента с помощью фабрики (экземпляр модели фабрики)
    minor_id_1 = "SB134"
    minor_id_2 = "SB410"
    minor_ids = [minor_id_1, minor_id_2]
    student_factory_create = StudentFactory_create.build(major_id="SB489", minors=f"{minor_id_1}, {minor_id_2}")
    # создаем студента с помощью api_func через метод create
    student_create, student_model_create = StudentApiFunc.create(student_factory_create.dict(),
                                                                 headers=auth)  # create возвращает body и model
    # GET
    # получаем id-к студента через модель
    student_id_create = student_model_create.student_id  # или через словарь student_create["student_id"]
    # получаем созданного студента с помощью api_func через метод get
    student_get_create, student_model_get_create = StudentApiFunc.get(student_id=student_id_create,
                                                                      headers=auth)  # get возвращает body и model
    # сравниваем значения, отправленные на сервер с полученными значениями (фабрику и модель)
    assert student_factory_create.first_name == student_model_get_create.first_name, f"first_name фабрики НЕ равно first_name модели для create"
    assert student_factory_create.last_name == student_model_get_create.last_name, f"last_name фабрики НЕ равно last_name модели для create"
    assert student_factory_create.email_address == student_model_get_create.email_address, f"email_address фабрики НЕ равно email_address модели для create"
    assert student_factory_create.major_id == student_model_get_create.major[
        "subject_id"], "major_id фабрики НЕ равно major модели для create"
    # проверка для поля minors
    # достаем id-ки предметов
    subject_ids = []
    for minor in student_model_get_create.minors:
        subject_ids.append(minor["subject_id"])
    # сортируем списки с отправленными и полученными minors
    minor_ids.sort()
    subject_ids.sort()
    # сравниваем отправленные minors с полученными minors
    assert minor_ids == subject_ids
    # UPDATE
    # создаем экземпляр модели фабрики для update
    student_factory_update = StudentFactory_update.build(major_id="SB489", minors="SB410")
    # изменяем данные студента с помощью api_func через метод update
    student_update, student_model_update = StudentApiFunc.update(student_id=student_id_create,
                                                                 body=student_factory_update.dict(),
                                                                 headers=auth)  # update возвращает body и model
    # получаем id-к студента
    student_id_update = student_model_update.student_id
    # сравниваем id-ки, полученные через create и update
    assert student_id_create == student_id_update, f"id-к create НЕ равен id-ку update"
    # получаем созданного студента с помощью api_func через метод get
    student_get_update, student_model_get_update = StudentApiFunc.get(student_id=student_id_update,
                                                                      headers=auth)  # get возвращает body и model
    assert student_factory_update.first_name == student_model_get_update.first_name, f"first_name фабрики НЕ равно first_name модели для update"
    assert student_factory_update.last_name == student_model_get_update.last_name, f"last_name фабрики НЕ равно last_name модели для update"
    # у фабрики update НЕТ поля email_address (так как его изменять нельзя)
    assert student_factory_create.email_address == student_model_get_update.email_address, f"email_address фабрики НЕ равно email_address модели для update"
    assert student_factory_update.major_id == student_model_get_update.major[
        "subject_id"], "major_id фабрики НЕ равно major модели для update"
    # DELETE
    # Удаляем созданного студента
    StudentApiFunc.delete(student_id=student_id_create, headers=auth)
    # Проверяем, что удаленный студент отсутствует через send_get
    response = send_get(url=StudentFullPath.get.value / student_id_create, headers=auth)  # в kwargs передаем headers
    assert response.status_code == 404, f"Wrong status_code {entity_name}:send_get after delete"
    pass

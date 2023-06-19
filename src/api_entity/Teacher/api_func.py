import dpath

from src.data_func import get_response_body
from src.http_func import send_post, send_put, send_get, send_delete
from src.api_entity.Teacher.factory import TeacherFactory_create, TeacherFactory_update
from src.api_entity.Teacher.model import TeacherModel_create_for_factory, TeacherModel_update_for_factory, \
    TeacherModel_create_for_response, TeacherModel_update_for_response, TeacherModel_get_for_response, \
    TeacherModel_delete_for_response, TeacherModel_getItems_for_response
from src.api_entity.Teacher.api_path import TeacherFullPath
from src.api_entity.Teacher import entity_name


class TeacherApiFunc:
    @staticmethod
    def create(teacher_dict, **kwargs):
        """Создаем Teacher"""
        _body = teacher_dict
        response = send_post(url=TeacherFullPath.create, json=_body, **kwargs)
        assert response.status_code == 201, f"Wrong status code {entity_name}: create"
        body = get_response_body(response, err_msg=f"{entity_name}:create")
        # валидируем (создаем экземпляр модели)
        model = TeacherModel_create_for_response.parse_obj(body)
        return body, model

    @staticmethod
    def get(teacher_id, **kwargs):
        """Получаем teacher_body через get"""
        response = send_get(url=TeacherFullPath.get.value / teacher_id, **kwargs)  # в kwargs передаем headers
        assert response.status_code == 200, f"Wrong status_code {entity_name}:get"
        # получаем body из ответа в виде словаря
        body = get_response_body(response, err_msg=f"{entity_name}:get")
        # валидируем (создаем экземпляр модели)
        model = TeacherModel_get_for_response.parse_obj(body)
        return body, model

    @staticmethod
    def getItems(**kwargs):
        """Получаем teacher_body через getItems"""
        response = send_get(url=TeacherFullPath.getItems.value, **kwargs)
        assert response.status_code == 200, f"Wrong status_code {entity_name}:getItems"
        # получаем body из ответа в виде словаря
        body = get_response_body(response, err_msg=f"{entity_name}:get")
        # валидируем (создаем экземпляр модели)
        model = TeacherModel_getItems_for_response.parse_obj(body)
        return body, model

    @staticmethod
    def update(teacher_id, body, **kwargs):
        response = send_put(url=TeacherFullPath.put.value / teacher_id, json=body, **kwargs)
        assert response.status_code == 200, f"Wrong statuse_code {entity_name}:update"
        body = get_response_body(response, err_msg=f"{entity_name}:update")
        # валидируем (создаем экземпляр модели)
        model = TeacherModel_update_for_response.parse_obj(body)
        return body, model

    @staticmethod
    def delete(teacher_id, **kwargs):
        response = send_delete(url=TeacherFullPath.delete.value / teacher_id, **kwargs)
        assert response.status_code == 200, f"Wrong status_code {entity_name}:delete"
        body = get_response_body(response, err_msg=f"{entity_name}:delete")
        # валидируем (создаем экземпляр модели)
        model = TeacherModel_delete_for_response.parse_obj(body)
        return body, model


if __name__ == "__main__":
    # для теста
    from tests.login import get_auth_header_user1

    # получаем хэдер Authorization
    auth = get_auth_header_user1()
    # CREATE
    # создаем учителя с помощью фабрики (экземпляр модели фабрики)
    teacher_factory_create = TeacherFactory_create.build()
    # создаем учителя с помощью api_func через метод create
    teacher_create, teacher_model_create = TeacherApiFunc.create(teacher_factory_create.dict(),
                                                                 headers=auth)  # create возвращает body и model
    # GET
    # получаем id-к учителя через модель
    teacher_id_create = teacher_model_create.staff_id  # или через словарь student_create["student_id"]
    # получаем созданного учителя с помощью api_func через метод get
    teacher_get_create, teacher_model_get_create = TeacherApiFunc.get(teacher_id=teacher_id_create,
                                                                      headers=auth)  # get возвращает body и model
    # сравниваем значения, отправленные на сервер с полученными значениями (фабрику и модель)
    assert teacher_factory_create.first_name == teacher_model_get_create.first_name, f"first_name фабрики НЕ равно first_name модели для create"
    assert teacher_factory_create.last_name == teacher_model_get_create.last_name, f"last_name фабрики НЕ равно last_name модели для create"
    assert teacher_factory_create.email_address == teacher_model_get_create.email_address, f"email_address фабрики НЕ равно email_address модели для create"
    # UPDATE
    # создаем экземпляр модели фабрики для update
    teacher_factory_update = TeacherFactory_update.build()
    # изменяем данные учителя с помощью api_func через метод update
    teacher_update, teacher_model_update = TeacherApiFunc.update(teacher_id=teacher_id_create,
                                                                 body=teacher_factory_update.dict(),
                                                                 headers=auth)  # update возвращает body и model
    # получаем id-к учителя
    teacher_id_update = teacher_model_update.staff_id
    # сравниваем id-ки, полученные через create и update
    assert teacher_id_create == teacher_id_update, f"id-к create НЕ равен id-ку update"
    # получаем созданного учителя с помощью api_func через метод get
    teacher_get_update, teacher_model_get_update = TeacherApiFunc.get(teacher_id=teacher_id_update,
                                                                      headers=auth)  # get возвращает body и model
    assert teacher_factory_update.first_name == teacher_model_get_update.first_name, f"first_name фабрики НЕ равно first_name модели для update"
    assert teacher_factory_update.last_name == teacher_model_get_update.last_name, f"last_name фабрики НЕ равно last_name модели для update"
    # у фабрики update НЕТ поля email_address (так как его изменять нельзя)
    assert teacher_factory_create.email_address == teacher_model_get_update.email_address, f"email_address фабрики НЕ равно email_address модели для update"

    # teachers, teachers_model = TeacherApiFunc.getItems(headers=auth)
    # print(teachers)

    # DELETE
    # Удаляем созданного учителя
    TeacherApiFunc.delete(teacher_id=teacher_id_create, headers=auth)
    # Проверяем, что удаленный учитель отсутствует через send_get
    response = send_get(url=TeacherFullPath.get.value / teacher_id_create, headers=auth)  # в kwargs передаем headers
    assert response.status_code == 404, f"Wrong status_code {entity_name}:get"
    pass

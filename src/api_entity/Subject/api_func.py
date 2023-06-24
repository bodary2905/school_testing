import dpath

from src.data_func import get_response_body
from src.http_func import send_post, send_put, send_get, send_delete
from src.api_entity.Subject.factory import SubjectFactory_create, SubjectFactory_update
from src.api_entity.Subject.model import SubjectModel_create_for_factory, SubjectModel_update_for_factory, \
    SubjectModel_create_for_response, SubjectModel_update_for_response, SubjectModel_get_for_response, \
    SubjectModel_delete_for_response, SubjectModel_getItems_for_response
from src.api_entity.Subject.api_path import SubjectFullPath
from src.api_entity.Subject import entity_name


class SubjectApiFunc:
    @staticmethod
    def create(subject_dict, **kwargs):
        """Создаем Subject"""
        _body = subject_dict
        response = send_post(url=SubjectFullPath.create, json=_body, **kwargs)
        assert response.status_code == 201, f"Wrong status code {entity_name}: create\n" \
                                            f"Actual: {response.status_code}. Expected 201\n" \
                                            f"Message: {response.text}"
        body = get_response_body(response, err_msg=f"{entity_name}:create")
        # валидируем (создаем экземпляр модели)
        model = SubjectModel_create_for_response.parse_obj(body)
        return body, model

    @staticmethod
    def get(subject_id, **kwargs):  # аннотируем функцию (указываем возвращаемый тип)
        """Получаем subject_body через get"""
        response = send_get(url=SubjectFullPath.get.value / subject_id, **kwargs)  # в kwargs передаем headers
        assert response.status_code == 200, f"Wrong status code {entity_name}: get\n" \
                                            f"Actual: {response.status_code}. Expected 201\n" \
                                            f"Message: {response.text}"
        # получаем body из ответа в виде словаря
        body = get_response_body(response, err_msg=f"{entity_name}:get")
        # валидируем (создаем экземпляр модели)
        model = SubjectModel_get_for_response.parse_obj(body)
        return body, model

    @staticmethod
    def getItems(**kwargs):
        """Получаем subject_body через getItems"""
        response = send_get(url=SubjectFullPath.getItems.value, **kwargs)  # в kwargs передаем headers
        assert response.status_code == 200, f"Wrong status code {entity_name}: getItems\n" \
                                            f"Actual: {response.status_code}. Expected 201\n" \
                                            f"Message: {response.text}"
        # получаем body из ответа в виде словаря
        body = get_response_body(response, err_msg=f"{entity_name}:getItems")
        # валидируем (создаем экземпляр модели)
        model = SubjectModel_getItems_for_response.parse_obj(body)
        return body, model

    @staticmethod
    def update(subject_id, body, **kwargs):
        response = send_put(url=SubjectFullPath.put.value / subject_id, json=body, **kwargs)
        assert response.status_code == 200, f"Wrong status code {entity_name}: update\n" \
                                            f"Actual: {response.status_code}. Expected 201\n" \
                                            f"Message: {response.text}"
        body = get_response_body(response, err_msg=f"{entity_name}:update")
        # валидируем (создаем экземпляр модели)
        model = SubjectModel_update_for_response.parse_obj(body)
        return body, model

    @staticmethod
    def delete(subject_id, **kwargs):
        response = send_delete(url=SubjectFullPath.delete.value / subject_id, **kwargs)
        assert response.status_code == 200, f"Wrong status code {entity_name}: delete\n" \
                                            f"Actual: {response.status_code}. Expected 201\n" \
                                            f"Message: {response.text}"
        body = get_response_body(response, err_msg=f"{entity_name}:delete")
        # валидируем (создаем экземпляр модели)
        model = SubjectModel_delete_for_response.parse_obj(body)
        return body, model


if __name__ == "__main__":
    # для теста
    from tests.login import get_auth_header_user1

    # получаем хэдер Authorization
    auth = get_auth_header_user1()

    # subjects, subjects_model = SubjectApiFunc.getItems(headers=auth)
    # print(subjects)

    # CREATE
    # создаем предмет с помощью фабрики (экземпляр модели фабрики)
    subject_factory_create = SubjectFactory_create.build(teacher_id="TC421")
    # создаем предмет с помощью api_func через метод create
    subject_create, subject_model_create = SubjectApiFunc.create(subject_factory_create.dict(),
                                                                 headers=auth)  # create возвращает body и model
    # GET
    # получаем id-к предмета через модель
    subject_id_create = subject_model_create.subject_id  # или через словарь student_create["student_id"]
    # получаем созданный предмет с помощью api_func через метод get
    student_get_create, subject_model_get_create = SubjectApiFunc.get(subject_id=subject_id_create,
                                                                      headers=auth)  # get возвращает body и model
    # сравниваем значения, отправленные на сервер с полученными значениями (фабрику и модель)
    assert subject_factory_create.name == subject_model_get_create.name, f"name фабрики НЕ равно name модели для create"
    assert subject_factory_create.description == subject_model_get_create.description, f"description фабрики НЕ равно description модели для create"
    assert subject_factory_create.teacher_id == subject_model_get_create.teacher[
        "staff_id"], f"teacher_id фабрики НЕ равно staff_id модели для create"
    # UPDATE
    # создаем экземпляр модели фабрики для update
    subject_factory_update = SubjectFactory_update.build(teacher_id="TC127")
    # изменяем данные предмета с помощью api_func через метод update
    subject_update, subject_model_update = SubjectApiFunc.update(subject_id=subject_id_create,
                                                                 body=subject_factory_update.dict(),
                                                                 headers=auth)  # update возвращает body и model
    # получаем id-к предмета
    subject_id_update = subject_model_update.subject_id
    # сравниваем id-ки, полученные через create и update
    assert subject_id_create == subject_id_update, f"id-к create НЕ равен id-ку update"
    # получаем созданный предмет с помощью api_func через метод get
    subject_get_update, subject_model_get_update = SubjectApiFunc.get(subject_id=subject_id_update,
                                                                      headers=auth)  # get возвращает body и model
    assert subject_factory_update.name == subject_model_get_update.name, f"name фабрики НЕ равно name модели для update"
    assert subject_factory_update.description == subject_model_get_update.description, f"description фабрики НЕ равно description модели для update"
    assert subject_factory_update.teacher_id == subject_model_get_update.teacher[
        "staff_id"], f"teacher_id фабрики НЕ равно staff_id модели для update"
    # DELETE
    # Удаляем созданный предмет
    SubjectApiFunc.delete(subject_id=subject_id_create, headers=auth)
    # Проверяем, что удаленный предмет отсутствует через send_get
    response = send_get(url=SubjectFullPath.get.value / subject_id_create, headers=auth)  # в kwargs передаем headers
    assert response.status_code == 404, f"Wrong status_code {entity_name}:send_get after delete"
    pass

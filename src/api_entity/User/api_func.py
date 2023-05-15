"""
    Функции для работы с данной сущностью через API
"""
import dpath
from strenum import StrEnum

from src.data_func import get_response_body
from src.http_func import send_post, send_put, send_get
from src.api_entity.User.api_path import UserFullPath
from src.api_entity.User import entity_name

# TODO все переделать
class _UserBodyPath(StrEnum):
    """Константы с путями в body для User"""
    token = "token"


class UserApiFunc:
    # TODO ДОДЕЛАТЬ
    @staticmethod
    def register(body):
        """Регистрируем нового User"""
        response = send_post(url=UserFullPath.register, json=body)
        assert response.status_code == 200, f"Wrong status_code on {UserApiFunc.register.__name__} " \
                                            f"{entity_name}"

    # TODO ДОДЕЛАТЬ
    @staticmethod
    def confirmRegistration(body):
        """Подтверждаем регистрацию нового User"""
        response = send_post(url=UserFullPath.confirmRegistration, json=body)
        assert response.status_code == 200, f"Wrong status_code on {UserApiFunc.confirmRegistration.__name__} " \
                                            f"{entity_name}"

    @staticmethod
    def loginWithoutCaptcha(body):
        """Логинимся без Captcha на сервер"""
        response = send_post(url=UserFullPath.loginWithoutCaptcha, json=body)
        assert response.status_code == 200, f"Wrong status_code on {entity_name}:loginWithoutCaptcha"
        body = get_response_body(response, err_msg=f"{entity_name}:loginWithoutCaptcha")
        # получаем umt_token
        umt_token = dpath.get(body, _UserBodyPath.umt_token, separator='.')
        # пока просто проверяем что token - ненулевая строка
        assert isinstance(umt_token, str) and \
               len(umt_token) > 0, f"{entity_name} UMT token broken or don't exist"
        return umt_token

    @staticmethod
    def loginToService(body):
        """Логинимся в конкретный сервис"""
        response = send_post(url=UserFullPath.loginToService, json=body)
        assert response.status_code == 200, f"Wrong status_code on {entity_name}:loginToService"
        body = get_response_body(response, err_msg=f"{entity_name}:loginToService")
        # получаем token_to_service
        token_to_service = dpath.get(body, _UserBodyPath.token_to_service, separator='.')
        # пока просто проверяем что token - ненулевая строка
        assert isinstance(token_to_service, str) and \
               len(token_to_service) > 0, f"{entity_name} token is broken or don't exist"
        return token_to_service

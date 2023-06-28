"""
    Функции для работы с данной сущностью через API
"""
import dpath
from strenum import StrEnum

from src.data_func import get_response_body
from src.http_func import send_post, send_put, send_get
from src.api_entity.User.api_path import UserFullPath
from src.api_entity.User import entity_name


class _UserBodyPath(StrEnum):
    """Константы с путями в body для User"""
    token = "token"


class UserApiFunc:
    @staticmethod
    def register(body):
        """Регистрируем нового User"""
        response = send_post(url=UserFullPath.register, json=body)
        assert response.status_code == 200, f"Wrong status_code on {UserApiFunc.register.__name__} " \
                                            f"{entity_name}"

    @staticmethod
    def login(body):
        """Логинимся на сервер"""
        response = send_post(url=UserFullPath.login, json=body)
        assert response.status_code == 200, f"Wrong status_code on {entity_name}:login"
        body = get_response_body(response, err_msg=f"{entity_name}:loginWithoutCaptcha")
        # получаем token
        token = dpath.get(body, _UserBodyPath.token, separator='.')
        # пока просто проверяем что token - ненулевая строка
        assert isinstance(token, str) and \
               len(token) > 0, f"{entity_name} UMT token broken or don't exist"
        return token


if __name__ == "__main__":
    # для теста

    body = {
        "username": "testuser_1",
        "password": "testpassword_1"
    }
    user_1 = UserApiFunc.login(body)
    print(user_1)
    pass

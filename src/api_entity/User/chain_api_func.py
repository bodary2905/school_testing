"""
    Функции состоящие из цепочек API вызовов
"""

from src.api_entity.User.api_func import UserApiFunc
from src.api_entity.const import UserCredential


class UserChainApiFunc:
    @staticmethod
    def get_token(role_credential: UserCredential):
        """Получаем header для авторизации для пользователя 'role_credential'"""
        # формируем body для loginWithoutCaptcha
        body = {
            "email_address": role_credential.email,
            "password": role_credential.password,
        }
        # получаем umt token
        token = UserApiFunc.login(body)
        role_credential.token = token
        return token

    @staticmethod
    def get_auth_header(role_credential: UserCredential,
                        auth_required=False,  # принудительная авторизация
                         ):
        """Получаем header с token-ом авторизации"""
        # активируем получение token-а при
        if auth_required or not role_credential.token:
            # флаге auth_required или если пользователь еще не получил token
            role_credential.token = UserChainApiFunc.get_token(role_credential)
        return {"Authorization": role_credential.token}

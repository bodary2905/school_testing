"""
    Функции для login-ов конкретный пользователей
"""
from src.api_entity.User.chain_api_func import UserChainApiFunc
from tests.config import user1_credential


def get_auth_header_user1():
    """Получаем header-ы для авторизации для User1"""
    return UserChainApiFunc.get_auth_header(user1_credential)


if __name__ == "__main__":
    # для теста
    headers = get_auth_header_user1()
    print(headers)

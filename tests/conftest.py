"""
    Общие фикстуры для тестов
"""
import pytest

from tests.login import get_auth_header_user1


@pytest.fixture(scope="session")
def user1_auth_hearders():
    """Получаем header-ы авторизации для user1"""
    auth_str = get_auth_header_user1()  # в переменную auth_str записываем результат функции get_auth_header_user1()
    yield auth_str  # возвращаем результат функции get_auth_header_user1(), yield = return

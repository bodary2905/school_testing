"""
    Общие фикстуры для тестов
"""
import pytest

from tests.login import get_auth_header_user1


@pytest.fixture(scope="session")
def user1_auth_hearders():
    """Получаем header-ы авторизации для user1"""
    return get_auth_header_user1()


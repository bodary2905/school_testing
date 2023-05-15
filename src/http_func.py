"""
    Функции для работы http-клиента
"""
import json
import requests
from enum import Enum


def _convert_body_to_json(kwargs):
    """Конвертируем body в json если нужно"""
    if kwargs.get("data") and isinstance(kwargs.get("data"), dict):
        kwargs["data"] = json.dumps(kwargs["data"])


def _convert_url_to_str(kwargs):
    """Конвертируем URL в str если нужно"""
    if kwargs.get("url") and isinstance(kwargs.get("url"), Enum):
        kwargs["url"] = kwargs["url"].value


def _change_headers_user_agent(kwargs):
    """Изменяем User-Agent для маскировки"""
    kwargs["headers"] = {"User-Agent": "PostmanRuntime/7.31.3"} | kwargs.get("headers", {})


def _preprocess_kwargs(kwargs):
    """Предобрабатываем kwargs для request-а"""
    _convert_url_to_str(kwargs)
    _convert_body_to_json(kwargs)
    _change_headers_user_agent(kwargs)


def send_post(**kwargs):
    """Отправляем POST запрос"""
    # kwargs["headers"] = {"Content-Type": "application/json"} | kwargs.get("headers", {})
    _preprocess_kwargs(kwargs)
    response = requests.post(**kwargs)
    return response


def send_put(**kwargs):
    """Отправляем PUT запрос"""
    # kwargs["headers"] = {"Content-Type": "application/json"} | kwargs.get("headers", {})
    _preprocess_kwargs(kwargs)
    response = requests.put(**kwargs)
    return response


def send_get(**kwargs):
    """Отправляем GET запрос"""
    _preprocess_kwargs(kwargs)
    response = requests.get(**kwargs)
    return response


def send_delete(**kwargs):
    """Отправляем DELETE запрос"""
    _preprocess_kwargs(kwargs)
    response = requests.delete(**kwargs)
    return response

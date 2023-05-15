"""
    Функции для работы с Json Schema
"""
import dpath


def get_field_parameter(field_name, parameter, schema):
    """Получаем parameter для field"""
    return dpath.get(schema, f"properties.{field_name}.{parameter}", separator='.')


def get_field_maxLength(field_name, schema):
    """Получаем maxLength для field"""
    return get_field_parameter(field_name, "maxLength", schema)


def get_field_minimum(field_name, schema):
    """Получаем minimum для field"""
    return get_field_parameter(field_name, "minimum", schema)


def get_field_maximum(field_name, schema):
    """Получаем maximum для field"""
    return get_field_parameter(field_name, "maximum", schema)

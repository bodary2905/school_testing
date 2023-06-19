"""
    Pydantic модели для данной сущности
"""

from __future__ import annotations
from typing import Literal, Optional, ClassVar, Union, List, Tuple
from pydantic import Field, constr, Extra, validator, ValidationError, validate_arguments, EmailStr
from email_validator import validate_email, EmailNotValidError
import re
import random

from src.api_entity.model import BaseModel


class TeacherModel_create_for_factory(BaseModel):
    """Модель для фабрики"""
    first_name: constr(min_length=1, max_length=50) = Field(..., description="имя")
    last_name: constr(min_length=1, max_length=50) = Field(..., description="фамилия")
    email_address: EmailStr = Field(..., description="электронная почта")
    # email_address: constr(regex=r"[\w.-]+@[\w-]+\.[\w.]+") = Field(..., description="электронная почта")
    # email_address: str = Field(..., description="электронная почта")


class TeacherModel_create_for_response(TeacherModel_create_for_factory):
    """Модель для response"""
    staff_id: str = Field(..., description="id-к учителя")
    # переопределяем поле email_address, чтобы не срабатывала проверка EmailStr (не пропускает 255 символов)
    email_address: str = Field(..., description="электронная почта")

    @validator("staff_id")
    def staff_id_check(cls, v: str):
        assert v.startswith("TC")
        try:
            v_list = v.split("TC")
            v_int = int(v_list[1])
        except ValueError as e:
            raise ValueError(f"Error in func TeacherModel_create:staff_id") from e
        return v

    @validator("email_address")
    def email_address_check(cls, v: str):
        # 255 символов - ограничение по документации
        if len(v) > 255:
            raise ValueError(f"Error in validate TeacherModel_create:email_address_check_len")
        # от 130 до 255 проверяем email через регулярное выражение
        # if len(v) > 129:
        #     if not re.fullmatch(r'[\w.-]+@[\w-]+\.[\w.]+', v):
        #         # re.fullmatch(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', v)
        #         raise ValueError(f"Email is invalid")
        # через библиотеку validate_email поверяем валидность email-адреса
        else:
            validate_email(v,
                           check_deliverability=False)  # check_deliverability: флаг, указывающий, нужно ли проверять возможность доставки email-сообщений на указанный адрес
        return v


class TeacherModel_update_for_factory(BaseModel):
    first_name: Optional[constr(min_length=1, max_length=50)] = Field(description="имя")
    last_name: Optional[constr(min_length=1, max_length=50)] = Field(description="фамилия")


class TeacherModel_update_for_response(TeacherModel_create_for_response):
    pass


class TeacherModel_get_for_response(TeacherModel_create_for_response):
    pass


class TeacherModel_delete_for_response(BaseModel):
    message: str = Field(description="сообщение об успехе удаления")

    @validator("message")
    def message_check(cls, v: str):
        assert "You have successfully deleted the teacher with the following ID: TC" in v, f"Wrong message for delete"
        return v


if __name__ == "__main__":
    body = {
        "first_name": "teacher_name_1",
        "last_name": "teacher_last_name_1",
        "email_address": "post@mail.ru",
        "staff_id": "TC123"
    }
    body_2 = {"message": "You have successfully deleted the teacher with the following ID: TC"}
    response = TeacherModel_create_for_response.parse_obj(body)
    print(response)
    pass

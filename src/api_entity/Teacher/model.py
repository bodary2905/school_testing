"""
    Pydantic модели для данной сущности
"""

from __future__ import annotations
from typing import Literal, Optional, ClassVar, Union, List, Tuple
from pydantic import Field, constr, Extra, validator, ValidationError, validate_arguments, EmailStr
from email_validator import validate_email, EmailNotValidError
import re

from src.api_entity.model import BaseModel


class TeacherModel_create(BaseModel):
    """Базовая модель"""
    # type зависит от фермер/покупатель: Адрес отгрузки/Адрес доставки
    first_name: constr(min_length=1, max_length=50) = Field(..., description="имя")
    last_name: constr(min_length=1, max_length=50) = Field(..., description="фамилия")
    # email_address: EmailStr = Field(..., description="электронная почта")
    # email_address: constr(regex=r"[\w.-]+@[\w-]+\.[\w.]+") = Field(..., description="электронная почта")
    email_address: str = Field(..., description="электронная почта")

    # @validator("email_address")
    # def email_address_check_len(cls, v: str):
    #     if len(v) > 255:
    #         raise ValueError(f"Error in validate TeacherModel_create:email_address_check_len")
    #     return v

    @validator("email_address")
    def email_address_check(cls, v: str):
        if len(v) > 255:
             raise ValueError(f"Error in validate TeacherModel_create:email_address_check_len")
        if len(v) > 129:
            try:
                re.fullmatch(r'[\w.-]+@[\w-]+\.[\w.]+', v)
                # re.fullmatch(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', v)
            except ValueError as e:
                raise ValueError(f"Email is invalid") from e
        else:
            try:
                validate_email(v, check_deliverability=False)
            except EmailNotValidError as e:
                print(str(e))




class TeacherModel_update(TeacherModel_create):
    """Модель с полем id"""
    id: int = Field(..., description='id')



if __name__ == "__main__":
    body = {
        "first_name": "teacher_name_2",
        "last_name": "teacher_last_name_2",
        "email_address": "qAssOfLGnnKLSGerKhVCzQwWXZWmQlgeEKfWnLLppAuduEMjJIUPneXgMVVJBXxBXnSocWxfUDvwUoIWSmrewbxOZsLNoAqfwtQSfLQqHtzgxpmNrUXlqzihdzcmail.ru"
    }
    teaher_1 = TeacherModel_create.parse_obj(body)

    pass

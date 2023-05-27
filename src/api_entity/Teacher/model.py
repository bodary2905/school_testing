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

    @validator("staff_id")
    def staff_id_check(cls, v:str):
        assert v.startswith("TC")
        try:
            v_list = v.split("TC")
            v_int = int(v_list[1])
        except ValueError as e:
            raise ValueError(f"Error in func TeacherModel_create:staff_id") from e
        return v
    @validator("email_address")
    def email_address_check(cls, v: str):
        if len(v) > 255:
             raise ValueError(f"Error in validate TeacherModel_create:email_address_check_len")
        if len(v) > 129:
                if not re.fullmatch(r'[\w.-]+@[\w-]+\.[\w.]+', v):
                    # re.fullmatch(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', v)
                    raise ValueError(f"Email is invalid")
        else:
            try:
                validate_email(v, check_deliverability=False)
            except EmailNotValidError as e:
                print(str(e))
        return v
class TeacherModel_update_for_factory(BaseModel):
    first_name: Optional[constr(min_length=1, max_length=50)] = Field(description="имя")
    last_name: Optional[constr(min_length=1, max_length=50)] = Field(description="фамилия")

class TeacherModel_get_for_response(TeacherModel_create_for_response):
    pass



if __name__ == "__main__":
    body = {
        "first_name": "teacher_name_1",
        "last_name": "teacher_last_name_1",
        "email_address": "test@mail.ru",
        "staff_id": "TC123"
    }
    teaher_1 = TeacherModel_get_for_response.parse_obj(body)

    pass

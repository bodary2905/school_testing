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


class StudentModel_create_for_factory(BaseModel):
    """Модель для фабрики"""
    first_name: constr(min_length=1, max_length=50) = Field(..., description="имя")
    last_name: constr(min_length=1, max_length=50) = Field(..., description="фамилия")
    email_address: EmailStr = Field(..., description="электронная почта")
    major_id: Optional[str] = Field(description="основной предмет")
    minors: Optional[str] = Field(description="дополнительные предметы")

    @validator("major_id")
    def major_id_check(cls, v:str):
        assert len(v.split(",")) == 1, "Более одного основного предмета"
        assert v.startswith("SB"), "major_id начинается не с SB"
        try:
            v_list = v.split("SB")
            v_int = int(v_list[1])
        except ValueError as e:
            raise ValueError(f"Error in func TeacherModel_create:major_id") from e
        return v




class TeacherModel_create_for_response(BaseModel):
    """Модель для response"""
    staff_id: str = Field(..., description="id-к учителя")
    first_name: constr(min_length=1, max_length=50) = Field(..., description="имя")
    last_name: constr(min_length=1, max_length=50) = Field(..., description="фамилия")
    email_address: EmailStr = Field(..., description="электронная почта")
    @validator("staff_id")
    def staff_id_check(cls, v:str):
        assert v.startswith("TC")
        try:
            v_list = v.split("TC")
            v_int = int(v_list[1])
        except ValueError as e:
            raise ValueError(f"Error in func TeacherModel_create:staff_id") from e
        return v

class TeacherModel_update_for_factory(BaseModel):
    first_name: Optional[constr(min_length=1, max_length=50)] = Field(description="имя")
    last_name: Optional[constr(min_length=1, max_length=50)] = Field(description="фамилия")
    email_address: EmailStr = Field(description="электронная почта")

class TeacherModel_get_for_response(TeacherModel_create_for_response):
    pass



if __name__ == "__main__":
    body = {
        "first_name": "teacher_name_1",
        "last_name": "teacher_last_name_1",
        "email_address": "test@mail.ru",
        "major_id": "SB1"
    }
    teaher_1 = StudentModel_create_for_factory.parse_obj(body)

    pass

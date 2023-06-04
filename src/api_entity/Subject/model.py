"""
    Pydantic модели для данной сущности
"""

from __future__ import annotations

import typing
from typing import Literal, Optional, ClassVar, Union, List, Dict
from pydantic import Field, constr, Extra, validator, ValidationError, validate_arguments, EmailStr
from pydantic.types import Json
from email_validator import validate_email, EmailNotValidError
import re
import random

from src.api_entity.model import BaseModel
from src.api_entity.Teacher.model import TeacherModel_create_for_response


class SubjectModel_create_for_factory(BaseModel):
    """Модель для фабрики"""
    name: constr(min_length=1, max_length=50) = Field(..., description="название предмета")
    teacher_id: str = Field(..., description="id-к учителя")
    description: Optional[constr(min_length=0, max_length=150)] = Field(description="описание предмета")


class SubjectModel_create_for_response(BaseModel):
    """Модель для response"""
    subject_id: str = Field(..., description="id-к предмета")
    name: constr(min_length=1, max_length=50) = Field(..., description="название предмета")
    description: Optional[constr(min_length=0, max_length=150)] = Field(description="описание предмета")
    teacher: dict = Field(..., description="информация об учителе")

    @validator('teacher')
    def teacher_is_dict(cls, v):
        assert v != {}, "Словарь teacher пуст"
        try:
            TeacherModel_create_for_response.parse_obj(v)
        except ValueError as e:
            raise ValueError(f"Error in func SubjectModel_create_for_response:teacher dict") from e
        return v

    @validator("subject_id")
    def subject_id_check(cls, v: str):
        assert v.startswith("SB"), "student_id начинается не с ST"
        try:
            v_list = v.split("SB")
            v_int = int(v_list[1])
        except ValueError as e:
            raise ValueError(f"Error in func SubjectModel_create_for_response:subject_id") from e
        return v


class SubjectModel_update_for_factory(BaseModel):
    """Модель для response"""
    name: Optional[constr(min_length=1, max_length=50)] = Field(description="название предмета")
    teacher_id: Optional[str] = Field(description="id-к учителя")
    description: Optional[constr(min_length=0, max_length=150)] = Field(description="описание предмета")


class SubjectModel_update_for_response(SubjectModel_create_for_response):
    pass


class SubjectModel_get_for_response(SubjectModel_create_for_response):
    pass


class SubjectModel_delete_for_response(BaseModel):
    message: str = Field(description="сообщение об успехе удаления")

    @validator("message")
    def message_check(cls, v: str):
        assert "You have successfully deleted the subject with the following ID: SB" in v, f"Wrong message for delete"
        return v


if __name__ == "__main__":
    body = {
        "subject_id": "SB210",
        "name": "Литература_upd",
        "description": "new",
        "teacher": {
            "staff_id": "TC898",
            "first_name": "teacher_name_02",
            "last_name": "teacher_last_name_2",
            "email_address": "teacher_2@mail.ru"
        }
    }
    body_2 = {"message": "You have successfully deleted the subject with the following ID: SB491"}
    subject_1 = SubjectModel_create_for_response.parse_obj(body)
    pass

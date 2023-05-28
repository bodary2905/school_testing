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

    @validator('teacher', pre=True)
    def teacher_is_dict(cls, v):
        assert len(v) != 0, "Словарь teacher пуст"
        try:
            SubjectModel_create_for_response._validate_teacher(v)
        except ValueError as e:
            raise ValueError(
                f"Error in func SubjectModel_create_for_response:teacher_is_dict" +
                f"Ошибка при валидации типа поля teacher. Исходное значение: {v}"
            ) from e
        return v
    @staticmethod
    @validate_arguments  # валидируем тип функции с помощью специальной функции pydantic
    def _validate_teacher(v: Optional[Dict[str, str]]):
        pass
    @validator('teacher', pre=True)
    def check_teacher_dict(cls, v):
        try:
            TeacherModel_create_for_response.parse_obj(v)
        except ValueError as e:
            raise ValueError(f"Error in func SubjectModel_create_for_response:teacher") from e
        return v

    @validator("subject_id")
    def subject_id_check(cls, v:str):
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

class SubjectsModel_get_for_response(SubjectModel_create_for_response):
    pass


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
    subject_1 = SubjectModel_create_for_response.parse_obj(body)
    pass

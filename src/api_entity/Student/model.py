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


class StudentModel_create_for_factory(BaseModel):
    """Модель для фабрики"""
    first_name: constr(min_length=1, max_length=50) = Field(..., description="имя")
    last_name: constr(min_length=1, max_length=50) = Field(..., description="фамилия")
    email_address: EmailStr = Field(..., description="электронная почта")
    major_id: Optional[str] = Field(description="основной предмет")
    minors: Optional[str] = Field(description="дополнительные предметы")


    # @validator("major_id")
    # def major_id_check(cls, v:str):
    #     assert len(v.split(",")) == 1, "Более одного основного предмета"
    #     assert v.startswith("SB"), "major_id начинается не с SB"
    #     try:
    #         v_list = v.split("SB")
    #         v_int = int(v_list[1])
    #     except ValueError as e:
    #         raise ValueError(f"Error in func TeacherModel_create:major_id") from e
    #     return v

    # @validator("minors")
    # def minors_check(cls, v:str):
    #     v_list = v.split(",")
    #     if len(v_list) > 1:
    #         for v in v_list:
    #             assert v.startswith("SB"), "Один из дополнительных предметов начинается не с SB"
    #             print(f"{v} прошел")
    #             assert type(int(v.split("SB")[1])) == int, "после SB не число список"
    #             print(f"{v} прошел")
    #     else:
    #         assert v.startswith("SB"), "minor_id начинается не с SB"
    #     return v

class StudentModel_create_for_response(StudentModel_create_for_factory):
    """Модель для response"""
    student_id: str = Field(..., description="id-к студента")
    major: Optional[dict] = Field(description="основной предмет")
    minors: Optional[list] = Field(description="дополнительные предметы")

    @validator('major', pre=True)
    def major_is_dict(cls, v):
        assert len(v) != 0, "Словарь major пуст"
        try:
            StudentModel_create_for_response._validate_major(v)
        except ValueError as e:
            raise ValueError(
                f"Error in func StudentModel_create_for_response:major_is_dict" +
                f"Ошибка при валидации типа поля major. Исходное значение: {v}"
            ) from e
        return v
    @staticmethod
    @validate_arguments  # валидируем тип функции с помощью специальной функции pydantic
    def _validate_major(v: Optional[Dict[str, Union[str, dict]]]):
        pass
    @validator('minors', pre=True)
    def minors_is_list(cls, v):
        try:
            StudentModel_create_for_response._validate_minors(v)
        except ValueError as e:
            raise ValueError(
                f"Error in func StudentModel_create_for_factory:minors_is_list" +
                f"Ошибка при валидации типа поля minors. Исходное значение: {v}"
            ) from e
        return v
    @staticmethod
    @validate_arguments  # валидируем тип функции с помощью специальной функции pydantic
    def _validate_minors(v: Optional[List[dict]]):
        pass

    @validator('major', pre=True)
    def check_teacher_dict(cls, v):
        try:
            body = v["teacher"]
            TeacherModel_create_for_response.parse_obj(body)
        except ValueError as e:
            raise ValueError(f"Error in func StudentModel_create_for_factory:major_id for teacher") from e
        return v

    @validator("student_id")
    def student_id_check(cls, v:str):
        assert v.startswith("ST"), "student_id начинается не с ST"
        try:
            v_list = v.split("ST")
            v_int = int(v_list[1])
        except ValueError as e:
            raise ValueError(f"Error in func StudentModel_create_for_response:student_id") from e
        return v

class StudentModel_update_for_factory(BaseModel):
    """Модель для response"""
    first_name: Optional[constr(min_length=1, max_length=50)] = Field(description="имя")
    last_name: Optional[constr(min_length=1, max_length=50)] = Field(description="фамилия")
    major_id: Optional[str] = Field(description="основной предмет")
    minors: Optional[str] = Field(description="дополнительные предметы")

class StudentModel_get_for_response(StudentModel_create_for_response):
    pass


if __name__ == "__main__":
    body = {
        "student_id": "ST123",
        "first_name": "student_name_5",
        "last_name": "student_last_name_5",
        "email_address": "student_5@mail.ru",
        "major": {
            "subject_id": "SB94",
            "name": "География",
            "description": "",
            "teacher": {
                "staff_id": "TC301",
                "first_name": "teacher_name_1",
                "last_name": "teacher_last_name_1",
                "email_address": "teacher_1@mail.ru"
            }
        },
        "minors": [
            {
                "subject_id": "SB94",
                "name": "География",
                "description": "",
                "teacher": {
                    "staff_id": "TC301",
                    "first_name": "teacher_name_1",
                    "last_name": "teacher_last_name_1",
                    "email_address": "teacher_1@mail.ru"
                }
            },
            {
                "subject_id": "SB412",
                "name": "Математика",
                "description": "",
                "teacher": {
                    "staff_id": "TC898",
                    "first_name": "teacher_name_02",
                    "last_name": "teacher_last_name_2",
                    "email_address": "teacher_2@mail.ru"
                }
            }
        ]
    }
    student_1 = StudentModel_create_for_response.parse_obj(body)

    pass

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
from src.api_entity.Subject.model import SubjectModel_create_for_response


class StudentModel_create_for_factory(BaseModel):
    """Модель создания для фабрики"""
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


class StudentModel_create_for_response(BaseModel):
    """Модель создания для ответа"""
    student_id: str = Field(..., description="id-к студента")
    first_name: constr(min_length=1, max_length=50) = Field(..., description="имя")
    last_name: constr(min_length=1, max_length=50) = Field(..., description="фамилия")
    email_address: EmailStr = Field(..., description="электронная почта")
    major: Optional[dict] = Field(description="основной предмет")
    minors: Optional[list] = Field(description="дополнительные предметы")

    @validator('major', pre=True)
    def major_check(cls, v):
        assert v != {}, "Словарь major пуст"
        try:
            # body = v["teacher"]
            # TeacherModel_create_for_response.parse_obj(body)
            SubjectModel_create_for_response.parse_obj(v)
        except ValueError as e:
            raise ValueError(f"Error in func StudentModel_create_for_factory:major_id for teacher") from e
        return v

    @validator('minors')
    def minors_check(cls, v):
        if len(v) > 0:
            if len(v) == 1:
                try:
                    SubjectModel_create_for_response.parse_obj(v[0])
                except ValueError as e:
                    raise ValueError(f"Error in func StudentModel_create_for_factory:minors for teacher") from e
            else:
                for _dict in v:
                    try:
                        SubjectModel_create_for_response.parse_obj(_dict)
                    except ValueError as e:
                        raise ValueError(f"Error in func StudentModel_create_for_factory:minors for teacher") from e
        else:
            print(f"{v} список с минорными предметами пуст")
        return v

    # @validator('major', pre=True)
    # def check_teacher_dict(cls, v):
    #     try:
    #         body = v["teacher"]
    #         TeacherModel_create_for_response.parse_obj(body)
    #     except ValueError as e:
    #         raise ValueError(f"Error in func StudentModel_create_for_factory:major_id for teacher") from e
    #     return v

    @validator("student_id")
    def student_id_check(cls, v: str):
        assert v.startswith("ST"), "student_id начинается не с ST"
        try:
            v_list = v.split("ST")
            v_int = int(v_list[1])
        except ValueError as e:
            raise ValueError(f"Error in func StudentModel_create_for_response:student_id") from e
        return v


class StudentModel_update_for_factory(BaseModel):
    """Модель изменения для фабрики"""
    first_name: Optional[constr(min_length=1, max_length=50)] = Field(description="имя")
    last_name: Optional[constr(min_length=1, max_length=50)] = Field(description="фамилия")
    major_id: Optional[str] = Field(description="основной предмет")
    minors: Optional[str] = Field(description="дополнительные предметы")


class StudentModel_update_for_response(StudentModel_create_for_response):
    """Модель изменения для ответа"""
    pass


class StudentModel_get_for_response(StudentModel_create_for_response):
    """Модель получения для ответа"""
    pass


class StudentModel_delete_for_response(BaseModel):
    """Модель удаления для ответа"""
    message: str = Field(description="сообщение об успехе удаления")

    @validator("message")
    def message_check(cls, v: str):
        assert "You have successfully deleted the student with the following ID: ST" in v, f"Wrong message for delete"
        return v


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
            # {
            #     "subject_id": "SB94",
            #     "name": "География",
            #     "description": "",
            #     "teacher": {
            #         "staff_id": "TC301",
            #         "first_name": "teacher_name_1",
            #         "last_name": "teacher_last_name_1",
            #         "email_address": "teacher_1@mail.ru"
            #     }
            # },
            # {
            #     "subject_id": "SB412",
            #     "name": "Математика",
            #     "description": "",
            #     "teacher": {
            #         "staff_id": "TC898",
            #         "first_name": "teacher_name_02",
            #         "last_name": "teacher_last_name_2",
            #         "email_address": "teacher_2@mail.ru"
            #     }
            # }
        ]
    }
    student_1 = StudentModel_create_for_response.parse_obj(body)
    print(student_1)
    body_2 = {"message": "You have successfully deleted the student with the following ID: ST793"}
    del_student = StudentModel_delete_for_response.parse_obj(body_2)
    pass

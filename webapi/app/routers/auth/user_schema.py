#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/25 15:37
# @Author  : 冉勇
# @Site    : 
# @File    : user_schema.py
# @Software: PyCharm
# @desc    : 用户模式
from pydantic import BaseModel, validator
from webapi.app.excpetions.ParamsException import ParamsError


class UserDto(BaseModel):
    name: str
    password: str
    username: str
    email: str

    @validator('name', 'password', 'username', 'email')
    def field_not_empty(cls, v):
        if isinstance(v, str) and len(v.strip()) == 0:
            raise ParamsError("不能为空")
        return v


class UserForm(BaseModel):
    username: str
    password: str

    @validator('username', 'password')
    def name_not_empty(cls, v):
        if isinstance(v, str) and len(v.strip()) == 0:
            raise ParamsError("不能为空")
        return v

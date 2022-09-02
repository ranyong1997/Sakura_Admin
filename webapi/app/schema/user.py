#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/22 10:31
# @Author  : 冉勇
# @Site    : 
# @File    : user.py
# @Software: PyCharm
# @desc    : 用户实例表单,主要用于用户信息
from pydantic import BaseModel, validator
from webapi.app.schema.base import SakuraModel
from webapi.app.excpetions.ParamsException import ParamsError


class UserUpdateForm(BaseModel):
    id: int
    name: str = None
    email: str = None
    phone: str = None
    role: str = None
    is_valid: bool = False  # 是否已验证

    @validator('id')
    def id_not_empty(cls, v):
        return SakuraModel.not_empty(v)


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

    @validator('password', 'username')
    def name_not_empty(cls, v):
        if isinstance(v, str) and len(v.strip()) == 0:
            raise ParamsError("不能为空")
        return v


class ResetPwdForm(BaseModel):
    password: str
    token: str

    @validator('token', 'password')
    def name_not_empty(cls, v):
        if isinstance(v, str) and len(v.strip()) == 0:
            raise ParamsError("不能为空")
        return v

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

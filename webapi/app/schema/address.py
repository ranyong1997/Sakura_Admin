#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/28 09:53
# @Author  : 冉勇
# @Site    : 
# @File    : address.py
# @Software: PyCharm
# @desc    : 网关表单
from pydantic import validator, BaseModel
from webapi.app.excpetions.ParamsException import ParamsError
from webapi.app.schema.base import SakuraModel


class SakuraAddressForm(BaseModel):
    id: int = None
    env: int = None
    name: str = ''
    gateway: str = ''

    @validator("env", "name")
    def name_not_empty(cls, v):
        return SakuraModel.not_empty(v)

    @validator("gateway", whole=True)
    def prefix_match(cls, v):
        if not v.startswith("http://", "https://", "ws://", "wss://"):
            raise ParamsError("前缀不为http或ws")
        return v

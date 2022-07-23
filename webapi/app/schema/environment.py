#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/20 11:33
# @Author  : 冉勇
# @Site    : 
# @File    : environment.py
# @Software: PyCharm
# @desc    : 环境-架构
from pydantic import BaseModel, validator
from webapi.app.excpetions.ParamsException import ParamsError


class EnvironmentForm(BaseModel):
    id: int = None
    name: str
    remarks: str = None

    @validator("name")
    def name_not_empty(cls, v):
        if isinstance(v, str) and len(v.strip()) == 0:
            raise ParamsError("不能为空")
        return v

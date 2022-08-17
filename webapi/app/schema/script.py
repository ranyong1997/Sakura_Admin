#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/17 11:40
# @Author  : 冉勇
# @Site    : 
# @File    : script.py
# @Software: PyCharm
# @desc    : 获取脚本表单
from pydantic import BaseModel, validator
from webapi.app.schema.base import SakuraModel


class PyScriptForm(BaseModel):
    command: str
    value: str

    @validator("command")
    def name_not_empty(cls, v):
        return SakuraModel.not_empty(v)

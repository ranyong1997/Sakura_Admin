#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/25 16:31
# @Author  : 冉勇
# @Site    : 
# @File    : gconfig.py
# @Software: PyCharm
# @desc    : 全局配置表单
from pydantic import BaseModel, validator
from webapi.app.excpetions.ParamsException import ParamsError


class GConfigForm(BaseModel):
    id: int = None
    key: str
    value: str
    env: str = None
    key_type: int
    enable = bool

    @validator("key", "value", "key_type", "enable")
    def name_not_empty(cls, v):
        if isinstance(v, str) and len(v.strip()) == 0:
            raise ParamsError("不能为空！")
        if not isinstance(v, int) and not v:
            raise ParamsError("不能为空！")
        return v

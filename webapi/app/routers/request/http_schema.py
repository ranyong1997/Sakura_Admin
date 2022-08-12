#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/12 09:17
# @Author  : 冉勇
# @Site    : 
# @File    : http_schema.py
# @Software: PyCharm
# @desc    : HTTP 模式
from pydantic import BaseModel, validator
from webapi.app.excpetions.ParamsException import ParamsError


class HttpRequestForm(BaseModel):
    method = str
    url = str
    body: str = None
    body_type: int = 0
    headers: dict = {}

    @validator('method', 'url')
    def name_not_empty(cls, v):
        if isinstance(v, str) and len(v.strip()) == 0:
            raise ParamsError("不能为空")
        return v

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/1 14:15
# @Author  : 冉勇
# @Site    : 
# @File    : constructor.py
# @Software: PyCharm
# @desc    : 构造器表单
from pydantic import BaseModel, validator
from webapi.app.excpetions.ParamsException import ParamsError
from webapi.app.schema.base import SakuraModel


class ConstructorForm(BaseModel):
    id: int = None
    value: str = ""
    type: int
    name: str
    index: int = 0
    constructor_json : str
    enable: bool
    case_id: int = None
    public: bool
    suffix: bool

    @validator('name', 'constructor_json', 'type', 'public', 'enable', 'suffix')
    def name_not_empty(cls, v):
        if isinstance(v, str) and len(v.strip()) == 0:
            raise ParamsError("不能为空")
        if not isinstance(v, int):
            if not v:
                raise ParamsError("不能为空")
        return v


class ConstructorIndex(BaseModel):
    id: int
    index: int

    @validator("id", "index")
    def name_not_empty(cls, v):
        return SakuraModel.not_empty(v)

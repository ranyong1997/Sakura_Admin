#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/1 16:34
# @Author  : 冉勇
# @Site    : 
# @File    : testcase_out_parameters.py
# @Software: PyCharm
# @desc    : 测试用例输出参数表单
from pydantic import BaseModel, validator
from webapi.app.schema.base import SakuraModel


class SakuraTestCaseOutParametersForm(BaseModel):
    id: int = None
    name: str
    expression: str = None
    match_index: str = None
    source: int

    @validator("name", "source")
    def name_not_empty(cls, v):
        return SakuraModel.not_empty(v)

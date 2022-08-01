#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/1 16:29
# @Author  : 冉勇
# @Site    : 
# @File    : testcase_data.py
# @Software: PyCharm
# @desc    : 测试用例数据表单
from pydantic import BaseModel, validator
from webapi.app.schema.base import SakuraModel


class SakuraTestcaseDataForm(BaseModel):
    id: int = None
    case_id: int = None
    name: str
    json_data: str
    env: int

    @validator("env", "name", "json_data")
    def name_not_empty(cls, v):
        return SakuraModel.not_empty(v)

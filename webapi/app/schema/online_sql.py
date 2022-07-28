#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/28 11:01
# @Author  : 冉勇
# @Site    : 
# @File    : online_sql.py
# @Software: PyCharm
# @desc    : 执行sql表单
from pydantic import BaseModel, validator
from webapi.app.schema.base import SakuraModel


class OnlineSQLForm(BaseModel):
    id: int = None
    sql: str

    @validator("sql", "id")
    def name_not_empty(cls, v):
        return SakuraModel.not_empty(v)

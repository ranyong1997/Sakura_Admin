#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/27 10:49
# @Author  : 冉勇
# @Site    : 
# @File    : database.py
# @Software: PyCharm
# @desc    : 数据库表单
from pydantic import validator, BaseModel
from webapi.app.schema.base import SakuraModel


class DatabaseForm(BaseModel):
    id: int = None
    name: str
    host: str
    port: int = None
    username: str
    password: str
    database: str
    sql_type: int
    env: int

    @validator("name", "host", "port", "username", "password", "database", "sql_type", "env")
    def data_not_empty(cls, v):
        return SakuraModel.not_empty(v)

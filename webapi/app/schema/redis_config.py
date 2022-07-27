#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/27 16:26
# @Author  : 冉勇
# @Site    : 
# @File    : redis_config.py
# @Software: PyCharm
# @desc    : redis配置表单
from pydantic import validator, BaseModel
from webapi.app.schema.base import SakuraModel


class RedisConfigForm(BaseModel):
    id: int = None
    name: str
    addr: str
    db: int = 0
    password: str = ''
    cluster: bool = False
    env: int

    @validator("name", "addr", "cluster", "db", "env")
    def data_not_empty(cls, v):
        return SakuraModel.not_empty(v)

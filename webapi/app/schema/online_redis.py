#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/27 15:28
# @Author  : 冉勇
# @Site    : 
# @File    : online_redis.py
# @Software: PyCharm
# @desc    : 在线执行redis
from pydantic import BaseModel, validator
from webapi.app.schema.base import SakuraModel


class OlineRedisForm(BaseModel):
    id: int = None
    command: str

    @validator("command", "id")
    def name_not_empty(cls, v):
        return SakuraModel.not_empty(v)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/29 17:04
# @Author  : 冉勇
# @Site    : 
# @File    : test_plan.py
# @Software: PyCharm
# @desc    : 测试计划表单
from typing import List
from pydantic import BaseModel, validator
from webapi.app.schema.base import SakuraModel


class SakuraTestPlanForm(BaseModel):
    id: int = None
    project_id: int
    name: str
    priority: str
    env: List[int]
    cron: str
    ordered: bool
    case_list: List[int]
    pass_rate: int
    receiver: List[int] = []
    msg_type: List[int] = []
    retry_minutes: int = 0

    @validator("cast_list", "project_id", "env", "cron", "ordered", "priority", "name", "pass_rate")
    def name_not_empty(cls, v):
        return SakuraModel.not_empty(v)

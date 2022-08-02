#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/2 10:32
# @Author  : 冉勇
# @Site    : 
# @File    : testcase_directory.py
# @Software: PyCharm
# @desc    : 测试用例目录
from typing import List
from pydantic import BaseModel, validator
from webapi.app.schema.base import SakuraModel


class SakuraTestcaseDirectoryForm(BaseModel):
    id: int = None
    name: str
    project_id: int
    parent: int = None

    @validator("name", "project_id")
    def name_not_empty(cls, v):
        return SakuraModel.not_empty(v)


class SakuraTestCaseDto(BaseModel):
    """
    数据传输对象（DTO）(Data Transfer Object)，是一种设计模式之间传输数据的软件应用系统。数
    据传输目标往往是数据访问对象从数据库中检索数据。
    数据传输对象与数据交互对象或数据访问对象之间的差异是一个以不具有任何行为除了存储和检索的数据（访问和存取器）。
    """
    project_id: int
    id_list: List[int]
    directory_id: int

    @validator("id_list", "project_id", "directory_id")
    def name_not_empty(cls, v):
        return SakuraModel.not_empty(v)

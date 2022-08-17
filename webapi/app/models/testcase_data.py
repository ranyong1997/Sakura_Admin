#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/2 16:45
# @Author  : 冉勇
# @Site    : 
# @File    : testcase_data.py
# @Software: PyCharm
# @desc    : 测试用例数据,用来存储各个环境下的测试数据,用于数据驱动
__author__ = "sakura"

from sqlalchemy import Column, INT, String, UniqueConstraint, TEXT
from webapi.app.models.basic import SakuraBase


class SakuraTestCaseData(SakuraBase):
    env = Column(INT, nullable=False)
    case_id = Column(INT, nullable=False)
    name = Column(String(32), nullable=False)
    json_data = Column(TEXT, nullable=False)

    __table_args__ = (
        UniqueConstraint('env', 'case_id', 'name', 'deleted_at'),
    )
    __tablename__ = 'sakura_testcase_data'
    __filelds__ = [name]
    __show__ = 1

    def __init__(self, env, case_id, name, json_data, user_id, id=None):
        super().__init__(user_id, id)
        self.env = env
        self.case_id = case_id
        self.name = name
        self.json_data = json_data

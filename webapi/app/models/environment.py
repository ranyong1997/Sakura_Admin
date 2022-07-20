#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/20 11:19
# @Author  : 冉勇
# @Site    : 
# @File    : environment.py
# @Software: PyCharm
# @desc    : 环境变量
from sqlalchemy import Column, String, UniqueConstraint
from webapi.app.models.basic import SakuraBase


class Environment(SakuraBase):
    __tablename__ = "sakura_environment"
    # 环境名称
    name = Column(String(10))
    remarks = Column(String(200))

    __table_args__ = (
        UniqueConstraint('name', 'deleted_at')
    )
    __fields__ = [name]
    __tag__ = "环境"
    __alias__ = dict(name="名称", remarks="备注")

    def __init__(self, name, remarks, user, id=None):
        super().__init__(user, id)
        self.name = name
        self.remarks = remarks

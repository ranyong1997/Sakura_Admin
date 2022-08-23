#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/23 10:02
# @Author  : 冉勇
# @Site    : 
# @File    : sql_log.py
# @Software: PyCharm
# @desc    : 数据库日志
from sqlalchemy import Column, String, INT
from webapi.app.models.basic import SakuraBase
from webapi.app.models.database import SakuraDatabase


class SakuraSQLHistory(SakuraBase):
    __tablename__ = "sakura_sql_history"
    sql = Column(String(1024), comment="sql语句")
    elapsed = Column(INT, comment="请求耗时")
    database_id = Column(INT, comment="操作数据库id")
    database: SakuraDatabase

    def __init__(self, sql, elapsed, database_id, user):
        super().__init__(user)
        self.sql = sql
        self.elapsed = elapsed
        self.database_id = database_id

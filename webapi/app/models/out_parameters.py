#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/21 10:13
# @Author  : 冉勇
# @Site    : 
# @File    : out_parameters.py
# @Software: PyCharm
# @desc    : 输出参数
from sqlalchemy import Column, String, INT, UniqueConstraint
from webapi.app.models.basic import SakuraBase


class SakuraTestCaseParameters(SakuraBase):
    """
    sakura用例参数数据，与用例bind
    """
    __tablename__ = "sakura_out_parameters"
    __table_args__ = (UniqueConstraint('case_id', 'name', 'deleted_at'))
    # 用例id
    case_id = Column(INT, nullable=False)
    # 参数名
    name = Column(String(24), nullable=False)
    # 来源类型
    source = Column(INT, nullable=False, default=0,
                    comment="0: Body(TEXT) 1: Body(JSON) 2: Header 3: Cookie 4: HTTP状态码")
    # 表达式
    expression = Column(String(128))
    # 获取结果索引，可以说random,也可以是all,还可以是数字
    match_index = Column(String(16))

    def __init__(self, name, source, case_id, user_id, expression=None, match_index=None, id=None):
        super().__init__(user_id, id)
        self.name = name
        self.case_id = case_id
        self.expression = expression
        self.match_index = match_index
        self.source = source
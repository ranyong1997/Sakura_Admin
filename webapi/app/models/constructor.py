#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/1 11:31
# @Author  : 冉勇
# @Site    : 
# @File    : constructor.py
# @Software: PyCharm
# @desc    : 数据构造器,包含前置条件和后置条件
from sqlalchemy import Column, INT, String, BOOLEAN, UniqueConstraint, TEXT, select, desc
from webapi.app.models.basic import SakuraBase


class Constructor(SakuraBase):
    __tablename__ = "sakura_constructor"
    __table_args__ = (
        UniqueConstraint('case_id', 'suffix', 'name', 'deleted_at'),
    )
    type = Column(INT, default=0, comment="0: 测试用例 1: 数据库 2: redis 3: py脚本 4: 其他")
    name = Column(String(64), comment="数据初始化")
    enable = Column(BOOLEAN, default=True, nullable=False)
    constructor_json = Column(TEXT, nullable=False)
    value = Column(String(16), comment="返回值")
    case_id = Column(INT, nullable=False, comment="所属用例id")
    public = Column(BOOLEAN, default=False, comment="是否共享")
    index = Column(INT, comment="前置条件顺序")
    suffix = Column(BOOLEAN, default=False, comment="是否是后置条件,默认为否")

    def __init__(self, type, name, enable, constructor_json, case_id, public, user_id, value="", suffix=False, id=None,
                 index=0):
        super().__init__(user_id, id)
        self.type = type
        self.name = name
        self.enable = enable
        self.constructor_json = constructor_json
        self.case_id = case_id
        self.public = public
        self.value = value
        self.suffix = suffix
        self.index = index

    @staticmethod
    async def get_index(session, case_id, suffix=False):
        sql = select(Constructor).where(
            Constructor.deleted_at == 0, Constructor.case_id == case_id,
            Constructor.suffix == suffix
        ).order_by(desc(Constructor.index))
        data = await session.execute(sql)
        query = data.scalars().first()
        # 如果没有查出前/后置条件,那么给它设置为0
        if query is None:
            return 0
        return query.index + 1

    def __str__(self):
        return f"[{'后置条件' if self.suffix else '前置条件'}: {self.name}]({self.id}))"

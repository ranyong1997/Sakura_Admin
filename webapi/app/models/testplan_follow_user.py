#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/29 16:55
# @Author  : 冉勇
# @Site    : 
# @File    : testplan_follow_user.py
# @Software: PyCharm
# @desc    : 测试计划关注用户
from sqlalchemy import INT, Column, UniqueConstraint
from webapi.app.models.basic import SakuraBase


class SakuraTestPlanFollowUserRel(SakuraBase):
    """
    测试计划关注用户表
    """
    __tablename__ = "sakura_testplan_follow_user_rel"
    __table_args__ = (
        UniqueConstraint("user_id", "plan_id", "deleted_at")
    )
    user_id = Column(INT, nullable=False)
    plan_id = Column(INT, nullable=False)

    def __init__(self, plan_id, user_id, user):
        super().__init__(user)
        self.user_id = user_id
        self.plan_id = plan_id

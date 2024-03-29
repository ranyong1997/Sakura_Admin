#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/21 09:44
# @Author  : 冉勇
# @Site    : 
# @File    : project_role.py
# @Software: PyCharm
# @desc    : 项目角色
from sqlalchemy import INT, Column
from webapi.app.models.basic import SakuraBase


class ProjectRole(SakuraBase):
    __tablename__ = "sakura_project_role"
    user_id = Column(INT, index=True)
    project_id = Column(INT, index=True)
    project_role = Column(INT, index=True)
    __alias__ = dict(user_id="用户", project_id="项目", project_role="角色")
    __tag__ = "项目角色"
    __fields__ = (project_id, user_id, project_role)
    __show__ = 2

    def __init__(self, user_id, project_id, project_role, create_user):
        super().__init__(create_user)
        self.user_id = user_id
        self.project_id = project_id
        self.project_role = project_role

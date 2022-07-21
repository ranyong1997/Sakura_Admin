#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/21 09:33
# @Author  : 冉勇
# @Site    : 
# @File    : project.py
# @Software: PyCharm
# @desc    : 项目管理
from sqlalchemy import INT, Column, String, Boolean
from webapi.app.models.basic import SakuraBase


class Project(SakuraBase):
    __tablename__ = 'sakura_project'
    name = Column(String(16), unique=True, index=True)
    owner = Column(INT)
    app = Column(String(32), index=True)
    private = Column(Boolean, default=False)
    description = Column(String(200))
    avatar = Column(String(128), nullable=True)
    lark_url = Column(String(128), nullable=True)
    __tag__ = "项目"
    __fields__ = (name, owner, app, private, description, avatar, lark_url)
    __alias__ = dict(name="项目名称", owner="项目所有者", private="是否私有", description="项目描述", avatar="项目头像", lark_url="飞书通知url")
    __show__ = 2

    def __init__(self, name, app, owner, create_user, description="", private=False, avatar=None, lark_url=''):
        super().__init__(create_user)
        self.name = name
        self.app = app
        self.owner = owner
        self.private = private
        self.description = description
        self.avatar = avatar
        self.lark_url = lark_url

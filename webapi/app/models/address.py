#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/20 17:28
# @Author  : 冉勇
# @Site    : 
# @File    : address.py
# @Software: PyCharm
# @desc    : py请求网关地址
from sqlalchemy import Column, INT, String, UniqueConstraint
from webapi.app.models.basic import SakuraBase


class SakuraGateway(SakuraBase):
    __tablename__ = 'sakura_gateway'
    __table_args__ = (UniqueConstraint('env', 'name', 'deleted_at'),)
    env = Column(INT, comment='对应环境')
    name = Column(String(32), comment='网关名称')
    gateway = Column(String(128), comment='网关地址')

    __fields__ = (name, env, gateway)
    __tag__ = '网关'
    __alias__ = dict(name="网关名称", env="环境", gateway="网关地址")
    __show__ = 2

    def __init__(self, env, name, gateway, user_id, id=None):
        super().__init__(user_id, id)
        self.env = env
        self.name = name
        self.gateway = gateway

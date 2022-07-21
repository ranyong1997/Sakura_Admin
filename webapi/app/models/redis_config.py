#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/21 10:01
# @Author  : 冉勇
# @Site    : 
# @File    : redis_config.py
# @Software: PyCharm
# @desc    : redis配置
from sqlalchemy import Column, INT, String, Boolean, UniqueConstraint
from webapi.app.models.basic import SakuraBase


class SakuraRedis(SakuraBase):
    __tablename__ = "sakura_redis_info"
    __table_args__ = (UniqueConstraint('env', 'name', 'deleted_at'))
    env = Column(INT, nullable=False)  # 对应环境
    name = Column(String(25), nullable=False)  # redis名称
    addr = Column(String(128), nullable=False)  # redis连接地址
    username = Column(String(36), nullable=False)  # redis用户名
    password = Column(String(64), nullable=False)  # redis密码
    db = Column(INT, nullable=False)  # redis库表
    # 是否是集群，默认为False,集群可不输入用户密码
    cluster = Column(Boolean, default=False, nullable=False)
    __tag__ = "Redis配置"
    __fields__ = (name, addr, username, password, db, cluster)
    __alias__ = dict(name="连接名称", env="环境", addr="连接地址", username="用户名", password="用户密码", db="库名", cluster="集群")

    def __init__(self, env, name, addr, user, username, password, db, cluster):
        super().__init__(user, id=id)
        self.env = env
        self.name = name
        self.addr = addr
        self.password = password
        self.username = username
        self.db = db
        self.cluster = cluster
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/20 09:11
# @Author  : 冉勇
# @Site    : 
# @File    : basic.py
# @Software: PyCharm
# @desc    : 基本的方法
import json
from datetime import datetime
from decimal import Decimal  # decimal模块用于十进制数学计算
from typing import Tuple  # 引入类型的元组
from sqlalchemy import INT, Column, BIGINT, TIMESTAMP
from webapi.app.models import Base
from webapi.config import Config


class SakuraBase(Base):
    id = Column(INT, primary_key=True)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)
    deleted_at = Column(BIGINT, nullable=False)
    created_user = Column(INT, nullable=False, default=0)
    update_user = Column(INT, nullable=False)
    __abstract__ = True
    __fields__: Tuple[Column] = [id]
    __tag__ = "未定义"
    __alias__ = dict(name="名称")
    __show__ = 1

    def __init__(self, user, id=None):
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.created_user = user
        self.update_user = user
        self.deleted_at = 0

    def serialize(self, *ignore):
        """
        :param ignore:
        :return:
        """
        data = {}
        for c in self.__table__.columns:
            if c.name in ignore:
                # 如果字段忽略，则不进行转换
                continue
            val = getattr(self, c.name)
            if isinstance(val, datetime):
                data[c.name] = val.strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(val, Decimal):
                data[c.name] = str(val)
            else:
                data[c.name] = val
        return json.dumps(data, ensure_ascii=False)


class SakuraRelationField(object):
    def __init__(self, field, foreign=None):
        self.field = field
        self.foreign = foreign


def init_relation(model, *data: SakuraRelationField):
    setattr(model, Config.RELATION, data)

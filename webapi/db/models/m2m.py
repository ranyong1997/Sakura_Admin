#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/4 11:21
# @Author  : 冉勇
# @Site    : 
# @File    : m2m.py
# @Software: PyCharm
# @desc    :
from sqlalchemy import Table, Integer, Column, ForeignKey

from webapi.db.config import Base

post_category = Table(
    'post_category',  # 第三张表名
    Base.metadata,  # 元类的数据
    Column('post_id', Integer, ForeignKey('Post.id'), primary_key=True),  # 关联文章的字段
    Column('category_id', Integer, ForeignKey('Category.id'), primary_key=True),  # 标签的外键关联字段
    # 两字段primary_key都等于True，组合主键唯一，防止内容一样
)

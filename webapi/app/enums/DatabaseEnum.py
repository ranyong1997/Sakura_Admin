#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/20 09:22
# @Author  : 冉勇
# @Site    : 
# @File    : DatabaseEnum.py
# @Software: PyCharm
# @desc    : 数据库类型枚举
from enum import IntEnum


class DatabaseEnum(IntEnum):
    """
    数据库类型枚举
    """
    MYSQL = 0
    POSTGRESQL = 1

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/3 17:16
# @Author  : 冉勇
# @Site    : 
# @File    : ConstructorEnum.py
# @Software: PyCharm
# @desc    : 构造函数枚举->前置条件类型
from enum import IntEnum


class ConstructorType(IntEnum):
    testcase = 0
    sql = 1
    redis = 2
    py_script = 3
    http = 4

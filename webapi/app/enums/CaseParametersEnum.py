#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/5 11:08
# @Author  : 冉勇
# @Site    : 
# @File    : CaseParametersEnum.py
# @Software: PyCharm
# @desc    : 用例参数枚举
from enum import IntEnum


class CaseParametersEnum(IntEnum):
    TEXT = 0
    JSON = 1
    HEADER = 2
    COOKIE = 3
    STATUS_CODE = 4

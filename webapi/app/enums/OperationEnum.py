#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/20 11:45
# @Author  : 冉勇
# @Site    : 
# @File    : OperationEnum.py
# @Software: PyCharm
# @desc    : 日志类型
from enum import IntEnum


class OperationType(IntEnum):
    INSERT = 0
    UPDATE = 1
    DELETE = 2
    EXECUTE = 3
    STOP = 4

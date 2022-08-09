#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/9 10:11
# @Author  : 冉勇
# @Site    : 
# @File    : GconfigEnum.py
# @Software: PyCharm
# @desc    : 全局配置枚举
from enum import IntEnum


class GConfigParserEnum(IntEnum):
    string = 0
    json = 1
    yaml = 2


class GConfigType(IntEnum):
    case = 0
    constructor = 1
    asserts = 2

    @staticmethod
    def text(val):
        if val == 0:
            return "用例"
        if val == 1:
            return "前后置条件"
        return "断言"

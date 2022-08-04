#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/4 11:45
# @Author  : 冉勇
# @Site    : 
# @File    : RequestBodyEnum.py
# @Software: PyCharm
# @desc    : 请求类型
from enum import IntEnum


class BodyType(IntEnum):
    none = 0
    json = 1
    form = 2
    x_form = 3
    binary = 4
    graphQL = 5

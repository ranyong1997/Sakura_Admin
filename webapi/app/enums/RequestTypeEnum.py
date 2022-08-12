#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/12 15:04
# @Author  : 冉勇
# @Site    : 
# @File    : RequestTypeEnum.py
# @Software: PyCharm
# @desc    : 请求类型枚举
from enum import IntEnum


class RequestType(IntEnum):
    http = 1
    grpc = 2
    dubbo = 3
    websocket = 4

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/9 10:15
# @Author  : 冉勇
# @Site    : 
# @File    : NoticeEnum.py
# @Software: PyCharm
# @desc    : 通知类型
from enum import IntEnum


class NoticeType(IntEnum):
    EMAIL = 0
    DINGDING = 1
    WECHAT = 2
    FEISHU = 3

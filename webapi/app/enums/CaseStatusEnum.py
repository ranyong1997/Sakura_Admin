#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/12 15:01
# @Author  : 冉勇
# @Site    : 
# @File    : CaseStatusEnum.py
# @Software: PyCharm
# @desc    : 用例状态枚举
from enum import IntEnum


class CaseStatus(IntEnum):
    debugging = 1  # 调试中
    closed = 2  # 暂时关闭
    running = 3  # 正常运作

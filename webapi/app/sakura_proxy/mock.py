#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/21 16:41
# @Author  : 冉勇
# @Site    : 
# @File    : mock.py
# @Software: PyCharm
# @desc    : mock数据
from pymock import Mock


class SakuraMock(object):
    def __init__(self):
        self.mock = Mock()

    def request(self, flow):
        pass

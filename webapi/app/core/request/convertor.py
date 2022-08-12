#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/12 14:25
# @Author  : 冉勇
# @Site    : 
# @File    : convertor.py
# @Software: PyCharm
# @desc    : 转换器
from typing import List
from webapi.app.schema.request import RequestInfo


# request转换器,支持har
class Convertor(object):
    @staticmethod
    def convert(file, regex: str = None) -> List[RequestInfo]:
        raise NotImplementedError

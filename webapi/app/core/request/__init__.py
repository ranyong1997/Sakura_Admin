#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/12 14:24
# @Author  : 冉勇
# @Site    : 
# @File    : __init__.py.py
# @Software: PyCharm
# @desc    : har转换器初始化
from webapi.app.core.request.convertor import Convertor
from webapi.app.core.request.har_convertor import HarConvertor
from webapi.app.enums.ConvertorEnum import CaseConvertorType


def get_convertor(c: CaseConvertorType) -> (Convertor.convert, str):
    """
    获取转换器
    :param c:
    :return:
    """
    if c == CaseConvertorType.har:
        return HarConvertor.convert, CaseConvertorType.har.name
    return None, ""

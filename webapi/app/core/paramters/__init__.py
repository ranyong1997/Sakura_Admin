#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/4 17:17
# @Author  : 冉勇
# @Site    : 
# @File    : __init__.py.py
# @Software: PyCharm
# @desc    :
from webapi.app.core.paramters.jsonpath_parser import JSONPathParser
from webapi.app.core.paramters.kv_parser import HeaderParser, CookieParser
from webapi.app.core.paramters.regex_parser import RegexParser
from webapi.app.core.paramters.status_code_parser import StatusCodeParser
from webapi.app.enums.CaseParametersEnum import CaseParametersEnum


def ParametersParser(parameter_type: CaseParametersEnum):
    if parameter_type == CaseParametersEnum.TEXT:
        return RegexParser.parse
    if parameter_type == CaseParametersEnum.JSON:
        return JSONPathParser.parse
    if parameter_type == CaseParametersEnum.HEADER:
        return HeaderParser.parse
    if parameter_type == CaseParametersEnum.COOKIE:
        return CookieParser.parse
    return StatusCodeParser.parse


#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/5 11:04
# @Author  : 冉勇
# @Site    : 
# @File    : status_code_parser.py
# @Software: PyCharm
# @desc    : 状态码解析器
import json
from webapi.app.core.paramters.parser import Parser


class StatusCodeParser(Parser):
    @staticmethod
    def parse(source: dict, expression: str = "", idx: str = None) -> str:
        return json.dumps(source.get("status_code"))

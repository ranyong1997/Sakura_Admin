#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/4 17:46
# @Author  : 冉勇
# @Site    : 
# @File    : kv_parser.py
# @Software: PyCharm
# @desc    : 参数提取
import json
from typing import Any
import jsonpath
from webapi.app.core.paramters.parser import Parser
from webapi.app.excpetions.CaseParametersException import CaseParametersException


class HeaderParser(Parser):
    @staticmethod
    def get_source(data: dict):
        return json.loads(data.get("response_headers"))

    @classmethod
    def parse(cls, source: dict, expression: str = "", idx: str = None) -> Any:
        if not source or not expression:
            raise CaseParametersException("解析出参数失败，源或表达式为空")
        try:
            source = cls.get_source(source)
            results = jsonpath.jsonpath(source, expression)
            if results is False:
                if not source and expression == "$..*":
                    # 说明想要全匹配并且没数据,直接返回data
                    return source
                raise CaseParametersException("jsonpath 匹配失败，请检查您的response或jsonpath")
            return Parser.parse_result(results, idx)
        except CaseParametersException as e:
            raise e
        except Exception as e:
            raise CaseParametersException(f"解析json数据错误，请检查jsonpath或json:{str(e)}") from e


class CookieParser(HeaderParser):
    @staticmethod
    def get_source(data: dict):
        return json.loads(data.get("cookies"))

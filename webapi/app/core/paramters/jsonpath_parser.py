#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/4 17:18
# @Author  : 冉勇
# @Site    : 
# @File    : jsonpath_parser.py
# @Software: PyCharm
# @desc    : jsonpath解析器
import json
from functools import lru_cache
from typing import Any
import jsonpath
from webapi.app.core.paramters.parser import Parser
from webapi.app.excpetions.CaseParametersException import CaseParametersException


class JSONPathParser(Parser):
    @staticmethod
    def parse(source: dict, expression: str = "", idx: str = None) -> Any:
        source = source.get("response")
        if not source or not expression:
            raise CaseParametersException("解析出参数失败，源或表达式为空")
        try:
            data = JSONPathParser.get_object(source)
            results = jsonpath.jsonpath(data, expression)
            if results is False:
                if not data and expression == "$..*":
                    # 说明想要全匹配并且没有数据,直接返回data
                    return json.dumps(data, ensure_ascii=False)
                raise CaseParametersException("jsonpath 匹配失败，请检查您的response或者jsonpath")
            return Parser.parse_result(results, idx)
        except CaseParametersException as e:
            raise e
        except Exception as e:
            raise CaseParametersException(f"解析json数据错误，请检查jsonpath或json:{str(e)}") from e

    @staticmethod
    @lru_cache()
    def get_object(json_str):
        return json.loads(json_str)

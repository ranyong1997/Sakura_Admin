#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/5 10:57
# @Author  : 冉勇
# @Site    : 
# @File    : regex_parser.py
# @Software: PyCharm
# @desc    : 文本的正则表达式
import re
from typing import Any
from webapi.app.core.paramters.parser import Parser
from webapi.app.excpetions.CaseParametersException import CaseParametersException


class RegexParser(Parser):
    @staticmethod
    def parse(source: dict, expression: str = "", idx: str = None) -> Any:
        try:
            source = source.get("response")
            if not source or not expression:
                raise CaseParametersException("解析出参数失败，源或表达式为空")
            if idx is None:
                raise CaseParametersException("索引为空，您必须为正则表达式匹配结果提供索引")
            pattern = re.compile(expression)
            result = re.findall(pattern, source)
            if len(result) == 0:
                raise CaseParametersException(f"正则表达式匹配失败，请检查您的正则表达式:{expression}")
            return Parser.parse_result(result, idx)
        except CaseParametersException as e:
            raise e
        except Exception as e:
            raise CaseParametersException(f"解析正则表达式文本错误，请检查正则表达式或文本:{str(e)}") from e

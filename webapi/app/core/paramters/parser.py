#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/4 17:19
# @Author  : 冉勇
# @Site    : 
# @File    : parser.py
# @Software: PyCharm
# @desc    : 解析器
import json
import random
from typing import Any
from webapi.app.excpetions.CaseParametersException import CaseParametersException


class Parser(object):
    @staticmethod
    def parse(source: dict, expression: str = "", idx: str = None) -> Any:
        raise NotImplementedError

    @staticmethod
    def parse_result(data: list, match_index: str = None):
        """
        解析结果
        :param data:
        :param match_index:
        :return:
        """
        if not data:
            return "null"
        if match_index is not None:
            if match_index.isdigit():
                idx = int(match_index)
                # 如果是数字
                length = len(data)
                if idx >= length or idx < -length:
                    raise CaseParametersException(f"长度为:{length},索引不在[{-length},{length}]")
                return json.dumps(data[idx], ensure_ascii=False)
            if match_index.lower() == 'random':
                # 随机选取
                return json.dumps(random.choice(data), ensure_ascii=False)
            if match_index.lower() == 'all':
                return json.dumps(data, ensure_ascii=False)
            raise CaseParametersException(f"错误的索引:{match_index},不能随机")
        return json.dumps(data, ensure_ascii=False)

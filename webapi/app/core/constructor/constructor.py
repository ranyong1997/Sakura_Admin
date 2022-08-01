#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/1 11:30
# @Author  : 冉勇
# @Site    : 
# @File    : constructor.py
# @Software: PyCharm
# @desc    : 构造器
from abc import ABC
from webapi.app.models.constructor import Constructor


class ConstructorAbstract(ABC):
    @staticmethod
    def run(executor, env, index, path, params, req_params, constructor: Constructor, **kwargs):
        pass

    @staticmethod
    def get_name(constructor):
        return '后置条件' if constructor.suffix else '前置条件'

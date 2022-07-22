#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/22 10:32
# @Author  : 冉勇
# @Site    : 
# @File    : base.py
# @Software: PyCharm
# @desc    : 架构基础
from webapi.app.excpetions.ParamsException import ParamsError


class SakuraModel(object):
    @staticmethod
    def not_empty(v):
        if isinstance(v, str) and len(v.strip()) == 0:
            raise ParamsError("不能为空！")
        if not isinstance(v, int) and not v:
            raise ParamsError("不能为空！")
        return v

    @property
    def parameters(self):
        raise NotImplementedError

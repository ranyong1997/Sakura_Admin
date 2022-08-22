#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/19 15:11
# @Author  : 冉勇
# @Site    : 
# @File    : ProjectEnum.py
# @Software: PyCharm
# @desc    : 角色枚举

class ProjectRoleEnum:
    MEMBER = 0
    ADMIN = 1

    @staticmethod
    def name(role):
        if role == 1:
            return "组长"
        if role == 0:
            return "组员"
        return None

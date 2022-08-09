#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/9 10:23
# @Author  : 冉勇
# @Site    : 
# @File    : case_logger.py
# @Software: PyCharm
# @desc    : 测试用例日志
from datetime import datetime


class CaseLog(object):
    def __init__(self):
        self.log = list()

    def append(self, content, end=True):
        if end:
            self.log.append(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]:步骤结束 -> {content}")
        else:
            self.log.append(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]:步骤开始 -> {content}")
    def o_append(self, content):
        """
        原始append
        :param content:
        :return:
        """
        self.log.append(content)

    def join(self):
        return "\n".join(self.log)

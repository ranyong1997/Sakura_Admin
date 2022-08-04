#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/4 15:24
# @Author  : 冉勇
# @Site    : 
# @File    : notification.py
# @Software: PyCharm
# @desc    : 通知
class Notification(object):
    @staticmethod
    def send_msg(subject, content, attachments=None, *receiver):
        raise NotImplementedError

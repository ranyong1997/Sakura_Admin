#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/23 10:30
# @Author  : 冉勇
# @Site    : 
# @File    : wss_msg.py
# @Software: PyCharm
# @desc    : 消息封装
from webapi.app.enums.MessageEnum import WebSocketMessageEnum


class WebSocketMessage(object):
    @staticmethod
    def msg_count(count=1, total=False):
        """
        消息统计
        :param count:
        :param total:
        :return:
        """
        return dict(type=WebSocketMessageEnum.COUNT, count=count, total=total)

    @staticmethod
    def desktop_msg(title, content=''):
        """
        桌面消息
        :param title:
        :param content:
        :return:
        """
        return dict(type=WebSocketMessageEnum.DESKTOP, title=title, content=content)

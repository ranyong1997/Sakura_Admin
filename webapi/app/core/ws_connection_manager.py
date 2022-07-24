#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/23 10:41
# @Author  : 冉勇
# @Site    : 
# @File    : ws_connection_manager.py
# @Software: PyCharm
# @desc    :
from typing import TypeVar
from fastapi import WebSocket
from webapi.app.core.msg.wss_msg import WebSocketMessage
from webapi.app.crud.notification import NotificationDao


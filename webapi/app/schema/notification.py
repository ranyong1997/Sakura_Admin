#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/28 10:38
# @Author  : 冉勇
# @Site    : 
# @File    : notification.py
# @Software: PyCharm
# @desc    : 通知
from typing import List
from pydantic import BaseModel


class NotificationForm(BaseModel):
    personal: List[int] = None
    broadcast: List[int] = None

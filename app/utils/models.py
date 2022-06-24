#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/6/24 17:35
# @Author  : 冉勇
# @Site    : 
# @File    : models.py
# @Software: PyCharm
# @desc    :
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text, DateTime
from datetime import datetime
from config import EVENT

if EVENT == "test":
    from app.utils.testDatabase import Base, engine

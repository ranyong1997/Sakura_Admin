#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/6/25 8:54 AM
# @Author  : ranyong
# @Site    : 
# @File    : get_db.py
# @Software: PyCharm

from app.utils.database import *
from app.utils.testDatabase import TestingSessionLocal
from config import EVENT


def get_test_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db_pro():
    """
    每一个请求处理完毕后会关闭当前连接，不同的请求使用不同的连接
    :return:
    """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


get_db = get_test_db if EVENT == "test" else get_db_pro

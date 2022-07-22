#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/22 15:59
# @Author  : 冉勇
# @Site    : 
# @File    : RequestException.py
# @Software: PyCharm
# @desc    : 请求例外
from fastapi import HTTPException


class AuthException(HTTPException):
    pass


class PermissionException(HTTPException):
    pass

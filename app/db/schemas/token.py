#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/4 14:50
# @Author  : 冉勇
# @Site    : 
# @File    : token.py
# @Software: PyCharm
# @desc    :
from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[int] = None

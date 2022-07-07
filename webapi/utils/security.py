#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/4 17:06
# @Author  : 冉勇
# @Site    : 
# @File    : security.py
# @Software: PyCharm
# @desc    :
from typing import Union, Any
from datetime import datetime, timedelta

from jose import jwt
from webapi.setting import settings

ALGORITHM = 'HS256'


def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {
        'exp': expire,
        'sub': str(subject)
    }
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=ALGORITHM
    )
    return encoded_jwt

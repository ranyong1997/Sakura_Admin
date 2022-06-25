#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/6/25 9:41 AM
# @Author  : ranyong
# @Site    : 
# @File    : jsontools.py
# @Software: PyCharm

from fastapi import status
from fastapi.responses import JSONResponse, Response
from typing import Union


def reponse(*, code=200, data: Union[list, dict, str], message="Success") -> Response:
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'code': code,
            'message': message,
            'data': data,
        }
    )


def resp_400(*, data: str = None, message: str = "BAD REQUEST") -> Response:
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            'code': 400,
            'message': message,
            'data': data,
        }
    )

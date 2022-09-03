#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/20 11:40
# @Author  : 冉勇
# @Site    : 
# @File    : __init__.py.py
# @Software: PyCharm
# @desc    : 路由初始化[身份鉴权]
import asyncio
from fastapi import Header
from starlette import status
from webapi.app.crud.auth.UserDao import UserDao
from webapi.app.excpetions.RequestException import AuthException, PermissionException
from webapi.app.handler.fatcory import SakuraResponse
from webapi.app.middleware.Jwt import UserToken
from webapi.app.models import async_session
from webapi.app.utils.internal import synchronize_async_helper
from webapi.config import Config

FORBIDDEN = "对不起, 你没有足够的权限"


class Permission:
    def __init__(self, role: int = Config.MEMBER):
        self.role = role

    async def __call__(self, token: str = Header(...)):
        if not token:
            raise AuthException(status.HTTP_200_OK, "用户信息身份认证失败, 请检查")
        try:
            user_info = UserToken.parse_token(token)
            if user_info.get("role", 0) < self.role:
                raise PermissionException(status.HTTP_200_OK, FORBIDDEN)
            user = await UserDao.query_user(user_info['id'])
            if user is None:
                raise Exception("用户不存在")
            user_info = SakuraResponse.model_to_dict(user, "password")
        except PermissionException as e:
            raise e
        except Exception as e:
            raise AuthException(status.HTTP_200_OK, str(e))
        return user_info


async def get_session():
    """
    获取异步session
    :return:
    """
    async with async_session() as session:
        yield session

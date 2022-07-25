#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/25 15:32
# @Author  : 冉勇
# @Site    : 
# @File    : user.py
# @Software: PyCharm
# @desc    : 用户管理【github登录】路由
import requests
from fastapi import APIRouter, Depends
from starlette import status
from webapi.app.crud.auth.UserDao import UserDao
from webapi.app.excpetions.RequestException import AuthException
from webapi.app.handler.fatcory import SakuraResponse
from webapi.app.middleware.Jwt import UserToken
from webapi.app.routers import Permission, FORBIDDEN
from webapi.app.routers.auth.user_schema import UserDto, UserForm
from webapi.app.schema.user import UserUpdateForm
from webapi.config import Config

router = APIRouter(perfix="/auth")


# router注册的函数都会自带 /auth,所以url是/auth/register
@router.post("/register")
async def register(user: UserDto):
    try:
        await UserDao.register_user(**user.dict())
        return SakuraResponse.success(msg="🎉🎉注册成功,请登录")
    except Exception as e:
        return SakuraResponse.failed(e)


@router.post("/login")
async def login(data: UserForm):
    try:
        user = await UserDao.login(data.username, data.password)
        user = SakuraResponse.model_to_dict(user, "password")
        expire, token = UserToken.get_token(user)
        return SakuraResponse.success(dict(token=token, user=user, expire=expire), msg="🎊🎊登录成功")
    except Exception as e:
        return SakuraResponse.failed(e)


@router.get("/listUser")
async def list_users(user_info=Depends(Permission())):
    try:
        user = await UserDao.list_user_touch()
        return SakuraResponse.success(user, exclude=("password",))

    except Exception as e:
        return SakuraResponse.failed(str(e))


@router.get("/github/login")
async def login_with_github(code: str):
    try:
        code = code.rstrip("#/")
        with requests.Session() as session:
            r = session.get(Config.GITHUB_ACCESS,
                            params=dict(client_id=Config.CLIENT_ID, client_secret=Config.SECRET_KEY, code=code),
                            timeout=8)
            token = r.text.split("&")[0].split("=")[1]
            res = session.get(Config.GITHUB_USER, headers={"Authorization": f"token{token}"}, timeout=8)
            user_info = res.json()
            user = await UserDao.register_for_github(user_info.get("login"), user_info.get("name"),
                                                     user_info.get("email"), user_info.get("avatar_url"))
            user = SakuraResponse.model_to_dict(user, "password")
            expire, token = UserToken.get_token(user)
            return SakuraResponse.success(dict(token=token, user=user, expire=expire), msg="🎊🎊登录成功")
    except Exception:
        return SakuraResponse.failed(code=110, msg="登录超时,请稍后再试")


@router.post("/update")
async def update_user_info(user_info: UserForm, user=Depends(Permission(Config.MEMBER))):
    try:
        if user['role'] != Config.ADMIN:
            if user['id'] != user_info.id:
                # 既不是改自己资料,也不是超管
                return SakuraResponse.failed(FORBIDDEN)
            user_info.role = None
        user = await UserDao.update_user(user_info, user['id'])
        return SakuraResponse.success(user, exclude=("password", "phone", "email"))
    except AuthException as e:
        raise e
    except Exception as e:
        return SakuraResponse.failed(e)


@router.get("/query")
async def query_user_info(token: str):
    try:
        if not token:
            raise AuthException(status.HTTP_200_OK, "🍥🍥token不存在!")
        user_info = UserToken.parse_token(token)
        user = await UserDao.query_user(user_info['id'])
        if user is None:
            return SakuraResponse.failed("🍥🍥用户不存在")
        return SakuraResponse.success(user, exclude=("password",))
    except Exception as e:
        return SakuraResponse.failed(e)


@router.delete("/delete")
async def delete_user(id: int, user=Depends(Permission(Config.ADMIN))):
    try:
        user = await UserDao.delete_user(id, user['id'])
        return SakuraResponse.success(user)
    except Exception as e:
        return SakuraResponse.failed(e)

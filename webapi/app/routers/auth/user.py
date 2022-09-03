#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/25 15:32
# @Author  : 冉勇
# @Site    : 
# @File    : user.py
# @Software: PyCharm
# @desc    : 用户管理路由
import asyncio
import requests
from fastapi import APIRouter, Depends
from starlette import status
from webapi.app.core.msg.mail import Email
from webapi.app.crud.auth.UserDao import UserDao
from webapi.app.excpetions.RequestException import AuthException
from webapi.app.handler.fatcory import SakuraResponse
from webapi.app.middleware.Jwt import UserToken
from webapi.app.routers import Permission, FORBIDDEN
from webapi.app.schema.user import UserUpdateForm, UserForm, UserDto, ResetPwdForm
from webapi.app.utils.des import Des
from webapi.config import Config

router = APIRouter(prefix="/auth")


# router注册的函数都会自带 /auth,所以url是/auth/register
@router.post("/register", summary="注册", tags=['User'])
async def register(user: UserDto):
    try:
        await UserDao.register_user(**user.dict())
        return SakuraResponse.success(msg="🎉🎉注册成功,请登录")
    except Exception as e:
        return SakuraResponse.failed(e)


@router.post("/login", summary="登录", tags=['User'])
async def login(data: UserForm):
    try:
        user = await UserDao.login(data.username, data.password)
        user = SakuraResponse.model_to_dict(user, "password")  # 排除显示密码
        expire, token = UserToken.get_token(user)
        print("expire-->", expire, "token-->", token)
        return SakuraResponse.success(dict(token=token, user=user, expire=expire), msg="🎊🎊登录成功")
    except Exception as e:
        return SakuraResponse.failed(e)


@router.get("/listUser", summary="列出用户", tags=['User'])
async def list_users(user_info=Depends(Permission())):
    try:
        user = await UserDao.list_users()
        return SakuraResponse.success(user, exclude=("password",))
    except Exception as e:
        return SakuraResponse.failed(str(e))


@router.get("/github/login", summary="github 第三方登录", tags=['User'])
async def login_with_github(code: str):
    try:
        code = code.rstrip("#/")
        with requests.Session() as session:
            r = session.get(Config.GITHUB_ACCESS,
                            params=dict(client_id=Config.CLIENT_ID, client_secret=Config.SECRET_KEY, code=code),
                            timeout=8)
            token = r.text.split("&")[0].split("=")[1]
            res = session.get(Config.GITHUB_USER, headers={"Authorization": "token {}".format(token)}, timeout=8)
            user_info = res.json()
            user = await UserDao.register_for_github(user_info.get("login"), user_info.get("name"),
                                                     user_info.get("email"), user_info.get("avatar_url"))
            user = SakuraResponse.model_to_dict(user, "password")
            expire, token = UserToken.get_token(user)
            return SakuraResponse.success(dict(token=token, user=user, expire=expire), msg="🎊🎊登录成功")
    except Exception:
        return SakuraResponse.failed(code=110, msg="登录超时,请稍后再试")


@router.post("/update", summary="更新密码,手机,邮箱", tags=['User'])
async def update_user_info(user_info: UserUpdateForm, user=Depends(Permission(Config.MEMBER))):
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


@router.get("/query", summary="查询账号", tags=['User'])
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


@router.delete("/delete", summary="删除账号", tags=['User'])
async def delete_user(id: int, user=Depends(Permission(Config.ADMIN))):
    try:
        user = await UserDao.delete_user(id, user['id'])
        return SakuraResponse.success(user)
    except Exception as e:
        return SakuraResponse.failed(e)


@router.post("/reset", summary="重置用户密码", tags=['User'])
async def reset_user(form: ResetPwdForm):
    email = Des.des_decrypt(form.token)
    await UserDao.reset_password(email, form.password)
    return SakuraResponse.success()


@router.get("/reset/generate/{email}", summary="生成重置密码链接", tags=['User'])
async def generate_reset_url(email: str):
    try:
        user = await UserDao.query_user_by_email(email)
        if user is not None:
            # 说明邮件存在,发送邮件
            em = Des.des_encrypt(email)
            link = f"""https://sakura.fun/#/user/resetPassword?token={em}"""
            render_html = Email.render_html(Config.PASSWORD_HTML_PATH, link=link, name=user.name)
            asyncio.create_task(Email.send_msg("重置你的用户密码", render_html, None, email))
        return SakuraResponse.success(None)
    except Exception as e:
        return SakuraResponse.failed(str(e))


@router.get("/reset/check/{token}", summary="检测生成的链接是否正确", tags=['User'])
async def check_reset_url(token: str):
    try:
        email = Des.des_decrypt(token)
        return SakuraResponse.success(email)
    except Exception as e:
        return SakuraResponse.failed("重置链接不存在,请不要无脑尝试", {e})

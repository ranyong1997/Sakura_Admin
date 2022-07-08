#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/6 15:02
# @Author  : 冉勇
# @Site    : 
# @File    : user_router.py
# @Software: PyCharm
# @desc    : 用户路由
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from webapi.db.dals.user_dal import User, UserDAL
from webapi.db.schemas.token import Token
from webapi.utils.dependencies import DALGetter, get_current_user
from webapi.setting import settings
from webapi.utils import security

router = APIRouter()


@router.post('/login/access_token/', tags=['用户'],
             response_model=Token, status_code=status.HTTP_201_CREATED)
async def login_access_token(
        dal: UserDAL = Depends(DALGetter(UserDAL)),  # 获取用户数据访问层
        form_data: OAuth2PasswordRequestForm = Depends()  # OAuth2PasswordRequestForm表单数据
):
    user = await dal.authenticate(
        username=form_data.username,  # 用户名
        password=form_data.password  # 密码
    )
    if not user:
        raise HTTPException(
            status_code=400, detail="错误的帐号或密码"
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        'access_token': security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer"
    }


@router.get('/login/getinfo/', tags=['用户'])
async def login_getinfo(
        current_user: User = Depends(get_current_user)
):
    data = {
        '用户名': current_user.username,
        '昵称': current_user.nickname,
        '角色': ['admin']
    }
    return JSONResponse(content=data, status_code=status.HTTP_200_OK)

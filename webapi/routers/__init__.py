#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/6/22 17:10
# @Author  : 冉勇
# @Site    : 
# @File    : __init__.py.py
# @Software: PyCharm
# @desc    :
from fastapi import APIRouter

from . import category_router  # 导入分类路由
from . import post_router  # 导入post路由
from . import user_router  # 导入用户路由
from . import comment_router  # 导入评论路由

api_router = APIRouter()
api_router.include_router(user_router.router, tags=['User'], prefix='/admin')  # 挂载用户路由
api_router.include_router(post_router.router, tags=['Post'], prefix='/posts')  # 挂载post路由
api_router.include_router(category_router.router, tags=['Category'], prefix='/categories')  # 挂载分类路由
api_router.include_router(comment_router.router, tags=['Comment'], prefix='/comments')  # 挂载评论路由

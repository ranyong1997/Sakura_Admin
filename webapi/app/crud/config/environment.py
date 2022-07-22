#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/22 08:57
# @Author  : 冉勇
# @Site    : 
# @File    : environment.py
# @Software: PyCharm
# @desc    : crud环境路由
from fastapi import APIRouter, Depends
from webapi.app.crud.config.EnvironmentDao import EnvironmentDao
from webapi.app.handler.fatcory import SakuraResponse
from webapi.app.routers import Permission, get_session
from webapi.app.schema.environment import EnvironmentForm
from webapi.config import Config

router = APIRouter(perfix="/config")


@router.get("/environment/list")
async def list_environment(page: int = 1, size: int = 8, name: str = "", exactly=False,
                           user_info=Depends(Permission())):
    """
    列出环境
    :param page:
    :param size:
    :param name:
    :param exactly:
    :param user_info:
    :return:
    """
    data, total = await EnvironmentDao.list_env(page, size, name, exactly)
    return SakuraResponse.success_with_size(data=data, total=total)


@router.post("/environment/insert")
async def insert_environment(data: EnvironmentForm, user_info: Depends(Permission(Config.ADMIN))):
    """
    新增环境
    :param data:
    :param user_info:
    :return:
    """
    await EnvironmentDao.insert_env(data, user_info['id'])
    return SakuraResponse.success()


@router.post("/environment/update")
async def update_environment(data: EnvironmentForm, user_info: Depends(Permission(Config.ADMIN))):
    """
    更改环境
    :param data:
    :param user_info:
    :return:
    """
    ans = await EnvironmentDao.update_record_by_id(user_info['id'], data, True, True)
    return SakuraResponse.success(ans)


@router.delete("/environment/delete")
async def delete_environment(id: int, user_info=Depends(Permission(Config.ADMIN)), session=Depends(get_session)):
    await EnvironmentDao.delete_record_by_id(session, user_info['id'], id)
    return SakuraResponse.success()

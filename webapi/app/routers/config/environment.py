#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/20 11:41
# @Author  : 冉勇
# @Site    : 
# @File    : environment.py
# @Software: PyCharm
# @desc    : 环境配置(路由)
from fastapi import APIRouter, Depends
from webapi.app.crud.config.EnvironmentDao import EnvironmentDao
from webapi.app.handler.fatcory import SakuraResponse
from webapi.app.routers import Permission, get_session
from webapi.app.schema.environment import EnvironmentForm
from webapi.config import Config

router = APIRouter(prefix="/config")


@router.get("/environment/list", summary="列出环境", tags=['Environment'])
async def list_environment(page: int = 1, size: int = 8, name: str = "", exactly=False,
                           user_info=Depends(Permission())):
    data, total = await EnvironmentDao.list_env(page, size, name, exactly)
    return SakuraResponse.success_with_size(data=data, total=total)


@router.post("/environment/insert", summary="新增环境", tags=['Environment'])
async def insert_environment(data: EnvironmentForm, user_info=Depends(Permission(Config.ADMIN))):
    await EnvironmentDao.insert_env(data, user_info['id'])
    return SakuraResponse.success()


@router.post("/environment/update", summary="更新环境", tags=['Environment'])
async def update_environment(data: EnvironmentForm, user_info=Depends(Permission(Config.ADMIN))):
    ans = await EnvironmentDao.update_record_by_id(user_info['id'], data, True, True)
    return SakuraResponse.success(ans)


@router.delete("/environment/delete", summary="删除环境", tags=['Environment'])
async def delete_environment(id: int, user_info=Depends(Permission(Config.ADMIN)), session=Depends(get_session)):
    await EnvironmentDao.delete_record_by_id(session, user_info['id'], id)
    return SakuraResponse.success()

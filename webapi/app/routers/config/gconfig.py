#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/25 16:28
# @Author  : 冉勇
# @Site    : 
# @File    : gconfig.py
# @Software: PyCharm
# @desc    : 全局配置(路由)
from fastapi import Depends
from webapi.app.crud.config.GConfigDao import GConfigDao
from webapi.app.handler.fatcory import SakuraResponse
from webapi.app.routers import Permission, get_session
from webapi.app.routers.config.environment import router
from webapi.app.schema.gconfig import GConfigForm
from webapi.config import Config


@router.get("/gconfig/list", summary="列出全局配置", tags=['Gconfig'])
async def list_gconfig(page: int = 1, size: int = 8, env=None, key: str = "", _=Depends(Permission())):
    data, total = await GConfigDao.list_record_with_pagination(page, size, env=env, key=key)
    return SakuraResponse.success_with_size(data=data, total=total)


@router.post("/gconfig/insert", summary="新增全局配置", tags=['Gconfig'])
async def insert_gconfig(data: GConfigForm, user_info=Depends(Permission(Config.ADMIN))):
    await GConfigDao.insert_gconfig(data, user_info['id'])
    return SakuraResponse.success()


@router.post("/gconfig/update", summary="更新全局配置", tags=['Gconfig'])
async def update_gconfig(data: GConfigForm, user_info=Depends(Permission(Config.ADMIN))):
    await GConfigDao.update_record_by_id(user_info['id'], data, True, True)
    return SakuraResponse.success()


@router.delete("/gconfig/delete", summary="删除全局配置", tags=['Gconfig'])
async def delete_gconfig(id: int, user_info=Depends(Permission(Config.ADMIN)), session=Depends(get_session)):
    await GConfigDao.delete_record_by_id(session, user_info['id'], id, log=True)
    return SakuraResponse.success()

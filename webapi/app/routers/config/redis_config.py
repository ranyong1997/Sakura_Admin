#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/27 15:17
# @Author  : 冉勇
# @Site    : 
# @File    : redis_config.py
# @Software: PyCharm
# @desc    : redis配置
from fastapi import Depends
from starlette.background import BackgroundTasks
from webapi.app.crud.config.RedisConfigDao import SakuraRedisConfigDao
from webapi.app.handler.fatcory import SakuraResponse
from webapi.app.middleware.RedisManager import SakuraRedisManager
from webapi.app.models.redis_config import SakuraRedis
from webapi.app.routers import Permission, get_session
from webapi.app.routers.config.environment import router
from webapi.app.schema.online_redis import OnlineRedisForm
from webapi.app.schema.redis_config import RedisConfigForm
from webapi.config import Config


@router.get("/redis/list")
async def list_redis_config(name: str = '', addr: str = '', env: int = None,
                            cluster: bool = None, _=Depends(Permission(Config.MEMBER))):
    try:
        data = await SakuraRedisConfigDao.list_record(
            name=SakuraRedisConfigDao.like(name), addr=SakuraRedisConfigDao.like(addr),
            env=env, cluster=cluster
        )
        return SakuraResponse.success(data=data)
    except Exception as e:
        return SakuraResponse.failed(e)


@router.post("/redis/insert")
async def insert_redis_config(form: RedisConfigForm, user_info=Depends(Permission(Config.ADMIN))):
    try:
        query = await SakuraRedisConfigDao.query_record(name=form.name, env=form.env)
        if query is not None:
            raise Exception("数据已存在,请勿重复添加")
        data = SakuraRedis(**form.dict(), user=user_info['id'])
        result = await SakuraRedisConfigDao.insert(model=data, log=True)
        return SakuraResponse.success(data=result)
    except Exception as e:
        return SakuraResponse.failed(e)


@router.post("/redis/update")
async def update_redis_config(form: RedisConfigForm, background_tasks: BackgroundTasks,
                              user_info=Depends(Permission(Config.ADMIN))):
    try:
        result = await SakuraRedisConfigDao.update_record_by_id(user_info['id'], form, log=True)
        if result.cluster:
            background_tasks.add_task(SakuraRedisManager.refresh_redis_cluster, *(result.id, result.addr))
        else:
            background_tasks.add_task(SakuraRedisManager.refresh_redis_client,
                                      *(result.id, result.addr, result.password, result.db))
        return SakuraResponse.success(data=result)
    except Exception as e:
        return SakuraResponse.failed(e)


@router.get("/redis/delete")
async def delete_redis_config(id: int, background_tasks: BackgroundTasks, user_info=Depends(Permission(Config.ADMIN)),
                              session=Depends(get_session)):
    try:
        ans = await SakuraRedisConfigDao.delete_record_by_id(session, user_info['id'], id)
        # 更新缓存
        background_tasks.add_task(SakuraRedisManager.delete_client, *(id, ans.cluster))
        return SakuraResponse.success()
    except Exception as e:
        return SakuraResponse.failed(e)


@router.post("/redis/command")
async def test_redis_command(form: OnlineRedisForm):
    try:
        res = await SakuraRedisConfigDao.execute_command(form.command, id=form.id)
        return SakuraResponse.success(res)
    except Exception as e:
        return SakuraResponse.failed(e)

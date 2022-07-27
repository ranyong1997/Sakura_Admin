#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/27 10:35
# @Author  : 冉勇
# @Site    : 
# @File    : dbconfig.py
# @Software: PyCharm
# @desc    : 数据库配置(路由)
from fastapi import Depends
from webapi.app.crud.config.DbConfigDao import DbConfigDao
from webapi.app.handler.fatcory import SakuraResponse
from webapi.app.models import DatabaseHelper, db_helper
from webapi.app.routers import Permission
from webapi.app.routers.config.environment import router
from webapi.app.schema.database import DataBaseForm
from webapi.config import Config


@router.get("/dbconfig/list")
async def list_dbconfig(name: str = "", database: str = "", env: int = None,
                        user_info=Depends(Permission(Config.MEMBER))):
    try:
        data = await DbConfigDao.list_database(name, database, env)
        return SakuraResponse.success(data)
    except Exception as e:
        return SakuraResponse.failed(e)


@router.post("/dbconfig/insert")
async def insert_dbconfig(form: DataBaseForm, user_info=Depends(Permission(Config.ADMIN))):
    try:
        await DbConfigDao.insert_database(form, user_info['id'])
        return SakuraResponse.success()
    except Exception as e:
        return SakuraResponse.failed(e)


@router.post("/dbconfig/update")
async def insert_dbconfig(form: DataBaseForm, user_info=Depends(Permission(Config.ADMIN))):
    try:
        await DbConfigDao.insert_database(form, user_info['id'])
        return SakuraResponse.success()
    except Exception as e:
        return SakuraResponse.failed(e)


@router.get("dbconfig/delete", summary="删除数据库配置")
async def delete_dbconfig(id: int, user_info=Depends(Permission(Config.ADMIN))):
    try:
        await DbConfigDao.delete_database(id, user_info['id'])
        return SakuraResponse.success()
    except Exception as e:
        return SakuraResponse.failed(e)


@router.get("dbconfig/connect", summary="测试数据库连接")
async def connect_test(sql_type: int, host: str, port: int, username: str, password: str, database: str,
                       _=Depends(Permission(Config.ADMIN))):
    try:
        data = await db_helper.get_connection(sql_type, host, port, username, password, database)
        if data is None:
            raise Exception("测试连接失败")
        await DatabaseHelper.test_connection(data.get("session"))
        return SakuraResponse.success(msg="连接成功")
    except Exception as e:
        return SakuraResponse.failed(e)

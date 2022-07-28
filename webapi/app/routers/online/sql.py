#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/28 10:59
# @Author  : 冉勇
# @Site    : 
# @File    : sql.py
# @Software: PyCharm
# @desc    : 数据库[执行sql,查询配置信息]
from fastapi import APIRouter, Depends
from webapi.app.crud.config.DbConfigDao import DbConfigDao
from webapi.app.handler.fatcory import SakuraResponse
from webapi.app.routers import Permission
from webapi.app.schema.online_sql import OnlineSQLForm

router = APIRouter(prefix="/online")


@router.post('/sql')
async def execute_sql(data: OnlineSQLForm, _=Depends(Permission())):
    try:
        result = await DbConfigDao.online_sql(data.id, data.sql)
        columns = result = SakuraResponse.parse_sql_result(result)
        return SakuraResponse.success(data=dict(result=result, columns=columns))
    except Exception as e:
        return SakuraResponse.failed(e)


@router.get('/tables')
async def list_tables(_=Depends(Permission())):
    try:
        result, table_name = await DbConfigDao.query_database_and_tables()
        return SakuraResponse.success(dict(database=result, tables=table_name))
    except Exception as e:
        return SakuraResponse.failed(e)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/28 10:59
# @Author  : 冉勇
# @Site    : 
# @File    : sql.py
# @Software: PyCharm
# @desc    : 数据库[执行sql,查询配置信息]
from fastapi import APIRouter, Depends
from webapi.app.crud.config.DbConfigDao import DbConfigDao, SakuraSQLHistoryDao
from webapi.app.handler.fatcory import SakuraResponse
from webapi.app.models.database import SakuraDatabase
from webapi.app.models.environment import Environment
from webapi.app.models.sql_log import SakuraSQLHistory
from webapi.app.routers import Permission
from webapi.app.schema.database import DatabaseForm
from webapi.app.schema.online_sql import OnlineSQLForm

router = APIRouter(prefix="/online")


@router.post('/sql', summary="sql执行", tags=['Sql'])
async def execute_sql(data: OnlineSQLForm, user=Depends(Permission())):
    try:
        result, elapsed = await DbConfigDao.online_sql(data.id, data.sql)
        columns, result = SakuraResponse.parse_sql_result(result)
        await SakuraSQLHistoryDao.insert(model=SakuraSQLHistory(data.sql, elapsed, data.id, user['id']))
        return SakuraResponse.success(data=dict(result=result, columns=columns, elapsed=elapsed))
    except Exception as e:
        return SakuraResponse.failed(e)


@router.get("/history/query", summary="获取sql执行历史记录", tags=['Sql'])
async def query_sql_history(page: int = 1, size: int = 4, _=Depends(Permission())):
    data, total = await SakuraSQLHistory.list_with_pagination(page, size,
                                                              _sort=[SakuraSQLHistory.created_at.desc()],
                                                              _select=[SakuraDatabase, Environment],
                                                              _join=[(SakuraDatabase,
                                                                      SakuraDatabase.id == SakuraSQLHistory.database_id),
                                                                     (Environment,
                                                                      Environment.id == SakuraDatabase.env)])
    ans = []
    for history, database, env in data:
        database.env_info = env
        history.database = database
        ans.append(history)
    return SakuraResponse.success(dict(data=ans, total=total))


@router.get('/tables', summary="sql表", tags=['Sql'])
async def list_tables(_=Depends(Permission())):
    try:
        result, table_map = await DbConfigDao.query_database_and_tables()
        return SakuraResponse.success(dict(database=result, tables=table_map))
    except Exception as e:
        return SakuraResponse.failed(e)


@router.get("/database/list", summary="列出数据库", tags=['Sql'])
async def list_database(_=Depends(Permission())):
    try:
        result = await DbConfigDao.query_database_tree()
        return SakuraResponse.success(result)
    except Exception as e:
        return SakuraResponse.failed(e)


@router.post("/tables/list", summary="获取数据库表和字段", tags=['Sql'])
async def list_tables(form: DatabaseForm, _=Depends(Permission())):
    try:
        children, tables = await DbConfigDao.get_tables(form)
        return SakuraResponse.success(dict(children=children, tables=tables))
    except Exception as e:
        return SakuraResponse.failed(e)

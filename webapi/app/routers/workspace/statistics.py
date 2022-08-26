#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/25 11:28
# @Author  : 冉勇
# @Site    : 
# @File    : statistics.py
# @Software: PyCharm
# @desc    : 统计数据
from datetime import datetime, timedelta
from fastapi import Depends
from webapi.app.core.ws_connection_manager import ws_manage
from webapi.app.crud.statistics.dashboard import DashboardDao
from webapi.app.crud.test_case.TestCaseDao import TestCaseDao
from webapi.app.handler.fatcory import SakuraResponse
from webapi.app.routers import Permission
from webapi.app.routers.workspace.workspace import router


@router.get("/statistics", description="获取统计数据", summary="获取平台统计数据")
async def query_follow_testplan(_=Depends(Permission())):
    end = datetime.now()
    start = datetime.now() - timedelta(days=6)
    rank = await TestCaseDao.query_user_case_rank()
    count, data = await DashboardDao.get_statistics_data(start, end)
    report_data = await DashboardDao.get_report_statistics(start, end)
    online = ws_manage.get_clients()
    return SakuraResponse.success(dict(count=count, data=data, rank=rank, clients=online, report=report_data))

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/28 11:14
# @Author  : 冉勇
# @Site    : 
# @File    : operation_log.py
# @Software: PyCharm
# @desc    : 获取用户操作记录
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy import desc
from webapi.app.crud.operation.SakuraOperationDao import SakuraOperationDao
from webapi.app.handler.fatcory import SakuraResponse
from webapi.app.models.operation_log import SakuraOperationLog
from webapi.app.routers import Permission

router = APIRouter(prefix="/operation")


# 获取用户操作记录
@router.get("/list", summary="获取用户操作记录", tags=['用户操作'])
async def list_user_operation(start_time: str, end_time: str, user_id: int, tag: str = None, _=Depends(Permission())):
    try:
        start = datetime.strptime(start_time, "%Y-%m-%d")
        end = datetime.strptime(end_time, "%Y-%m-%d")
        records = await SakuraOperationDao.list_record(user_id=user_id, tag=tag, condition=[
            SakuraOperationLog.operate_time.between(start, end)], _sort=[desc(SakuraOperationLog.operate_time)])
        return SakuraResponse.records(records)
    except Exception as e:
        return SakuraResponse.failed(e)


# 获取用户操作记录热力图以及参与的项目数量
@router.get("/count", summary="获取用户操作记录热力图以及参与的项目数量", tags=['用户操作'])
async def list_user_activities(user_id: int, start_time: str, end_time: str, _=Depends(Permission())):
    try:
        start = datetime.strptime(start_time, "%Y-%,-%d")
        end = datetime.strptime(end_time, "%Y-%m-%d")
        records = await SakuraOperationDao.count_user_activities(user_id, start, end)
        ans = []
        for r in records:
            # 解包日期和数量
            date, count = r
            ans.append(dict(date=date.strftime("%Y-%m-%d"), count=count))
        return SakuraResponse.success(ans)
    except Exception as e:
        return SakuraResponse.failed(e)

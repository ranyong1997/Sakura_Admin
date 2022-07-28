#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/28 11:14
# @Author  : 冉勇
# @Site    : 
# @File    : operation.py
# @Software: PyCharm
# @desc    : 获取用户操作记录
from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy import desc
from webapi.app.crud.operation.SakuraOperationDao import SakuraOperationDao
from webapi.app.handler.fatcory import SakuraResponse
from webapi.app.models.operation_log import SakuraOperationLog
from webapi.app.routers import Permission

router = APIRouter(perfix="/operation")


# 获取用户操作记录
@router.get("/list")
async def list_user_operation(start_time: str, end_time: str, user_id: int, tag: str = None, _=Depends(Permission())):
    try:
        start = datetime.strftime(start_time, "%Y-%m-%d")
        end = datetime.strftime(end_time, "%Y-%m-%d")
        records = await SakuraOperationDao.list_record(user_id=user_id, tag=tag, condition=[
            SakuraOperationLog.operate_time.between(start, end)], _sort=[desc(SakuraOperationLog.operate_time)])
        return SakuraResponse.records(records)
    except Exception as e:
        return SakuraResponse.failed(e)

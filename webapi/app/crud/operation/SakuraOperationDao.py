#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/28 11:15
# @Author  : 冉勇
# @Site    : 
# @File    : SakuraOperationDao.py
# @Software: PyCharm
# @desc    : 操作记录(dao)逻辑
from datetime import datetime
from sqlalchemy import func, select
from webapi.app.crud import Mapper
from webapi.app.models import async_session
from webapi.app.models.operation_log import SakuraOperationLog
from webapi.app.utils.decorator import dao
from webapi.app.utils.logger import Log


@dao(SakuraOperationLog, Log("SakuraOperationDao"))
class SakuraOperationDao(Mapper):
    @classmethod
    async def count_user_activities(cls, user_id, start_time: datetime, end_time: datetime):
        """
        根据开始/结束时间 获取用户的活动日历(操作记录的数量)
        :param user_id:
        :param start_time:
        :param end_time:
        :return:
        """
        async with async_session() as session:
            async with session.begin():
                sql = select(
                    SakuraOperationLog.operate_time, func.count(SakuraOperationLog.id)).where(
                    SakuraOperationLog.operate_time.between(start_time, end_time),
                    SakuraOperationLog.user_id == user_id) \
                    .group_by(SakuraOperationLog.operate_time).order_by(SakuraOperationLog.operate_time)
                data = await session.execute(sql)
                return data.all()

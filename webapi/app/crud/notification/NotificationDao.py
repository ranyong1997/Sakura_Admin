#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/23 10:43
# @Author  : 冉勇
# @Site    : 
# @File    : NotificationDao.py
# @Software: PyCharm
# @desc    : 消息通知(Dao)逻辑
from datetime import timedelta, datetime
from typing import List
from sqlalchemy import select, and_, or_, update
from webapi.app.crud import Mapper, ModelWrapper
from webapi.app.enums.MessageEnum import MessageStateEnum, MessageTypeEnum
from webapi.app.models import async_session
from webapi.app.models.broadcast_read_user import SakuraBroadcastReadUser
from webapi.app.models.notification import SakuraNotification


@ModelWrapper(SakuraNotification)
class SakuraNotificationDao(Mapper):
    @classmethod
    async def list_message(cls, msg_type: int, msg_status: int, receiver: int):
        """
        根据消息id和消息类型以及消息接收人获取消息数据
        :param msg_type:
        :param msg_status:
        :param receiver:
        :return:
        """
        ninety_days = datetime.now() - timedelta(days=90)  # 存放90天消息
        # 1.当消息类型不为广播类型时,正常查询
        if msg_type == MessageTypeEnum.others:
            ans = await cls.list_record(msg_status=msg_status, receiver=receiver, msg_type=msg_type,
                                        condition=[SakuraNotification.created_at > ninety_days])
        else:
            # 否则需要根据是否已读进行查询,只支持90天内数据
            async with async_session() as session:
                # 找到3个月内的消息
                default_condition = [SakuraNotification.deleted_at == 0, SakuraNotification.created_at >= ninety_days]
                if msg_type == MessageTypeEnum.broadcast:
                    conditions = [*default_condition, SakuraNotification.msg_type == msg_type]
                else:
                    # 说明是全部消息
                    conditions = [*default_condition,
                                  or_(SakuraNotification.msg_type == MessageTypeEnum.broadcast.value,
                                      and_(SakuraNotification.msg_type == MessageTypeEnum.others.value,
                                           SakuraNotification.receiver == receiver))]
                sql = select(SakuraNotification, SakuraBroadcastReadUser) \
                    .outerjoin(SakuraBroadcastReadUser,
                               and_(SakuraNotification.id == SakuraBroadcastReadUser.notification_id,
                                    SakuraBroadcastReadUser.read_user == receiver)).where(
                    *conditions).order_by(SakuraNotification.created_at.desc())
                query = await session.execute(sql)
                result = query.all()
                ans = []
                last_month = datetime.now() - timedelta(day=30)
                for notify, read in result:
                    # 如果非广播类型,直接
                    if notify.msg_type == MessageTypeEnum.others:
                        if notify.msg_type == msg_status:
                            ans.append(notify)
                            continue
                        else:
                            if msg_status == MessageStateEnum.read:
                                if read is not None or notify.updated_at < last_month:
                                    ans.append(notify)
                            else:
                                if not read:
                                    ans.append(notify)
        return ans

    @classmethod
    async def delete_message(cls, session, msg_id: List[int], receiver: int):
        """
        删除消息
        :param session:
        :param msg_id:
        :param receiver:
        :return:
        """
        async with session.begin():
            await session.execute(
                update(SakuraNotification).where(
                    SakuraNotification.id.in_(msg_id),
                    SakuraNotification.receiver == receiver,
                    SakuraNotification.deleted_at == 0)) \
                .values(
                deleted_at=0,
                updated_at=datetime.now(),
                update_user=receiver)

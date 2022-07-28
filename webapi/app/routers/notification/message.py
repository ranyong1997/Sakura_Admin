#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/28 10:32
# @Author  : 冉勇
# @Site    : 
# @File    : message.py
# @Software: PyCharm
# @desc    : 用户消息列表[crud]
from typing import List
from fastapi import APIRouter, Depends
from webapi.app.crud.notification.BroadcastReadDao import BroadcastReadDao
from webapi.app.crud.notification.NotificationDao import SakuraNotificationDao
from webapi.app.enums.MessageEnum import MessageStateEnum
from webapi.app.handler.fatcory import SakuraResponse
from webapi.app.models.broadcast_read_user import SakuraBroadcastReadUser
from webapi.app.models.notification import SakuraNotification
from webapi.app.schema.notification import NotificationForm
from webapi.app.routers import Permission, get_session

router = APIRouter(prefix="/notification")


@router.get("/list", description="获取用户消息列表")
async def list_msg(msg_status: int, msg_type: int, user_info=Depends(Permission())):
    try:
        data = await SakuraNotificationDao.list_message(msg_type=msg_type, msg_status=msg_status,
                                                        receiver=user_info['id'])
        return SakuraResponse.success(data)
    except Exception as e:
        return SakuraResponse.failed(str(e))


@router.post('/read', description="用户读取消息")
async def read_msg(form: NotificationForm, user_info=Depends(Permission())):
    try:
        if form.personal:
            await SakuraNotificationDao.update_by_map(user_info['id'],
                                                      SakuraNotification.id.in_(form.personal),
                                                      SakuraNotification.receiver == user_info['id'],
                                                      msg_status=MessageStateEnum.read.value)
        if form.broadcast:
            user_id = user_info['id']
            for f in form.broadcast:
                model = SakuraBroadcastReadUser(f, user_id)
                await BroadcastReadDao.insert_record(model)
        return SakuraResponse.success()
    except Exception as e:
        return SakuraResponse.failed(str(e))


@router.post("/delete", description="用户删除信息")
async def read_msg(msg_id: List[int], user_info=Depends(Permission()), session=Depends(get_session)):
    try:
        await SakuraNotificationDao.delete_message(session, msg_id, user_info['id'])
        return SakuraResponse.success()
    except Exception as e:
        return SakuraResponse.failed(str(e))

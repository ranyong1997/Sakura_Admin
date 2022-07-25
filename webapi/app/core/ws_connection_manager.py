#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/23 10:41
# @Author  : 冉勇
# @Site    : 
# @File    : ws_connection_manager.py
# @Software: PyCharm
# @desc    : wss连接管理
from typing import TypeVar
from fastapi import WebSocket
from webapi.app.core.msg.wss_msg import WebSocketMessage
from webapi.app.crud.notification.NotificationDao import SakuraNotificationDao
from webapi.app.models.notification import SakuraNotification
from webapi.app.utils.logger import Log

MsgType = TypeVar('MsgType', str, dict, bytes)


class ConnectionManager:
    BROADCAST = -1
    logger = Log('wss_manager')

    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}
        self.log = Log("websocket")

    async def connect(self, websocket: WebSocket, client_id: int) -> None:
        await websocket.accept()
        exist: WebSocket = self.active_connections.get(client_id)
        if exist:
            await exist.close()
        else:
            self.active_connections[client_id]: WebSocket = websocket
            self.log.debug(f"websocket:用户[{client_id}]建立连接成功")

    def disconnect(self, client_id: int) -> None:
        del self.active_connections[client_id]
        self.log.debug(f"websocket:用户[{client_id}]已安全断开")

    @staticmethod
    async def pushed(sender: WebSocket, message: MsgType) -> None:
        """
        根据不同消息类型,调用不同的方法发送信息
        :param sender:
        :param message:
        :return:
        """
        msg_mapping: dict = {
            str: sender.send_text,
            dict: sender.send_json,
            bytes: sender.send_bytes
        }
        if func_push_msg := msg_mapping.get(type(message)):
            await func_push_msg(message)
        else:
            raise TypeError(f"websocket不能发送{type(message)}的内容")

    async def send_personal_message(self, message: MsgType) -> None:
        """
        发送个人信息
        :param message:
        :return:
        """
        for connection in self.active_connections.values():
            await self.pushed(sender=connection, message=message)

    async def broadcast(self, message: MsgType) -> None:
        """
        广播
        :param message:
        :return:
        """
        for connection in self.active_connections.values():
            await self.pushed(sender=connection, message=message)

    async def notify(self, user_id, title=None, content=None, notice: SakuraNotification = None):
        """
        根据user_id推送对应信息
        :param user_id:
        :param title:
        :param content:
        :param notice:
        :return:
        """
        try:
            # 判断是否为桌面通知
            if title is not None:
                msg = WebSocketMessage.desktop_msg(title, content)
                if user_id == ConnectionManager.BROADCAST:
                    await self.broadcast(msg)
                else:
                    await self.send_personal_message(user_id, msg)
            elif user_id == ConnectionManager.broadcast:
                await self.broadcast(WebSocketMessage.msg_count())
            else:
                await self.send_personal_message(user_id, WebSocketMessage.msg_count())
            # 判断是否要落入推送表
            if notice is not None:
                await SakuraNotificationDao.insert_record(notice)
        except Exception as e:
            ConnectionManager.logger.error(f"发送消息失败,{e}")

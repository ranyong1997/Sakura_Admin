#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/17 10:49
# @Author  : 冉勇
# @Site    : 
# @File    : record.py
# @Software: PyCharm
# @desc    : 流量录制->生成case功能
import asyncio
import json
import re
from webapi.app.core.ws_connection_manager import ws_manage
from webapi.app.enums.MessageEnum import WebSocketMessageEnum
from webapi.app.middleware.RedisManager import RedisHelper
from webapi.app.schema.request import RequestInfo


class SakuraRecorder(object):
    def request(self, flow):
        flow.request.headers["X-Forwarded-For"] = flow.client_conn.address[0]

    async def response(self, flow):
        if "sakura.fun" in flow.request.url or flow.request.method.lower() == "options" or \
                flow.request.url.endswith(("js", "css", "ttf", "jpg", "svg", "gif")):
            # 如果是sakura,options请求,js等url直接拒绝
            return
        addr = flow.client_conn.address[0]
        record = await RedisHelper.get_address_record(addr)
        if not record:
            return
        data = json.loads(record)
        pattern = re.compile(data.get("regex"))
        if re.findall(pattern, flow.request.url):
            # 说明已经开启了录制开关,纪录状态
            request_data = RequestInfo(flow)
            dump_data = request_data.dumps()
            await RedisHelper.cache_record(addr, dump_data)
            asyncio.create_task(
                ws_manage.send_personal_message(data.get("user_id"), WebSocketMessageEnum.RECORD, dump_data))

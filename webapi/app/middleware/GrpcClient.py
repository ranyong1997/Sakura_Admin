#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/17 11:24
# @Author  : 冉勇
# @Site    : 
# @File    : GrpcClient.py
# @Software: PyCharm
# @desc    : grpc客户端
import asyncio
from grpc_requests import AsyncClient


class GrpcClient(object):
    @staticmethod
    async def invoke(address: str, iface: str, method: str, request_data=None):
        client = AsyncClient(address)
        service = await client.service(iface)
        return await getattr(service, method)(request_data)


if __name__ == "__main__":
    asyncio.run(GrpcClient.invoke("localhost:50052", "Hello", "Edit", {"number": 10}))

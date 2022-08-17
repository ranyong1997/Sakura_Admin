#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/21 16:39
# @Author  : 冉勇
# @Site    : 
# @File    : proxy.py
# @Software: PyCharm
# @desc    : 代理
import asyncio
import uvicorn
from fastapi import FastAPI
from loguru import logger

from webapi.config import Config
from webapi.sakura_proxy import start_proxy

mock = FastAPI()
if Config.MOCK_ON:
    asyncio.run(start_proxy(logger))

if __name__ == '__main__':
    uvicorn.run("proxy:mock", host="0.0.0.0", port=Config.PROXY_PORT, reload=False, forwarded_allow_ips="*", workers=1)

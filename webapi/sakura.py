#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/21 16:37
# @Author  : 冉勇
# @Site    : 
# @File    : sakura.py
# @Software: PyCharm
# @desc    : 运行入口
import uvicorn

from webapi.config import Config

if __name__ == '__main__':
    uvicorn.run("main:sakura", host=Config.SERVER_HOST, port=Config.SERVER_PORT, reload=False, forwarded_allow_ips="*")

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/22 17:10
# @Author  : 冉勇
# @Site    : 
# @File    : main.py
# @Software: PyCharm
# @desc    : 主入口
import asyncio
from mimetypes import guess_type
from os.path import isfile
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import Request,WebSocket,WebSocketDisconnect,Depends
from starlette.responses import Response
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from webapi.app import S


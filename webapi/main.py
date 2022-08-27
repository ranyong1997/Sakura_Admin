#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/22 17:10
# @Author  : 冉勇
# @Site    : 
# @File    : main.py
# @Software: PyCharm
# @desc    : 主入口
import asyncio
import contextlib
from mimetypes import guess_type
from os.path import isfile
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import Request, WebSocket, WebSocketDisconnect, Depends
from starlette.responses import Response
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from webapi.app import sakura, init_logging
from webapi.app.core.msg.wss_msg import WebSocketMessage
from webapi.app.core.ws_connection_manager import ws_manage
from webapi.app.crud import create_table
from webapi.app.crud.notification.NotificationDao import SakuraNotificationDao
from webapi.app.enums.MessageEnum import MessageStateEnum, MessageTypeEnum
from webapi.app.middleware.RedisManager import RedisHelper
from webapi.app.routers.auth import user
from webapi.app.routers.config import router as config_router
from webapi.app.routers.notification import router as msg_router
from webapi.app.routers.online import router as online_router
from webapi.app.routers.operation import router as operation_router
from webapi.app.routers.oss import router as oss_router
from webapi.app.routers.project import project
from webapi.app.routers.request import http
from webapi.app.routers.testcase import router as testcase_router
from webapi.app.routers.workspace import router as workspace_router
from webapi.config import Config, SAKURA_ENV, BANNER
from webapi.app.utils.scheduler import Scheduler

logger = init_logging()
logger.bind(name=None).opt(ansi=True).success(f"sakura 正在运行环境: <red>{SAKURA_ENV} 网址: http://localhost:7777/docs</red>")
logger.bind(name=None).success(BANNER)


async def request_info(request: Request):
    logger.bind(name=None).debug(f"{request.method}{request.url}")
    try:
        body = await request.json()
        logger.bind(payload=body, name=None).debug("request_json:")
    except Exception:
        with contextlib.suppress(Exception):
            body = await request.body()
            if len(body) != 0:
                # 有请求体,记录日志
                logger.bind(payload=body, name=None).debug(body)


# 注册路由
sakura.include_router(user.router)
sakura.include_router(project.router, dependencies=[Depends(request_info)])
sakura.include_router(http.router, dependencies=[Depends(request_info)])
sakura.include_router(testcase_router, dependencies=[Depends(request_info)])
sakura.include_router(config_router, dependencies=[Depends(request_info)])
sakura.include_router(online_router, dependencies=[Depends(request_info)])
sakura.include_router(oss_router, dependencies=[Depends(request_info)])
sakura.include_router(operation_router, dependencies=[Depends(request_info)])
sakura.include_router(msg_router, dependencies=[Depends(request_info)])
sakura.include_router(workspace_router, dependencies=[Depends(request_info)])
sakura.mount("/statics", StaticFiles(directory="statics"), name="statics")
templates = Jinja2Templates(directory="statics")


@sakura.get("/", tags=['Other'])
async def serve_spa(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@sakura.get("/{filename}", tags=['Other'])
async def get_site(filename):
    filename = f"app/statics/{filename}"
    if not isfile(filename):
        return Response(status_code=404)
    with open(filename, mode='rb') as f:
        content = f.read()
    content_type = guess_type(filename)
    return Response(content, media_type=content_type)


@sakura.get("/static/{filename}", tags=['Other'])
async def get_site_static(filename):
    filename = f"app/statics/static/{filename}"
    if not isfile(filename):
        return Response(status_code=404)
    with open(filename, mode='rb') as f:
        content = f.read()

    content_type, _ = guess_type(filename)
    return Response(content, media_type=content_type)


@sakura.on_event("startup")
async def init_redis():
    """
    初始化redis,失败则服务不起来
    :return:
    """
    try:
        await RedisHelper.ping()
        logger.bind(name=None).success("Redis 连接成功.✔")
    except Exception as e:
        if not Config.REDIS_ON:
            logger.bind(name=None).warning("没有选择redis，所以我们不能保证任务不重复执行.🚫")
            return
        logger.bind(name=None).error("Redis 连接失败，请检查 config.py 中的 redis 配置.❌")
        raise e


@sakura.on_event("startup")
def init_scheduler():
    """
    初始化定时任务
    :return:
    """
    # SQLAlchemyJobStore指定存储链接
    job_store = {
        'default': SQLAlchemyJobStore(url=Config.SQLALCHEMY_DATABASE_URI, engine_options={"pool_recycle": 1500},
                                      pickle_protocol=3)
    }
    scheduler = AsyncIOScheduler()
    Scheduler.init(scheduler)
    Scheduler.configure(jobstore=job_store)
    Scheduler.start()
    logger.bind(name=None).success("ApScheduler 启动成功.✔")


@sakura.on_event("startup")
async def init_database():
    """
    初始化数据库,建表
    :return:
    """
    try:
        asyncio.create_task(create_table())
        logger.bind(name=None).success("数据库和表创建成功.✔")
    except Exception as e:
        logger.bind(name=None).error(f"数据库和表创建失败.❌ \n Error:{str(e)}")
        raise


@sakura.on_event("shutdown")
def stop_test():
    pass


@sakura.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    async def send_heartbeat():
        while True:
            logger.debug("发送心跳💓")
            await websocket.send_json({
                "type": 3
            })
            await asyncio.sleep(Config.HEARTBASE)

    await ws_manage.connect(websocket, user_id)
    try:
        # 定义特殊值的回复,配合前端实现确定连接,心跳检测等逻辑
        questions_and_answers_map: dict = {
            "HELLO SERVER": f"hello{user_id}",
            "HEARTBEAT": f"{user_id}"
        }
        # 存储连接后获取信息
        msg_records = await SakuraNotificationDao.list_message(msg_type=MessageTypeEnum.all.value, receiver=user_id,
                                                               msg_status=MessageStateEnum.unread.value)
        # 如果有未读消息,则推送给前端对应的count
        if len(msg_records) > 0:
            await websocket.send_json(WebSocketMessage.msg_count(len(msg_records), True))
        # 发送心跳
        while True:
            data: str = await websocket.receive_text()
            du = data.upper()
            if du in questions_and_answers_map:
                await ws_manage.send_personal_message(message=questions_and_answers_map.get(du), websocket=websocket)
    except WebSocketDisconnect:
        if user_id in ws_manage.active_connections:
            ws_manage.disconnect(user_id)
    except Exception as e:
        logger.bind(name=None).debug(f"websocket:用户:{user_id}异常退出:{str(e)}")

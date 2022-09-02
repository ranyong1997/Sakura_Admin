#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/20 09:10
# @Author  : 冉勇
# @Site    : 
# @File    : __init__.py.py
# @Software: PyCharm
# @desc    :
import logging
import os
import sys
import traceback
from pprint import pformat
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from loguru import logger
from loguru._defaults import LOGURU_FORMAT
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.errors import ServerErrorMiddleware
from starlette.types import Message
from webapi.app.excpetions.RequestException import AuthException
from webapi.app.excpetions.RequestException import PermissionException
from webapi.config import Config
# from starlette_context import middleware, plugins
sakura = FastAPI()

# sakura.add_middleware(
#     middleware.ContextMiddleware,
#     plugins={
#         plugins.ForwardedForPlugin()
#     }
# )

# 配置日志格式
INFO_FORMAT = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> " \
              "| <level>{level: <8}</level> | <cyan>文件: {extra[filename]}</cyan> " \
              "| 模块: <cyan>{extra[business]}</cyan> | 方法: <cyan>{extra[func]}</cyan> " \
              "| <cyan>行数: {extra[line]}</cyan> | - <level>{message}</level>"

ERROR_FORMAT = "<red>{time:YYYY-MM-DD HH:mm:ss.SSS}</red> " \
               "| <level>{level: <8}</level> | <cyan>文件: {extra[filename]}</cyan> " \
               "| 模块: <cyan>{extra[business]}</cyan> | 方法: <cyan>{extra[func]}</cyan> " \
               "| <cyan>行数: {extra[line]}</cyan> | - <level>{message}</level>"


async def set_body(request: Request, body: bytes):
    async def receive() -> Message:
        return {"type": "http.request", "body": body}

    request._receive = receive


async def get_body(request: Request) -> bytes:
    body = await request.body()
    await set_body(request, body)
    return body


@sakura.middleware("http")
async def errors_handler(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        traceback.print_exc()
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder({
                "code": 110,
                "msg": str(exc)
            })
        )


def error_map(error_type: str, field: str, msg: str = None):
    if "missing" in error_type:
        return f"缺少参数:{field}"
    elif "params" in error_type:
        return f"参数{field}{'不规范' if msg is None else msg}"
    elif "not_allowed" in error_type:
        return f"参数:{field}类型不正确"
    elif "type_error" in error_type:
        return f"参数:{field}类型不合法"


@sakura.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    验证异常处理程序
    :param request:
    :param exc:
    :return:
    """
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({
            "code": 101,
            "msg": error_map(exc.errors()[0]["type"], exc.errors()[0].get("loc", ['unknown'])[-1],
                             exc.errors()[0].get("msg")) if len(exc.errors()) > 0 else "参数解析失败"
        })
    )


@sakura.exception_handler(PermissionException)
async def unexpected_exception_error(request: Request, exc: PermissionException):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({
            "code": 403,
            "msg": exc.detail
        })
    )


@sakura.exception_handler(AuthException)
async def unexpected_exception_error(request: Request, exc: AuthException):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=jsonable_encoder({
            "code": 401,
            "msg": str(exc.detail),
        })
    )


async def global_execution_handler(request: Request, exc: Exception):
    """
    全局执行处理程序
    :param request:
    :param exc:
    :return:
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=dict(code=110, msg="未知错误:" + str(exc))
    )


# 添加全局error
sakura.add_middleware(
    ServerErrorMiddleware,
    handler=global_execution_handler,
)

# 添加跨域
sakura.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


class InterceptHandler(logging.Handler):
    """拦截处理程序"""

    def emit(self, record: logging.LogRecord):
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def format_record(record: dict) -> str:
    """
    记录日志格式
    :param record:
    :return:
    例子：
    Example:
    # >>> payload = [{"users":[{"name": "Nick", "age": 87, "is_active": True}, {"name": "Alex", "age": 27, "is_active": True}], "count": 2}]
    # >>> logger.bind(payload=).debug("users payload")
    # >>> [   {   'count': 2,
    # >>>         'users': [   {'age': 87, 'is_active': True, 'name': 'Nick'},
    # >>>                      {'age': 27, 'is_active': True, 'name': 'Alex'}]}]
    """
    format_string = LOGURU_FORMAT
    if record["extra"].get("payload") is not None:
        record["extra"]["payload"] = pformat(
            record["extra"]["payload"], indent=4, compact=True, width=88
        )
        format_string += "\n<level>{extra[payload]}</level>"
    format_string += "{exception}\n"
    return format_string


def make_filter(name):
    """
    过滤操作,当日志要选择对应的日志文件的时候,通过filter进行筛选
    :param name:
    :return:
    """

    def filter_(record):
        return record["extra"].get("name") == name

    return filter_


def init_logging():
    """
    初始化日志
    :return:
    """
    loggers = {
        logging.getLogger(name)
        for name in logging.root.manager.loggerDict
        if name.startswith("uvicorn.")  # 以【uvicorn.】开始
    }
    for uvicorn_logger in loggers:
        uvicorn_logger.handlers = []
    # 这里啊错做事为了改变uvicorn默认的logger,采用loguru的logger
    intercept_handler = InterceptHandler()
    logging.getLogger("uvicorn").handlers = [intercept_handler]
    # 为sakura添加一个info log的文件,主要记录debug和info级别的日志
    sakura_info = os.path.join(Config.LOG_DIR, f"{Config.SAKURA_INFO}.log")
    # 为sakura添加一个error log的文件,主要记录warning和error级别的日志
    sakura_error = os.path.join(Config.LOG_DIR, f"{Config.SAKURA_ERROR}.log")
    logger.add(sakura_info, enqueue=True, rotation="20 MB", level="DEBUG", filter=make_filter(Config.SAKURA_INFO))
    logger.add(sakura_error, enqueue=True, rotation="20 MB", level="WARNING", filter=make_filter(Config.SAKURA_ERROR))

    # 配置loguru的日志句柄,sink代表输出目标
    logger.configure(
        handlers=[
            {"sink": sys.stdout, "level": logging.DEBUG, "format": format_record},
            {"sink": sakura_info, "level": logging.INFO, "format": INFO_FORMAT,
             "filter": make_filter(Config.SAKURA_INFO)},
            {"sink": sakura_error, "level": logging.WARNING, "format": ERROR_FORMAT,
             "filter": make_filter(Config.SAKURA_ERROR)}
        ]
    )
    return logger

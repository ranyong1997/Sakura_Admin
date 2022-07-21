#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/21 16:56
# @Author  : 冉勇
# @Site    : 
# @File    : decorator.py
# @Software: PyCharm
# @desc    : 装饰器封装
import asyncio
import functools
import os
from datetime import datetime
from functools import wraps
from typing import Coroutine
from redlock import RedLock, RedLockError
from webapi.config import Config


class SingletonDecorator:
    # 单例装饰器
    def __init__(self, cls):
        self.cls = cls
        self.instance = None

    def __call__(self, *args, **kwargs):
        if self.instance is None:
            self.instance = self.cls(*args, **kwargs)
        return self.instance


def case_log(func):
    if asyncio.iscoroutine(func):
        @wraps(func)
        async def wrapper(*args, **kw):
            self = args[0]
            doc = func.__doc__
            self.logger.o_append("[{}]: 步骤开始 -> {}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                           doc.strip() if doc else func.__name__, get_str(args, kw)))
            returns = await func(*args, **kw)
            self.logger.o_append("[{}]:步骤结束 -> {} {}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                             doc.strip() if doc else func.__name__,
                                                             get_returns(returns)))

            return returns
    else:
        @wraps(func)
        def wrapper(*args, **kw):
            self = args[0]
            doc = func.__doc__
            self.logger.o_append("[{}]: 步骤开始 -> {}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                           doc.strip() if doc else func.__name__, get_str(args, kw)))
            returns = func(*args, **kw)
            if not isinstance(returns, Coroutine):
                self.logger.o_append("[{}]:步骤结束 -> {}{}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                                doc.strip() if doc else func.__name__))
            return returns
    return wrapper


def get_str(args, kwargs):
    result = []
    # 这里从1索引开始，因为args[0]是self,也就注定了case_log只能在Executor方法下使用
    for i, a in enumerate(args[1:], start=1):
        if type(a).__name__ == "function":
            result.append(a.__doc__ if a.__doc__ else a.__name__)
        else:
            result.append(f"\n 参数{i}:\n{str(a)}")
    if kwargs:
        for k, v in kwargs:
            result.append(f"\n {k}->{v}")
    if len(result) == 0:
        return "无"
    return ",".join(result)


def get_returns(obj):
    if not obj:
        return ""
    if type(obj).__name__ == "function":
        return obj.__obj__ if obj.__doc__ else obj.__name__
    if isinstance(obj, object):
        return str(obj)
    return f"返回值:{obj}"


def dao(model, log):
    def wrapper(cls):
        setattr(cls, "model", model)
        setattr(cls, "log", log)
        return cls

    return wrapper


def lock(key):
    """
    redis分布式锁，基于redlock
    :param key: 唯一key,确保所有任务一致,但不与其他任务冲突
    :return:
    """

    def decorator(func):
        if asyncio.iscoroutinefunction(func):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                try:
                    with RedLock(f"分布式锁:{func.__name__}:{key}:{str(args)}", connection_details=Config.REDIS_NODES,
                                 ttl=30000  # 释放时间为30s
                                 ):
                        return func(*args, **kwargs)
                except Exception:
                    print(f"进程:{os.getpid()}获取任务失败,不用担心,还有其他为你执行")
        else:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                try:
                    with RedLock(f"distributed_lock:{func.__name__}:{key}:{str(args)}",
                                 connection_details=Config.REDIS_NODES,
                                 ttl=30000,  # 锁释放时间为30s
                                 ):
                        return func(*args, **kwargs)
                except RedLockError:
                    print(f"进程: {os.getpid()}获取任务失败,不用担心,还有其他为你执行")
        return wrapper

    return decorator

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/4 15:07
# @Author  : 冉勇
# @Site    : 
# @File    : redis_constructor.py
# @Software: PyCharm
# @desc    : redis 构造函数
import json
from webapi.app.core.constructor.constructor import ConstructorAbstract
from webapi.app.crud.config.RedisConfigDao import SakuraRedisConfigDao
from webapi.app.models.constructor import Constructor


class RedisConstructor(ConstructorAbstract):
    @staticmethod
    async def run(executor, env, index, path, params, req_params, constructor: Constructor, **kwargs):
        try:
            executor.append(f"当前路径:{path},第{index + 1}条{ConstructorAbstract.get_name(constructor)}")
            data = json.loads(constructor.constructor_json)
            redis = data.get("redis")
            command = data.get("command")
            executor.append(f"当前{ConstructorAbstract.get_name(constructor)}类型为redis,名称:{redis}\n 命令:{command}\n")
            command_result = await SakuraRedisConfigDao.execute_command(command=command, name=redis, env=env)
            params[constructor.value] = command_result
            executor.append(
                f"当前{ConstructorAbstract.get_name(constructor)}返回变量:{constructor.value}\n返回值:\n{command_result}\n")
        except Exception as e:
            raise Exception(
                f"当前路径:{path}->{constructor.name}第{index + 1}个{ConstructorAbstract.get_name(constructor)}执行失败:{str(e)}") from e

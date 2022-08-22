#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/27 15:19
# @Author  : 冉勇
# @Site    : 
# @File    : RedisConfigDao.py
# @Software: PyCharm
# @desc    : ReidsDao(逻辑)
from webapi.app.crud import Mapper, ModelWrapper
from webapi.app.middleware.RedisManager import SakuraRedisManager, RedisHelper
from webapi.app.models.redis_config import SakuraRedis


@ModelWrapper(SakuraRedis)
class SakuraRedisConfigDao(Mapper):

    @staticmethod
    async def execute_command(command: str, **kwargs):
        try:
            redis_config = await SakuraRedisConfigDao.query_record(**kwargs)
            if redis_config is None:
                raise Exception("Redis配置不存在")
            if not redis_config.cluster:
                client = SakuraRedisManager.get_single_client(redis_config.id, redis_config.addr,
                                                              redis_config.password, redis_config.db)
            else:
                client = SakuraRedisManager.get_cluster_client(redis_config.id, redis_config.addr)
            return await RedisHelper.execute_command(client, command)
        except Exception as e:
            raise Exception(f"执行redis命令出错:{e}") from e

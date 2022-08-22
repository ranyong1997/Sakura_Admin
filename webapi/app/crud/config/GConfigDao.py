#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/25 16:29
# @Author  : 冉勇
# @Site    : 
# @File    : GConfigDao.py
# @Software: PyCharm
# @desc    : 全局配置Dao(逻辑)
from sqlalchemy import select
from webapi.app.crud import Mapper, ModelWrapper
from webapi.app.middleware.RedisManager import RedisHelper
from webapi.app.models import async_session
from webapi.app.models.gconfig import GConfig
from webapi.app.schema.gconfig import GConfigForm


@ModelWrapper(GConfig)
class GConfigDao(Mapper):

    @classmethod
    @RedisHelper.up_cache("dao")
    async def insert_gconfig(cls, form: GConfigForm, user_id: int) -> None:
        try:
            async with async_session() as session:
                async with session.begin():
                    query: await session.execute(
                        select(GConfig).where(GConfig.env == form.env, GConfig.key == form.key,
                                              GConfig.deleted_at == 0))
                    data = query.scalars().first()
                    if data is not None:
                        raise Exception(f"变量,{data.key}已存在")
                    config = GConfig(**form.dict(), user=user_id)
                    session.add(config)
        except Exception as e:
            cls.__log__.error(f"新增变量:{data.key}失败,{str(e)}")
            raise Exception(f"新增变量:{data.key}失败,{str(e)}") from e

    @staticmethod
    @RedisHelper.cache("dao", 1800, True)
    async def async_get_gconfig_by_key(key: str, env: int) -> GConfig:
        try:
            filter = [GConfig.key == key, GConfig.deleted_at == 0, GConfig.enable == True, GConfig.env == env]
            async with async_session() as session:
                sql = select(GConfig).where(*filter)
                result = await session.execute(sql)
                return result.scalars().first()
        except Exception as e:
            raise Exception(f"查询全局变量失败:{str(e)}") from e

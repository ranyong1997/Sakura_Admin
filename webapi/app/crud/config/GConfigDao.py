#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/25 16:29
# @Author  : 冉勇
# @Site    : 
# @File    : GConfigDao.py
# @Software: PyCharm
# @desc    : 全局配置Dao(逻辑)
from sqlalchemy import select
from webapi.app.crud import Mapper
from webapi.app.middleware.RedisManager import RedisHelper
from webapi.app.models import async_session
from webapi.app.models.gconfig import GConfig
from webapi.app.schema.gconfig import GConfigForm
from webapi.app.utils.decorator import dao
from webapi.app.utils.logger import Log


@dao(GConfig, Log("GConfigDao"))
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
                    select.add(config)
        except Exception as e:
            raise Exception(f"查询全局变量失败:{str(e)}") from e
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/28 09:32
# @Author  : 冉勇
# @Site    : 
# @File    : AddressDao.py
# @Software: PyCharm
# @desc    : 网关Dao(逻辑)
from sqlalchemy import select
from webapi.app.crud import Mapper, ModelWrapper
from webapi.app.models import async_session
from webapi.app.models.address import SakuraGateway


@ModelWrapper(SakuraGateway)
class SakuraGatewayDao(Mapper):
    @staticmethod
    async def query_gateway(env, name):
        async with async_session() as session:
            query = await session.execute(
                select(SakuraGateway).where(SakuraGateway.deleted_at == 0, SakuraGateway.env == env,
                                            SakuraGateway.name == name)
            )
            data = query.scalars().first()
            if data is None:
                raise Exception(f"此环境没有网关配置: {name}")
            return data.gateway

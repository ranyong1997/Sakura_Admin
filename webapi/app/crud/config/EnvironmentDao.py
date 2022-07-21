#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/20 11:42
# @Author  : 冉勇
# @Site    : 
# @File    : EnvironmentDao.py
# @Software: PyCharm
# @desc    : 环境Dao(逻辑)
from sqlalchemy import select
from webapi.app.crud import Mapper
from webapi.app.models import async_session
from webapi.app.models.environment import Environment
from webapi.app.schema.environment import EnvironmentForm
from webapi.app.utils.decorator import dao
from webapi.app.utils.logger import Log


@dao(Environment, Log("EnvironmentDao"))
class EnvironmentDao(Mapper):
    @staticmethod
    async def query_env(id: int):
        """
        环境id
        :param id:
        :return:
        """
        async with async_session() as session:
            ans = await session.execute(select(Environment).where(Environment.id == id, Environment.deleted_at == 0))
            if ans is None:
                raise Exception(f"环境:{id}不存在")
            return ans.scalars().first()

    @classmethod
    async def insert_env(cls, data: EnvironmentForm, user):
        try:
            async with async_session() as session:
                async with session.begin():
                    query = await session.execute(
                        select(Environment).where(Environment.name == data.name, Environment.deleted_at == 0)
                    )
                    if query.scalars().first() is not None:
                        raise Exception("环境已存在")
                    env = Environment(**data.dict(), user=user)
                    session.add(env)
        except Exception as e:
            EnvironmentDao.log.error(f"新增环境:{data.name}失败,{e}")
            raise Exception(f"添加失败:{str(e)}") from e

    @classmethod
    async def list_env(cls, page, size, name=None, exactly=False):
        try:
            search = [Environment.deleted_at == 0]
            async with async_session() as session:
                if name:
                    search.append(Environment.name.like(f"%{name}%"))
                sql = select(Environment).where(*search)
                query = await session.execute(sql)
                if exactly:
                    data = query.scalars().all()
                    return data, len(data)
                total = query.raw.rowcount
                if total == 0:
                    return [], 0
                sql = sql.offset((page - 1) * size).limit(size)
                data = await session.execute(sql)
                return data.scalars().all(), total
        except Exception as e:
            cls.log.error(f"获取环境列表失败,{str(e)}")
            raise Exception(f"获取环数据失败:{str(e)}") from e

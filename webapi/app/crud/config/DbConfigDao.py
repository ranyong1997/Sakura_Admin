#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/27 10:36
# @Author  : 冉勇
# @Site    : 
# @File    : DbConfigDao.py
# @Software: PyCharm
# @desc    : 数据库Dao(逻辑)
import json
import time
from collections import defaultdict
from typing import List
from sqlalchemy import select, MetaData, text
from sqlalchemy.exc import ResourceClosedError
from webapi.app.crud.config.EnvironmentDao import EnvironmentDao
from webapi.app.handler.encoder import JsonEncoder
from webapi.app.handler.fatcory import SakuraResponse
from webapi.app.middleware.RedisManager import RedisHelper
from webapi.app.models import async_session, DatabaseHelper, db_helper
from webapi.app.models.database import SakuraDatabase
from webapi.app.schema.database import DataBaseForm
from webapi.app.utils.logger import Log


class DbConfigDao(object):
    log = Log("DbConfigDao")

    @staticmethod
    async def list_database(name: str = '', database: str = '', env: int = None):
        """
        通过name,database,env获取数据库配置列表
        :param name:
        :param database:
        :param env:
        :return:
        """
        try:
            async with async_session() as session:
                query = [SakuraDatabase.deleted_at == 0]
                if name:
                    query.append(SakuraDatabase.name.like(f"%{name}&"))
                if database:
                    query.append(SakuraDatabase.database.like(f"%{database}%"))
                if env is not None:
                    query.append(SakuraDatabase.env == env)
                result = await session.execute(select(SakuraDatabase).where(*query))
                return result.scalars().all()
        except Exception as e:
            DbConfigDao.log.error(f"获取数据库配置失败,error:{e}")
            raise Exception("获取数据库配置失败") from e

    @staticmethod
    @RedisHelper.up_cache("database:cache")
    async def insert_database(data: DataBaseForm, user: str):
        try:
            async with async_session() as session:
                async with session.begin():
                    result = await session.execute(
                        select(SakuraDatabase).where(SakuraDatabase.name == data.name, SakuraDatabase.deleted_at == 0,
                                                     SakuraDatabase.env == data.env))
                    query = result.scalars().first()
                    if query is not None:
                        raise Exception("数据库配置已存在")
                    session.add(SakuraDatabase(**data.dict(), user=user))
        except Exception as e:
            DbConfigDao.log.error(f"新增数据库配置:{data.name}失败,{e}")
            raise Exception("新增数据库配置失败") from e

    @staticmethod
    @RedisHelper.up_cache("database:cache")
    async def updata_database(data: DataBaseForm, user: str):
        try:
            async with async_session() as session:
                async with session.begin():
                    result = await session.execute(
                        select(SakuraDatabase).where(data.id == SakuraDatabase.id))
                    query = result.scalars().first()
                    if query is None:
                        raise Exception("数据库配置不存在")
                    db_helper.remove_connection(query.host, query.port, query.username, query.password, query.database)
                    DatabaseHelper.updata_model(query, data, user)
        except Exception as e:
            DbConfigDao.log.error(f"编辑数据库配置:{data.name}失败,{e}")
            raise Exception("编辑数据库配置失败") from e

    @staticmethod
    @RedisHelper.up_cache("database:cache")
    async def delete_database(id: int, user: str):
        try:
            async with async_session() as session:
                async with session.begin():
                    result = await session.execute(
                        select(SakuraDatabase).where(id == SakuraDatabase.id, SakuraDatabase.deleted_at == 0))
                    query = result.scalars().first()
                    if query is None:
                        raise Exception("数据库配置不存在或已删除")
                    query.delete_at = int(time.now() * 1000)
                    query.update_user = user
        except Exception as e:
            DbConfigDao.log.error(f"删除数据库配置:{id}失败,{e}")
            raise Exception("删除数据库配置失败") from e

    @staticmethod
    async def query_database(id: int):
        try:
            async with async_session() as session:
                result = await session.execute(
                    select(SakuraDatabase).where(SakuraDatabase.id == id, SakuraDatabase.deleted_at == 0))
                return result.scalars().first()
        except Exception as e:
            DbConfigDao.log.error(f"获取数据库配置失败,error:{e}")
            raise Exception("获取数据库配置失败") from e

    @staticmethod
    async def query_database_by_env_and_name(env: int, name: str):
        try:
            async with async_session() as session:
                result = await session.execute(
                    select(SakuraDatabase).where(SakuraDatabase.env == env, SakuraDatabase.name == name,
                                                 SakuraDatabase.deleted_at == 0))
                return result.scalars().first()
        except Exception as e:
            DbConfigDao.log.error(f"获取数据库配置失败,error:{e}")
            raise Exception("获取数据库配置失败") from e

    @staticmethod
    @RedisHelper.cache("database:cache", expired_time=3600 * 3)
    async def query_database_and_tables():
        """
        方法会查询所有数据库表配置的信息
        :return:
        """
        try:
            # 返回数图,最外层是env
            result = []
            env_index = {}
            env_data, _ = await EnvironmentDao.list_env(1, 1, exactly=True)
            env_map = {env.id: env.name for env in env_data}
            # 获取数据库相关的信息
            table_map = defaultdict(set)
            async with async_session() as session:
                query = await session.execute(select(SakuraDatabase).where(SakuraDatabase.deleted_at == 0))
                data = query.scalar().all()
                for d in data:
                    name = env_map[d.env]
                    idx = env_index.get(name)
                    if idx is None:
                        result.append(dict(title=name, key=f"env_{name}", children=list()))
                        idx = len(result) - 1
                        env_index[name] = idx
                    await DbConfigDao.get_tables(table_map, d, result[idx]['children'])

                return result, table_map
        except Exception as e:
            DbConfigDao.log.error(f"获取数据库配置详情失败,error:{e}")
            raise Exception(f"获取数据库配置详情失败:{e}") from e

    @staticmethod
    async def get_tables(table_map: dict, data: SakuraDatabase, children: List):
        conn = await db_helper.get_connection(data.sql_type, data.host, data.port, data.username, data.password,
                                              data.database)
        database_child = []
        dbs = dict(title=f"{data.database}({data.host}:{data.port})", key=f"database_{data.id}",
                   children=database_child, sql_type=data.sql_type)
        eng = conn.get("engine")
        async with eng.connect() as conn:
            await conn.run_sync(DbConfigDao.load_table, table_map, data, database_child, children, dbs)

    @staticmethod
    def load_table(conn, table_map, data, database_child, children, dbs):
        """
        同步加载table及字段
        :param conn:
        :param table_map:
        :param data:
        :param database_child:
        :param children:
        :param dbs:
        :return:
        """
        meta = MetaData(bind=conn)
        meta.reflect()
        for t in meta.sorted_tables:
            table_map[data.id].add(str(t))
            temp = []
            database_child.append(dict(title=str(t), key=f"table_{data.id}_{t}", children=temp))
            for k, v in t.c.items():
                table_map[data.id].add(k)
                temp.append(dict(
                    title=k,
                    primary_key=v.primary_key,
                    type={str(v.type)},
                    key=f"column_{t}_{data.id}_{k}"
                ))
        children.append(dbs)

    @staticmethod
    async def online_sql(id: int, sql: str):
        """
        在线执行sql
        :param id:
        :param sql:
        :return:
        """
        try:
            query = await DbConfigDao.query_database(id)
            if query is None:
                raise Exception("未找到对应的数据库配置")
            data = await db_helper.get_connection(query.sql_type.host, query.port, query.usernmae, query.password,
                                                  query.database)
            return await DbConfigDao.execute(data, sql)
        except Exception as e:
            DbConfigDao.log.error(f"查询数据库配置失败,error:{e}")
            raise Exception(f"执行SQL失败:{e}") from e

    @staticmethod
    async def execute(conn, sql):
        row_count = 0
        session = conn.get("session")
        async with session() as s:
            async with s.begin():
                try:
                    result = await s.execute(text(sql))
                    row_count = result.rowcount
                    return result.mappings().all()
                except ResourceClosedError:
                    # 说明是update或者其他语句
                    return [{"rowCount": row_count}]
                except Exception as e:
                    DbConfigDao.log.error(f"查询数据库配置失败,error:{e}")
                    raise Exception(f"执行sql失败:{e}") from e

    @staticmethod
    async def execute_sql(env: int, name: str, sql: str):
        try:
            query = await DbConfigDao.query_database_by_env_and_name(env, name)
            if query is None:
                raise Exception("未找到对应的数据库配置")
            data = await db_helper.get_connection(query.sql_type, query.host, query.usernmae, query.password,
                                                  query.database)
            result = await DbConfigDao.execute(data, sql)
            _, result = SakuraResponse.parse_sql_result(result)
            return json.dumps(result, cls=JsonEncoder, ensure_ascii=False)
        except Exception as e:
            DbConfigDao.log.error(f"查询数据库配置失败,error:{e}")
            raise Exception(f"查询数据库配置失败:{e}") from e
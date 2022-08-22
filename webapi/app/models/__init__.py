#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/20 09:10
# @Author  : 冉勇
# @Site    : 
# @File    : __init__.py.py
# @Software: PyCharm
# @desc    : orm操作
import time
from datetime import datetime
from typing import List
from sqlalchemy import create_engine  # create_engine创建sql连接
from sqlalchemy.ext.asyncio import AsyncSession  # 异步操作
from sqlalchemy.ext.asyncio import create_async_engine  # 创建engine
from sqlalchemy.ext.declarative import declarative_base  # 建立基本映射类
from sqlalchemy.orm import sessionmaker
from webapi.app.enums.DatabaseEnum import DatabaseEnum
from webapi.config import Config


def create_database():
    engine = create_engine(
        f'mysql+mysqlconnector://{Config.MYSQL_USER}:{Config.MYSQL_PWD}@{Config.MYSQL_HOST}:{Config.MYSQL_PORT}',
        echo=True)
    with engine.connect() as conn:
        conn.execute("CREATE DATABASE IF NOT EXISTS sakura_admin default character set utf8mb4 collate "
                     "utf8mb4_unicode_ci")
        # 关闭引擎
    engine.dispose()


# 优先建库
create_database()

# 同步engine
# engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, pool_recycle=1500)
# 异步engine
async_engine = create_async_engine(Config.ASYNC_SQLALCHEMY_URI, pool_recycle=1500)

async_session = sessionmaker(async_engine, class_=AsyncSession)

# 创建对象的基类
Base = declarative_base()


class DatabaseHelper(object):
    def __init__(self):
        self.connection = {}

    async def get_connection(self, sql_type: int, host: str, port: int, username: str, password: str, database: str):
        # 拼接key
        key = f"{host}:{port}:{database}:{username}:{password}:{database}"
        connection = self.connection.get(key)
        # 先判断是否已连接了，如果有则直接返回
        if connection is not None:
            return connection
        # 获取sqlalchemy需要jdbc url
        jdbc_url = DatabaseHelper.get_jdbc_url(sql_type, host, port, username, password, database)
        # 创建异步引擎
        eg = create_engine(jdbc_url, pool_recycle=1500)
        ss = sessionmaker(bind=eg, class_=AsyncSession)
        # 将数据缓存起来
        data = dict(engine=eg, session=ss)
        self.connection[key] = data
        return data

    @staticmethod
    async def test_connection(ss):
        if ss is None:
            raise Exception("暂不支持的数据库类型")
        async with ss() as session:
            await session.execute("select 1")

    @staticmethod
    def get_jdbc_url(sql_type: int, host: str, port: int, username: str, password: str, database: str):
        if sql_type == DatabaseEnum.MYSQL:
            # mysql模式
            return f"mysql+aiomysql://{username}:{password}@{host}:{port}/{database}"
        if sql_type == DatabaseEnum.POSTGRESQL:
            return f"postgresql+asyncpg://{username}:{password}@{host}:{port}/{database}"
        raise Exception("未知数据库类型")

    def remove_connection(self, host: str, port: int, username: str, password: str, database: str):
        key = f"{host}:{port}:{database}:{username}:{password}:{database}"
        if self.connection.get(key):
            self.connection.pop(key)

    @staticmethod
    def update_model(dist, source, update_user=None, not_null=False):
        """
        更新模型
        :param dist:
        :param source:
        :param update_user:
        :param not_null:
        :return:
        """
        changed = []
        for var, value in vars(source).items():
            if not_null:
                if value is None:
                    continue
                if isinstance(value, bool) or isinstance(value, int) or value:
                    # 如果bool值或者int，false和0也是允许的
                    if not hasattr(dist, var):
                        continue
                    if getattr(dist, var) != value:
                        changed.append(var)
                        setattr(dist, var, value)
            elif getattr(dist, var) != value:
                changed.append(var)
                setattr(dist, var, value)
        if update_user:
            setattr(dist, 'update_user', update_user)
        setattr(dist, 'updated_at', datetime.now())
        return changed

    @staticmethod
    def delete_model(dist, update_user):
        """
        删除数据,兼容老deleted_at
        :param dist:
        :param update_user:
        :return:
        """
        if str(dist.__class__.deleted_at.property.columns[0].type) == "DATETIME":
            dist.deleted_at = datetime.now()
        else:
            dist.deleted_at = int(time.time() * 1000)
        dist.updated_at = datetime.now()
        dist.update_user = update_user

    @classmethod
    def where(cls, params, sentence, condition: List):
        if params is None:
            return cls
        if isinstance(params, bool):
            condition.append(sentence)
            return cls
        if isinstance(params, int):
            condition.append(sentence)
            return cls
        if params:
            condition.append(sentence)
        return cls

    @staticmethod
    async def pagination(page: int, size: int, session, sql: str, scalars=True):
        """
        分页查询
        :param page:
        :param size:
        :param session:
        :param sql:
        :param scalars:
        :return:
        """
        data = await session.execute(sql)
        total = data.raw.rowcount
        if total == 0:
            return [], 0
        sql = sql.offset((page - 1) * size).limit(size)
        data = await session.execute(sql)
        if scalars:
            return data.scalars().all(), total
        return data.all(), total

    @staticmethod
    def like(s: str):
        if s:
            return f"%{s}%"
        return s


db_helper = DatabaseHelper()

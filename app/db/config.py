#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/4 09:54
# @Author  : 冉勇
# @Site    : 
# @File    : config.py
# @Software: PyCharm
# @desc    : 数据库配置文件

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

from app.setting import settings

DATABASE_URL = settings.DATABASE_URI
engine = create_async_engine(DATABASE_URL, future=True, pool_pre_ping=True, pool_recycle=3600)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/6/24 16:10
# @Author  : 冉勇
# @Site    : 
# @File    : database.py
# @Software: PyCharm
# @desc    : 数据连接

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://Sakura_Admin:Sakura_Admin@120.79.24.202:3306/sakura_admin'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, encoding='utf8', echo=True
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

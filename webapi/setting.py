#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/6/29 14:03
# @Author  : 冉勇
# @Site    : 
# @File    : setting.py
# @Software: PyCharm
# @desc    :
import os
import secrets
from typing import List

from pydantic import BaseSettings
from dotenv import dotenv_values

dotenv_config = dotenv_values('.env')


class Settings(BaseSettings):
    BASEDIR = os.path.abspath(os.path.dirname(__file__))  # 项目根目录
    LOG_PATH = os.path.join(BASEDIR, 'logs')  # 日志路径
    BACKEND_CORS_ORIGINS: List = ['*']  # 允许跨域

    # 默认管理员账号密码等信息
    ADMIN_USERNAME = dotenv_config.get('ADMIN_USERNAME', 'admin')  # 管理员账号
    ADMIN_PASSWORD = dotenv_config.get('ADMIN_PASSWORD', '123456')  # 密码
    ADMIN_NICKNAME = dotenv_config.get('ADMIN_NICKNAME', 'admin')  # 管理员昵称
    ADMIN_EMAIL = dotenv_config.get('ADMIN_EMAIL', 'admin@example.com')  # 管理员邮箱

    # 数据库账号密码
    DB_HOST = dotenv_config.get('DB_HOST', '120.79.24.202')  # 数据库地址
    DB_PORT = dotenv_config.get('DB_PORT', 3306)  # 数据库端口
    DB_USER = dotenv_config.get('DB_USER', 'Sakura_Admin')  # 数据库用户名
    DB_PASSWORD = dotenv_config.get('DB_PASSWORD', 'Sakura_Admin')  # 数据库密码
    DB_NAME = dotenv_config.get('DB_NAME', 'sakura_admin')  # 数据库名称

    DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}'
    SQLALCHEMY_DATABASE_URI: str = f'mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

    # Elasticsearch
    ELASTIC_HOST = dotenv_config.get('ELASTIC_HOST', '192.168.1.197')  # Elasticsearch地址
    ELASTIC_PORT = dotenv_config.get('ELASTIC_PORT', 9200)  # Elasticsearch端口

    # 12 Hours
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 12  # token过期时间
    SECRET_KEY: str = secrets.token_urlsafe(32)  # 秘钥


settings = Settings()  # 实例化配置类

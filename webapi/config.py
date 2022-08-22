#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/20 09:25
# @Author  : 冉勇
# @Site    :
# @File    : config.py
# @Software: PyCharm
# @desc    : 基础配置类
import os
from typing import List
from pydantic import BaseSettings

ROOT = os.path.dirname(os.path.abspath(__file__))


class BaseConfig(BaseSettings):
    LOG_DIR = os.path.join(ROOT, 'logs')
    LOG_NAME = os.path.join(LOG_DIR, 'sakura.log')
    SERVER_PORT: int
    HEARTBEAT: int = 48
    # mock_server
    MOCK_ON: bool  # mock开关
    PROXY_ON: bool  # mock代理
    PROXY_PORT: int  # mock端口
    MYSQL_HOST: str  # 数据库主机
    MYSQL_PORT: int  # 数据库端口
    MYSQL_USER: str  # 数据库用户名
    MYSQL_PWD: str  # 数据库密码
    DBNAME: str  # 数据库表名

    # redis_server:关闭redis可以让job同时运行多次
    REDIS_ON: bool  # redis开关
    REDIS_HOST: str  # redis主机
    REDIS_PORT: int  # redis端口
    REDIS_DB: int  # redis表名
    REDIS_PASSWORD: str  # redis密码
    REDIS_NODES: List[dict] = []  # redis连接信息

    # sqlalchemy_server
    SQLALCHEMY_DATABASE_URI: str = ''
    # 异步URI
    ASYNC_SQLALCHEMY_URI: str = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 权限 [0:普通用户、1:组长、2:管理员]
    MEMBER = 0
    MANAGER = 1
    ADMIN = 2

    # github access_token地址
    GITHUB_ACCESS = "https://github.com/login/oauth/access_token"

    # github获取用户信息
    GITHUB_USER = "https://api.github.com/user"

    # client_id 客户端
    CLIENT_ID: str

    # SECRET
    SECRET_KEY: str

    # 测试报告路径
    REPORT_PATH = os.path.join(ROOT, "templates", "report.html")

    # APP路径
    APP_PATH = os.path.join(ROOT, "app")

    # dao路径
    DAO_PATH = os.path.join(APP_PATH, "crud")

    # MD地址
    MARKDOWN_PATH = os.path.join(ROOT, 'templates', "markdown")

    SERVER_REPORT = "http://localhost:8000/#/record/report/"

    OSS_URL = "http://oss.pity.fun"
    # 七牛云链接地址，如果采用七牛oss，需要自行替换
    QINIU_URL = "https://static.pity.fun"
    RELATION = "sakura_relation"
    ALIAS = "__alias__"
    TABLE_TAG = "__tag__"
    # 数据库表展示的变更字段
    FIELD = "__fields__"
    SHOW_FIELD = "__show__"
    IGNORE_FIELDS = ('created_at', "updated_at", "deleted_at", "create_user", "update_user")

    # 测试重跑默认次数
    RETRY_TIMES = 1

    # 日志名
    SAKURA_ERROR = 'sakura_error'
    SAKURA_INFO = 'sakura_info'


class DevConfig(BaseConfig):
    class Config:
        env_file = os.path.join(ROOT, "conf", "dev.env")


class ProConfig(BaseConfig):
    class Config:
        env_file = os.path.join(ROOT, "conf", "pro.env")

    SERVER_REPORT = "http://localhost:8000/#/record/report/"


# 获取sakura环境变量
SAKURA_ENV = os.environ.get("sakura_env", "dev")
# 如果sakura_env存在且为pro
Config = ProConfig() if SAKURA_ENV and SAKURA_ENV.lower() == "pro" else DevConfig()

# 初始化redis
Config.REDIS_NODES = [
    {
        "host": Config.REDIS_HOST, "port": Config.REDIS_PORT, "db": Config.REDIS_DB, "password": Config.REDIS_PASSWORD
    }
]

# 初始化 sqlalchemy（由 apscheduler 使用）
Config.SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(
    Config.MYSQL_USER, Config.MYSQL_PWD, Config.MYSQL_HOST, Config.MYSQL_PORT, Config.DBNAME)

# 初始化sqlalchemy
Config.ASYNC_SQLALCHEMY_URI = f'mysql+aiomysql://{Config.MYSQL_USER}:{Config.MYSQL_PWD}' \
                              f'@{Config.MYSQL_HOST}:{Config.MYSQL_PORT}/{Config.DBNAME}'

BANNER = """
 ______     ______     __  __     __  __     ______     ______    
/\  ___\   /\  __ \   /\ \/ /    /\ \/\ \   /\  == \   /\  __ \   
\ \___  \  \ \  __ \  \ \  _"-.  \ \ \_\ \  \ \  __<   \ \  __ \  
 \/\_____\  \ \_\ \_\  \ \_\ \_\  \ \_____\  \ \_\ \_\  \ \_\ \_\ 
  \/_____/   \/_/\/_/   \/_/\/_/   \/_____/   \/_/ /_/   \/_/\/_/ 
                                                                                                                               
"""

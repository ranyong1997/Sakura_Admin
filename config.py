#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/6/24 17:12
# @Author  : 冉勇
# @Site    : 
# @File    : config.py
# @Software: PyCharm
# @desc    : 配置文件

EVENT = "test"
SECRET_KEY = "4e95f0a14cc530df519cb8c4d77e8eb029fd40ac56fa16be572c58b5ee0b55af"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
redishost = '127.0.0.1'  # redis配置
redisport = '6379'  # redis端口
redisdb = '0'

userid = 14
user_cru = 3
testplan = 'http://127.0.0.1:8000'
host = "120.79.24.202"  # mysql地址
port = 3306  # mysql端口
username = 'Sakura_Admin'  # mysql用户名
password = 'Sakura_Admin'  # mysql密码
db = 'sakura_admin'  # mysql数据库
# 测试服
testhost = "120.79.24.202"  # mysql地址
testport = 3306  # mysql端口
testusername = 'Sakura_Admin'  # mysql用户名
testpassword = 'Sakura_Admin'  # mysql密码
testdb = 'sakura_admin'  # mysql数据库

testredishost = '127.0.0.1'  # redis配置
testredisport = '6379'  # redis端口
testredisdb = '0'

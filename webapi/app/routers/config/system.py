#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/27 17:00
# @Author  : 冉勇
# @Site    : 
# @File    : system.py
# @Software: PyCharm
# @desc    : 系统配置
from fastapi import Depends
from webapi.app.core.configuration import SystemConfiguration
from webapi.app.handler.fatcory import SakuraResponse
from webapi.app.routers.config.gconfig import router
from webapi.app.routers import Permission
from webapi.config import Config


@router.get("/system", description="获取系统配置")
def get_system_config(_=Depends(Permission(Config.ADMIN))):
    configuration = SystemConfiguration.get_config()
    return SakuraResponse.success(configuration)


@router.post("/system/update", description="更新系统配置")
def get_system_config(data: dict, _=Depends(Permission(Config.ADMIN))):
    SystemConfiguration.update_config(data)
    return SakuraResponse.success()

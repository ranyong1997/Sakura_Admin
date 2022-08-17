#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/17 11:39
# @Author  : 冉勇
# @Site    : 
# @File    : script.py
# @Software: PyCharm
# @desc    : 获取脚本
from fastapi import Depends
from webapi.app.handler.fatcory import SakuraResponse
from webapi.app.schema.script import PyScriptForm
from webapi.app.routers import Permission
from webapi.app.routers.online.sql import router

tag = "Python脚本"


@router.post("/script")
def execute_py_script(data: PyScriptForm, user_info=Depends(Permission())):
    try:
        loc = {}
        exec(data.command, loc)
        value = loc.get(data.value)
        return SakuraResponse.success(data=value)
    except Exception as e:
        return SakuraResponse.failed(str(e))

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/28 10:33
# @Author  : 冉勇
# @Site    : 
# @File    : BroadcastReadDao.py
# @Software: PyCharm
# @desc    : 广播(dao)逻辑
from webapi.app.crud import Mapper
from webapi.app.models.broadcast_read_user import SakuraBroadcastReadUser
from webapi.app.utils.decorator import dao
from webapi.app.utils.logger import Log


@dao(SakuraBroadcastReadUser, Log("BroadcastReadDao"))
class BroadcastReadDao(Mapper):
    pass

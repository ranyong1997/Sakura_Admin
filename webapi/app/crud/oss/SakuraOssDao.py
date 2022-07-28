#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/28 11:41
# @Author  : 冉勇
# @Site    : 
# @File    : SakuraOssDao.py
# @Software: PyCharm
# @desc    : OSS(dao)逻辑
from webapi.app.crud import Mapper
from webapi.app.models.oss_file import SakuraOssFile
from webapi.app.utils.decorator import dao
from webapi.app.utils.logger import Log


@dao(SakuraOssFile, Log("SakuraOssDao"))
class SakuraOssDao(Mapper):
    pass

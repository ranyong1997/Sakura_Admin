#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/27 17:00
# @Author  : 冉勇
# @Site    : 
# @File    : configuration.py
# @Software: PyCharm
# @desc    : 配置
import json
import os
from webapi.app.middleware.RedisManager import RedisHelper
from webapi.config import Config, SAKURA_ENV, ROOT


class SystemConfiguration(object):
    """
    系统配置
    """

    @staticmethod
    def config_filename():
        if SAKURA_ENV and SAKURA_ENV.lower() == 'pro':
            return "configuration_pro.json"
        return "configuration_dev.json"

    @staticmethod
    @RedisHelper.cache("configuration", 24 * 3600)
    def get_config():
        try:
            filepath = os.path.join(ROOT, SystemConfiguration.config_filename())
            if not os.path.exists(filepath):
                raise Exception("没找到配置文件,请检查configuration文件是否已经被删除")
            with open(filepath, mode='r', encoding='utf8') as f:
                return json.load(f)
        except Exception as e:
            raise Exception(f"获取系统配置失败,{e}") from e

    @staticmethod
    @RedisHelper.up_cache("configuration")
    def update_config(config):
        try:
            filepath = os.path.join(ROOT, SystemConfiguration.config_filename())
            if not os.path.exists(filepath):
                raise Exception("没找到配置文件,请检查configuration文件是否已经被删除")
            with open(filepath, mode='w', encoding='utf8') as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
        except Exception as e:
            raise Exception(f"更新系统设置失败,{e}") from e

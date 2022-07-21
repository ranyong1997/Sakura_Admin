#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/21 16:57
# @Author  : 冉勇
# @Site    : 
# @File    : logger.py
# @Software: PyCharm
# @desc    : 日志
import inspect
import os
from loguru import logger
from webapi.config import Config


class Log(object):
    business = None

    def __init__(self, name='sakura'):  # Logger标识默认为app
        """
        :param name: 业务名称
        """
        if not os.path.exists(Config.LOG_DIR):
            os.mkdir(Config.LOG_DIR)
        self.business = name

    def info(self, message: str):
        """
        普通日志
        :param message:
        :return:
        """
        file_name, line, func, _, _ = inspect.getframeinfo(inspect.currentframe().f_back)
        logger.bind(name=Config.SAKURA_INFO, func=func, line=line, business=self.business, filename=file_name).debug(
            message)

    def error(self, message: str):
        """
        错误日志
        :param message:
        :return:
        """
        file_name, line, func, _, _ = inspect.getframeinfo(inspect.currentframe().f_back)
        logger.bind(name=Config.SAKURA_ERROR, func=func, line=line, business=self.business, filename=file_name).error(
            message)

    def warning(self, message: str):
        """
        警告日志
        :param message:
        :return:
        """
        file_name, line, func, _, _ = inspect.getframeinfo(inspect.currentframe().f_back)
        logger.bind(name=Config.SAKURA_ERROR, func=func, line=line, business=self.business, filename=file_name).warning(
            message)

    def debug(self, message: str):
        """
        debug日志
        :param message:
        :return:
        """
        file_name, line, func, _, _ = inspect.getframeinfo(inspect.currentframe().f_back)
        logger.bind(name=Config.SAKURA_ERROR, func=func, line=line, business=self.business, filename=file_name).debug(
            message)

    def exception(self, message: str):
        """
        其他日志
        :param message:
        :return:
        """
        file_name, line, func, _, _ = inspect.getframeinfo(inspect.currentframe().f_back)
        logger.bind(name=Config.SAKURA_ERROR, func=func, line=line, business=self.business,
                    filename=file_name).exception(
            message)

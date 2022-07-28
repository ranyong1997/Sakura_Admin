#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/28 14:10
# @Author  : 冉勇
# @Site    : 
# @File    : files.py
# @Software: PyCharm
# @desc    : oss文件CRUD和下载
import random
import time


class OssFile(object):
    _base_path = "sakura"

    async def create_file(self, filepath: str, content, base_path: str = None) -> (str, int):
        raise NotImplementedError

    async def delete_file(self, filepath: str, base_path: str = None):
        raise NotImplementedError

    async def download_file(self, filepath, base_path=None):
        raise NotImplementedError

    async def get_file_object(self, filepath):
        raise NotImplementedError

    def get_real_path(self, filepath, base_path=None):
        return f"{self._base_path if base_path is None else base_path}/{filepath}"

    @staticmethod
    def get_random_filename(filename):
        random_str = list("sakura")
        random.shuffle(random_str)
        return f"{time.time_ns()}_{''.join(random_str)}_{filename}"

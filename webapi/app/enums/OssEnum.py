#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/28 14:06
# @Author  : 冉勇
# @Site    : 
# @File    : OssEnum.py
# @Software: PyCharm
# @desc    : OSS类型
from enum import Enum


class OssEnum(Enum):
    ALIYUN = "aliyun"
    QINIU = "qiniu"
    TENCENT = "cos"

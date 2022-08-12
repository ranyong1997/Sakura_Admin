#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/12 09:12
# @Author  : 冉勇
# @Site    : 
# @File    : CertEnum.py
# @Software: PyCharm
# @desc    : 证书枚举
from enum import IntEnum


class CertType(IntEnum):
    windows = 0
    linux = 1
    macos = 2
    ios = 3
    android = 4

    def get_suffix(self):
        if self == CertType.windows:
            return "p12"
        if self in (CertType.linux, CertType.macos, CertType.ios):
            return "pem"
        if self == CertType.android:
            return "cer"
        raise Exception("不支持的证书类型")

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/17 10:48
# @Author  : 冉勇
# @Site    : 
# @File    : __init__.py.py
# @Software: PyCharm
# @desc    : 初始化服务
from webapi.sakura_proxy.mock import SakuraMock
from webapi.sakura_proxy.record import SakuraRecorder
from webapi.config import Config


async def start_proxy(log):
    """
    启动 mitmproxy 服务器
    :param log:
    :return:
    """
    try:
        from mitmproxy import options
        from mitmproxy.tools.dump import DumpMaster
    except ImportError:
        log.bind(name=None).warning(
            "mitmproxy 未安装，请参阅：https://docs.mitmproxy.org/stable/overview-installation/"
        )
        return

    addons = [
        SakuraRecorder()
    ]
    try:
        if Config.MOCK_ON:
            addons.append(SakuraMock())
        opts = options.Options(listen_host='0.0.0.0', listen_port=Config.PROXY_PORT)
        m = DumpMaster(opts, False, False)
        block_addon = m.addons.get("block")
        m.addons.remove(block_addon)
        m.addons.add(*addons)
        log.bind(name=None).debug(f"Mock服务正在运行,Http://0.0.0.0:{Config.PROXY_PORT}")
        await m.run()
    except Exception as e:
        log.bind(name=None).debug(f"Mock服务运行失败,如果所有节点都运行失败，请检查:{str(e)}")

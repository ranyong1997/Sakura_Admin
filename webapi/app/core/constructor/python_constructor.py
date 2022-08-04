#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/4 14:55
# @Author  : 冉勇
# @Site    : 
# @File    : python_constructor.py
# @Software: PyCharm
# @desc    : python构造函数
import json
from awaits.awaitable import awaitable
from webapi.app.core.constructor.constructor import ConstructorAbstract
from webapi.app.models.constructor import Constructor


class PythonConstructor(ConstructorAbstract):
    @staticmethod
    @awaitable
    def run(executor, env, index, path, params, req_params, constructor: Constructor, **kwargs):
        try:
            executor.append(f"当前路径:{path},第{index + 1}条{ConstructorAbstract.get_name(constructor)}")
            script = json.loads(constructor.constructor_json)
            command = script['command']
            executor.append(f"当前{ConstructorAbstract.get_name(constructor)}类型为python脚本\n{command}")
            loc = {}
            exec(command, loc)
            py_data = loc.get(constructor.value)
            if py_data is None:
                executor.append(f"当前{ConstructorAbstract.get_name(constructor)}未返回任何值")
                return
            if not isinstance(py_data, str):
                py_data = json.dumps(py_data, ensure_ascii=False)
            params[constructor.value] = py_data
            executor.append(f"当前{ConstructorAbstract.get_name(constructor)}返回变量:{constructor.value}\n返回值:\n{py_data}\n")
        except Exception as e:
            raise Exception(
                f"当前路径:{path}->{constructor.name}第{index + 1}个{ConstructorAbstract.get_name(constructor)}执行失败:{str(e)}") from e

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/17 10:12 AM
# @Author  : ranyong
# @Site    : 
# @File    : hr_router.py
# @Software: PyCharm
from fastapi import APIRouter

from httprunner.runner import HttpRunner
from httprunner.models import ProjectMeta, TestCase

router = APIRouter()
runner = HttpRunner()


@router.post("/hrun/debug/testcase", tags=["debug"])
async def debug_single_testcase(project_meta: ProjectMeta, testcase: TestCase):
    resp = {"code": 0, "message": "success", "result": {}}

    if project_meta.debugtalk_py:
        origin_local_keys = list(locals().keys()).copy()
        exec(project_meta.debugtalk_py, {}, locals())
        new_local_keys = list(locals().keys()).copy()
        new_added_keys = set(new_local_keys) - set(origin_local_keys)
        new_added_keys.remove("origin_local_keys")
        for func_name in new_added_keys:
            project_meta.functions[func_name] = locals()[func_name]

    runner.with_project_meta(project_meta).run_testcase(testcase)
    summary = runner.get_summary()

    if not summary.success:
        resp["code"] = 1
        resp["message"] = "fail"

    resp["result"] = summary.dict()
    return resp

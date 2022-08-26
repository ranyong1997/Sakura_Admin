#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/15 15:38
# @Author  : 冉勇
# @Site    : 
# @File    : workspace.py
# @Software: PyCharm
# @desc    : 工作空间
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends
from webapi.app.crud.project.ProjectDao import ProjectDao
from webapi.app.crud.test_case.TestCaseDao import TestCaseDao
from webapi.app.crud.test_case.TestPlan import SakuraTestPlanDao
from webapi.app.handler.fatcory import SakuraResponse
from webapi.app.routers import Permission

router = APIRouter(prefix="/workspace")


@router.get("/", summary="获取工作台用户统计数据", tags=['Notification'])
async def query_user_statistics(user_info=Depends(Permission())):
    user_id = user_info['id']
    count = await ProjectDao.query_user_project(user_id)
    rank = await TestCaseDao.query_user_case_list()
    now = datetime.now()
    weekly_case = await TestCaseDao.query_weekly_user_case(user_id, (now - timedelta(days=7)), now)
    case_count, user_rank = rank.get(str(user_id), [0, 0])
    return SakuraResponse.success(dict(project_count=count, case_count=case_count,
                                       weekly_case=weekly_case, user_rank=user_rank, total_user=len(rank)))


@router.get("/testplan", summary="获取用户关注的测试计划执行数据", tags=['Notification'])
async def query_follow_testplan(user_info=Depends(Permission())):
    user_id = user_info['id']
    ans = await SakuraTestPlanDao.query_user_follow_test_plan(user_id)
    return SakuraResponse.success(ans)

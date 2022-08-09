#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/5 11:26
# @Author  : 冉勇
# @Site    : 
# @File    : TestResult.py
# @Software: PyCharm
# @desc    : 测试结果
from datetime import datetime
from typing import List
from sqlalchemy import asc
from sqlalchemy.future import select
from webapi.app.models import async_session
from webapi.app.models.result import SakuraTestResult
from webapi.app.models.test_case import TestCase
from webapi.app.utils.logger import Log


class TestResultDao(object):
    log = Log("TestResultDao")

    @staticmethod
    async def insert(report_id: int, case_id: int, case_name: str, status: int, case_log: str, start_at: datetime,
                     finished_at: datetime, url: str, body: str, request_method: str, request_headers: str, cost: str,
                     asserts: str, response_headers: str, response: str, status_code: int, cookies: str,
                     retry: int = None, request_params: str = "", data_name: str = "", data_id: int = None) -> None:
        try:
            async with async_session() as session:
                async with session.begin():
                    result = SakuraTestResult(report_id, case_id, case_name, status,
                                              case_log, start_at, finished_at,
                                              url, body, request_method, request_headers, cost,
                                              asserts, response_headers, response, status_code,
                                              cookies, retry, request_params, data_name, data_id)
                    session.add(result)
                    await session.flush()
        except Exception as e:
            TestResultDao.log.error(f"新增测试结果失败:{str(e)}")
            raise Exception(f"新增测试结果失败:{str(e)}") from e

    @staticmethod
    async def list(report_id: int) -> List[SakuraTestResult]:
        try:
            async with async_session() as session:
                sql = select(SakuraTestResult, TestCase.directory_id).join(TestCase,
                                                                           TestCase.id == SakuraTestResult.case_id). \
                    where(SakuraTestResult.report_id == report_id, SakuraTestResult.delete_at == 0).order_by(
                    asc(SakuraTestResult.case_id), asc(SakuraTestResult.start_at))
                data = await session.execute(sql)
                ans = []
                for res, directory_id in data.all():
                    res.directory_id = directory_id
                    ans.append(res)
                return ans
        except Exception as e:
            TestResultDao.log.error(f"获取测试用例执行记录失败:{str(e)}")
            raise Exception(f"获取测试用例执行记录失败:{str(e)}") from e

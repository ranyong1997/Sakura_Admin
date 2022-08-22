#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/5 11:25
# @Author  : 冉勇
# @Site    : 
# @File    : TestReport.py
# @Software: PyCharm
# @desc    : 测试报告
from datetime import datetime
from sqlalchemy import select, desc
from webapi.app.crud import Mapper
from webapi.app.crud.test_case.TestResult import TestResultDao
from webapi.app.models import async_session
from webapi.app.models.report import SakuraReport
from webapi.app.models.test_plan import SakuraTestPlan
from webapi.app.utils.logger import Log


class TestReportDao(object):
    log = Log("TestReportDao")

    @staticmethod
    async def start(executor: int, env: int, mode: int = 0, plan_id: int = None) -> int:
        """
        生成buildId,开始执行任务,任务完成后通过回调方法更新报告
        :param executor:
        :param env:
        :param mode:
        :param plan_id:
        :return:
        """
        try:
            async with async_session() as session:
                async with session.begin():
                    report = SakuraReport(executor, env, mode=mode, plan_id=plan_id)
                    session.add(report)
                    await session.flush()
                    return report.id
        except Exception as e:
            TestReportDao.log.error(f"新增报告失败:{str(e)}")
            raise Exception(f"新增报告失败:{str(e)}") from e

    @staticmethod
    async def update(report_id: int, status) -> None:
        try:
            async with async_session() as session:
                async with session.begin():
                    sql = select(SakuraReport).where(SakuraReport.id == report_id)
                    data = await session.execute(sql)
                    report = data.scalars().first()
                    if report is None:
                        raise Exception("更新报告失败")
                    report.status = status
                    await session.flush()
        except Exception as e:
            TestReportDao.log.error(f"更新报告失败:{str(e)}")
            raise Exception(f"更新报告失败:{str(e)}") from e

    @staticmethod
    async def end(report_id: int, success_count: int, failed_count: int, error_count: int, skipped_count: int,
                  status: int, cost: str) -> SakuraReport:
        try:
            async with async_session() as session:
                async with session.begin():
                    sql = select(SakuraReport).where(SakuraReport.id == report_id)
                    data = await session.execute(sql)
                    report = data.scalars().first()
                    if report is None:
                        raise Exception("更新报告失败")
                    report.status = status
                    report.success_count = success_count
                    report.failed_count = failed_count
                    report.error_count = error_count
                    report.skipped_count = skipped_count
                    report.cost = cost
                    report.finished_at = datetime.now()
                    await session.flush()
                    session.expunge(report)
                    return report
        except Exception as e:
            TestReportDao.log.error(f"更新报告失败:{str(e)}")
            raise Exception(f"更新报告失败:{str(e)}") from e

    @staticmethod
    async def query(report_id: int):
        """
        根据报告id查询报告
        :param report_id:
        :return:
        """
        try:
            async with async_session() as session:
                sql = select(SakuraReport, SakuraTestPlan.name) \
                    .outerjoin(SakuraTestPlan, SakuraTestPlan.id == SakuraReport.plan_id) \
                    .where(SakuraReport.id == report_id)
                data = await session.execute(sql)
                if data is None:
                    raise Exception("报告不存在")
                report, plan_name = data.first()
                test_data = await TestResultDao.list(report_id)
                return report, test_data, plan_name
        except Exception as e:
            TestReportDao.log.error(f"查询报告失败:{str(e)}")
            raise Exception(f"查询报告失败:{str(e)}") from e

    @staticmethod
    async def list_report(page: int, size: int, start_time: datetime, end_time: datetime, executor: int or str = None):
        """
        获取报告列表
        :param page:
        :param size:
        :param start_time:
        :param end_time:
        :param executor:
        :return:
        """
        try:
            async with async_session() as session:
                sql = session(SakuraReport).where(SakuraReport.start_at.between(start_time, end_time)).order_by(
                    desc(SakuraReport.start_at))
                if executor is not None:
                    executor = executor if executor != "CPU" else 0
                    sql = sql.where(SakuraReport.executor == executor)
                data = await session.execute(sql)
                total = data.raw.rowcount
                if total == 0:
                    return [], 0
                sql = sql.offset((page - 1) * size).limit(size)
                data = await session.execute(sql)
                return data.scalars().all(), total
        except Exception as e:
            TestReportDao.log.error(f"查询构建记录失败:{str(e)}")
            raise Exception(f"查询构建记录失败:{str(e)}") from e

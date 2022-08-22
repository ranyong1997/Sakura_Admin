#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/29 15:41
# @Author  : 冉勇
# @Site    : 
# @File    : TestPlan.py
# @Software: PyCharm
# @desc    : 测试计划
import asyncio
import time
from copy import deepcopy
from sqlalchemy import select, and_, or_, null
from webapi.app.crud import Mapper, ModelWrapper
from webapi.app.crud.project.ProjectDao import ProjectDao
from webapi.app.enums.OperationEnum import OperationType
from webapi.app.models import async_session
from webapi.app.models.report import SakuraReport
from webapi.app.models.test_plan import SakuraTestPlan
from webapi.app.models.testplan_follow_user import SakuraTestPlanFollowUserRel
from webapi.app.schema.test_plan import SakuraTestPlanForm


@ModelWrapper(SakuraTestPlan)
class SakuraTestPlanDao(Mapper):
    @classmethod
    async def list_test_plan(cls, page: int, size: int, project_id: int = None, name: str = '', priority: str = '',
                             role: str = None, create_user: int = None,
                             user_id: int = None, follow: bool = None):
        try:
            async with async_session() as session:
                conditions = [SakuraTestPlan.deleted_at == 0]
                if project_id:
                    SakuraTestPlanDao.where(project_id, SakuraTestPlan.project_id == project_id, conditions)
                else:
                    # 找出用户能看到的项目
                    projects = await ProjectDao.list_project_id_by_user(session, user_id, role)
                    if projects is None:
                        # 说明用户一个项目都没有，不需要继续查询了
                        return [], 0
                    if len(projects) > 0:
                        cls.where(projects, SakuraTestPlan.project_id.in_(projects), conditions)
                cls.where(name, SakuraTestPlan.name.like(f"%{name}%"), conditions) \
                    .where(priority, SakuraTestPlan.priority == priority, conditions) \
                    .where(create_user, SakuraTestPlan.create_user == create_user, conditions)
                if follow is None:
                    sql = select(SakuraTestPlan, SakuraTestPlanFollowUserRel.id) \
                        .outerjoin(SakuraTestPlanFollowUserRel,
                                   and_(
                                       SakuraTestPlanFollowUserRel.user_id == user_id,
                                       SakuraTestPlanFollowUserRel.deleted_at == 0,
                                       SakuraTestPlanFollowUserRel.plan_id == SakuraTestPlan.id)) \
                        .where(*conditions)
                elif follow:
                    sql = select(SakuraTestPlan, SakuraTestPlanFollowUserRel.id) \
                        .outerjoin(SakuraTestPlanFollowUserRel,
                                   SakuraTestPlanFollowUserRel.plan_id == SakuraTestPlan.id,
                                   ).where(*conditions, SakuraTestPlanFollowUserRel.user_id == user_id,
                                           SakuraTestPlanFollowUserRel.deleted_at == 0)
                else:
                    sql = select(SakuraTestPlan, null().label('null_bar')) \
                        .outerjoin(SakuraTestPlanFollowUserRel,
                                   SakuraTestPlanFollowUserRel.plan_id == SakuraTestPlan.id).where(
                        *conditions, or_(SakuraTestPlanFollowUserRel.id == None,
                                         SakuraTestPlanFollowUserRel.deleted_at != 0))
                result, total = await cls.pagination(page, size, session, sql, False)
                return result, total
        except Exception as e:
            cls.__log__.error(f"获取测试计划失败: {str(e)}")
            raise Exception(f"获取测试计划失败: {str(e)}") from e

    @staticmethod
    async def insert_test_plan(plan: SakuraTestPlanForm, user: int) -> SakuraTestPlan:
        try:
            async with async_session() as session:
                async with session.begin():
                    query = await session.execute(
                        select(SakuraTestPlan).where(SakuraTestPlan.project_id == plan.project_id,
                                                     SakuraTestPlan.name == plan.name,
                                                     SakuraTestPlan.deleted_at == 0))
                    if query.scalars().first() is not None:
                        raise Exception("测试计划已存在")
                    test_plan = SakuraTestPlan(**plan.dict(), user=user)
                    session.add(test_plan)
                    await session.flush()
                    await session.refresh(test_plan)
                    session.expunge(test_plan)
                    return test_plan
        except Exception as e:
            SakuraTestPlanDao.__log__.error(f"新增测试计划失败:{str(e)}")
            raise Exception(f"新增测试计划失败:{str(e)}") from e

    @classmethod
    async def update_test_plan(cls, plan: SakuraTestPlanForm, user: int, log=False):
        try:
            async with async_session() as session:
                async with session.begin():
                    query = await session.execute(
                        session(SakuraTestPlan).where(SakuraTestPlan.id == plan.id, SakuraTestPlan.deleted_at == 0))
                    data = query.scalars().first()
                    if data is None:
                        raise Exception("测试计划不存在")
                    old = deepcopy(data)
                    plan.env = ",".join(map(str, plan.env))
                    plan.receiver = ",".join(map(str, plan.receiver))
                    plan.case_list = ",".join(map(str, plan.case_list))
                    plan.msg_type = ",".join(map(str, plan.msg_type))
                    changed = cls.update_model(data, plan, user)
                    await session.flush()
                    session.expunge(data)
                if log:
                    async with session.begin():
                        await asyncio.create_task(
                            cls.insert_log(session, user, OperationType.UPDATE, data, old, plan.id, changed))
        except Exception as e:
            SakuraTestPlanDao.__log__.exception(f"编辑测试计划失败:{str(e)}")
            SakuraTestPlanDao.__log__.error(f"编辑测试计划失败:{str(e)}")
            raise Exception(f"编辑失败:{str(e)}") from e

    @staticmethod
    async def update_test_plan_state(id: int, state: int):
        try:
            async with async_session() as session:
                async with session.begin():
                    query = await session.execute(
                        select(SakuraTestPlan).where(SakuraTestPlan.id == id, SakuraTestPlan.deleted_at == 0))
                    data = query.scalars().first()
                    if data is None:
                        raise Exception("测试计划不存在")
                    data.state = state
        except Exception as e:
            SakuraTestPlanDao.__log__.error(f"编辑测试计划失败:{str(e)}")
            raise Exception(f"编辑测试计划失败:{str(e)}") from e

    @staticmethod
    async def query_test_plan(id: int) -> SakuraTestPlan:
        try:
            async with async_session() as session:
                sql = select(SakuraTestPlan).where(SakuraTestPlan.deleted_at == 0, SakuraTestPlan.id == id)
                data = await session.execute(sql)
                return data.scalars().first()
        except Exception as e:
            SakuraTestPlanDao.__log__.error(f"获取测试计划失败:{str(e)}")
            raise Exception(f"获取测试计划:{str(e)}") from e

    @staticmethod
    async def follow_test_plan(plan_id: int, user_id: int):
        """
        关注测试计划
        :param plan_id:
        :param user_id:
        :return:
        """
        async with async_session() as session:
            async with session.begin():
                sql = session(SakuraTestPlanFollowUserRel).where(SakuraTestPlanFollowUserRel.deleted_at == 0,
                                                                 SakuraTestPlanFollowUserRel.plan_id == plan_id,
                                                                 SakuraTestPlanFollowUserRel.user_id == user_id)
                data = await session.execute(sql)
                ans = data.scalars().first()
                if ans is not None:
                    raise Exception("已经关注过此测试计划")
                model = SakuraTestPlanFollowUserRel(plan_id, user_id)
                session.add(model)

    @staticmethod
    async def unfollow_test_plan(plan_id: int, user_id: int):
        """
        取关测试计划
        :param plan_id:
        :param user_id:
        :return:
        """
        async with async_session() as session:
            async with session.begin():
                sql = session(SakuraTestPlanFollowUserRel).where(SakuraTestPlanFollowUserRel.deleted_at == 0,
                                                                 SakuraTestPlanFollowUserRel.plan_id == plan_id,
                                                                 SakuraTestPlanFollowUserRel.user_id == user_id)
                data = await session.execute(sql)
                ans = data.scalars().first()
                if ans is None:
                    raise Exception("已取关过此测试计划")
                ans.deleted_at = int(time.time() * 1000)

    @staticmethod
    async def query_user_follow_test_plan(user_id: int):
        """
        根据用户id查询出用户关注的测试计划执行数据
        :param uesr_id:
        :return:
        """
        ans = []
        async with async_session() as session:
            # 找到最近7次通过率
            sql = select(SakuraTestPlan, SakuraTestPlanFollowUserRel.id) \
                .outerjoin(SakuraTestPlanFollowUserRel, SakuraTestPlanFollowUserRel.plan_id == SakuraTestPlan.id).where(
                SakuraTestPlanFollowUserRel.user_id == user_id,
                SakuraTestPlanFollowUserRel.deleted_at == 0,
                SakuraTestPlan.deleted_at == 0)
            data = await session.execute(sql)
            for d in data.scalars().all():
                reports = list()
                query = await session.execute(select(SakuraReport).where(SakuraReport.plan_id == d.id).order_by(
                    SakuraReport.start_at.desc()).limit(7))
                for report in query.scalars().all():
                    reports.append(report)
                ans.append({
                    "plan": d,
                    "report": reports
                })
        return ans

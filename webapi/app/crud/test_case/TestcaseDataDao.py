#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/2 16:43
# @Author  : 冉勇
# @Site    : 
# @File    : TestcaseDataDao.py
# @Software: PyCharm
# @desc    : 测试用例数据(dao)逻辑
from collections import defaultdict
from typing import List
from sqlalchemy import select
from webapi.app.crud import Mapper, ModelWrapper
from webapi.app.models import async_session, DatabaseHelper
from webapi.app.models.testcase_data import SakuraTestCaseData
from webapi.app.schema.testcase_data import SakuraTestcaseDataForm


@ModelWrapper(SakuraTestCaseData)
class SakuraTestCaseDataDao(Mapper):

    @classmethod
    async def list_testcase_data(cls, case_id: int):
        """
        列出测试数据
        :param case_id:
        :return:
        """
        ans = defaultdict(list)
        try:
            async with async_session() as session:
                sql = select(SakuraTestCaseData).where(SakuraTestCaseData.case_id == case_id,
                                                       SakuraTestCaseData.deleted_at == 0)
                result = await session.execute(sql)
                query = result.scalars().all()
                for q in query:
                    ans[q.env].append(q)
                return ans
        except Exception as e:
            cls.__log__.error(f"查询测试数据失败:{str(e)}")
            raise Exception(f"查询测试数据失败:{str(e)}") from e

    @classmethod
    async def list_testcase_data_by_env(cls, env: int, case_id: int) -> List[SakuraTestCaseData]:
        try:
            async with async_session() as session:
                sql = select(SakuraTestCaseData).where(SakuraTestCaseData.case_id == case_id,
                                                       SakuraTestCaseData.env == env,
                                                       SakuraTestCaseData.deleted_at == 0)
                result = await session.execute(sql)
                return result.scalars().all()
        except Exception as e:
            cls.__log__.error(f"查询测试数据失败:{str(e)}")
            raise Exception(f"查询测试数据失败:{str(e)}") from e

    @classmethod
    async def insert_testcase_data(cls, form: SakuraTestcaseDataForm, user_id: int):
        """
        插入测试数据
        :param form:
        :param user_id:
        :return:
        """
        try:
            async with async_session() as session:
                async with session.begin():
                    sql = select(SakuraTestCaseData).where(SakuraTestCaseData.case.id == form.case_id,
                                                           SakuraTestCaseData.env == form.env,
                                                           SakuraTestCaseData.name == form.name,
                                                           SakuraTestCaseData.deleted_at == 0)
                    result = await session.execute(sql)
                    query = result.scalars().first()
                    if query is None:
                        raise Exception("该数据已存在,请重新编辑")
                    data = SakuraTestCaseData(**form.dict(), user_id=user_id)
                    session.add(data)
                    await session.flush()
                    await session.refresh()
                    session.expunge()
                    return data
        except Exception as e:
            cls.__log__.error(f"新增测试数据失败:{str(e)}")
            raise Exception(f"新增测试数据失败:{str(e)}") from e

    @classmethod
    async def update_testcase_data(cls, form: SakuraTestcaseDataForm, user: int):
        """
        更新测试数据
        :param form:
        :param user:
        :return:
        """
        try:
            async with async_session() as session:
                async with session.begin():
                    sql = select(SakuraTestCaseData).where(SakuraTestCaseData.id == form.id,
                                                           SakuraTestCaseData.deleted_at == 0)
                    result = await session.execute(sql)
                    query = result.scalars().first()
                    if query is None:
                        raise Exception("测试数据不存在")
                    DatabaseHelper.update_model(query, form, user)
                    await session.flush()
                    session.expunge(query)
                    return query
        except Exception as e:
            cls.__log__.error(f"更新测试数据失败:{str(e)}")
            raise Exception(f"更新测试数据失败:{str(e)}") from e

    @classmethod
    async def delete_testcase_data(cls, id: int, user: int):
        """
        删除测试数据
        :param id:
        :param user:
        :return:
        """
        try:
            async with async_session() as session:
                async with session.begin():
                    sql = select(SakuraTestCaseData).where(SakuraTestCaseData.id == id,
                                                           SakuraTestCaseData.deleted_at == 0)
                    result = await session.execute(sql)
                    query = result.scalars().first()
                    if query is None:
                        raise Exception("测试数据不存在")
                    DatabaseHelper.delete_model(query, user)
        except Exception as e:
            cls.__log__.error(f"删除测试数据失败:{str(e)}")
            raise Exception(f"删除测试数据失败:{str(e)}") from e

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/1 15:38
# @Author  : 冉勇
# @Site    : 
# @File    : TestCaseAssertsDao.py
# @Software: PyCharm
# @desc    : 测试用例断言(dao)逻辑
from typing import List
from sqlalchemy import asc, select
from webapi.app.crud import Mapper, ModelWrapper
from webapi.app.models import async_session, DatabaseHelper
from webapi.app.models.testcase_asserts import TestCaseAsserts
from webapi.app.schema.testcase_schema import TestCaseAssertsForm


@ModelWrapper(TestCaseAsserts)
class TestCaseAssertsDao(Mapper):
    @classmethod
    async def list_test_case_asserts(cls, case_id: int) -> List[TestCaseAsserts]:
        """
        通过用例id获取断言数据
        :param case_id:
        :return:
        """
        try:
            async with async_session() as session:
                query = await session.execute(select(TestCaseAsserts).where(TestCaseAsserts.case_id == case_id,
                                                                            TestCaseAsserts.deleted_at == 0)).order_by(
                    asc(TestCaseAsserts.name))
                return query.scalars().all()
        except Exception as e:
            cls.__log__.error(f"获取用例断言失败:{str(e)}")
            raise Exception(f"获取用例断言失败:{str(e)}") from e

    @staticmethod
    async def insert_test_case_asserts(form: TestCaseAssertsForm, user_id: int):
        """
        新增用例断言
        :param form:
        :param user_id:
        :return:
        """
        try:
            ans = None
            async with async_session() as session:
                async with session.begin():
                    sql = select(TestCaseAsserts).where(TestCaseAsserts.case_id == form.case_id,
                                                        TestCaseAsserts.name == form.name,
                                                        TestCaseAsserts.deleted_at == 0)
                    result = await session.execute(sql)
                    data = result.scalars().first()
                    if data is not None:
                        raise Exception("断言信息已存在,请检查")
                    new_assert = TestCaseAsserts(**form.dict(), user_id=user_id)
                    session.add(new_assert)
                    await session.flush()
                    await session.refresh(new_assert)
                    session.expunge(new_assert)
                    return new_assert
            return ans
        except Exception as e:
            TestCaseAssertsDao.__log__.error(f"新增用例断言失败:{e}")
            raise Exception(f"新增用例断言失败:{e}") from e

    @classmethod
    async def update_test_case_asserts(cls, form: TestCaseAssertsForm, user_id: int) -> TestCaseAsserts:
        """
        更新用例断言
        :param form:
        :param user_id:
        :return:
        """
        try:
            async with async_session() as session:
                async with session.begin():
                    sql = select(TestCaseAsserts).where(TestCaseAsserts.id == form.id,
                                                        TestCaseAsserts.deleted_at == 0)
                    result = await session.execute(sql)
                    data = result.scalars().first()
                    if data is None:
                        raise Exception("断言信息不存在,请检查")
                    DatabaseHelper.updata_model(data, form, user_id)
                    await session.flush()
                    session.expunge(data)
                    return data
        except Exception as e:
            cls.__log__.error(f"更新用例断言失败:{e}")
            raise Exception(f"更新用例断言失败:{e}") from e

    @classmethod
    async def delete_test_case_asserts(cls, id: int, user_id: int) -> None:
        try:
            async with async_session() as session:
                async with session.begin():
                    sql = select(TestCaseAsserts).where(TestCaseAsserts.id == id,
                                                        TestCaseAsserts.deleted_at == 0)
                    result = await session.execute(sql)
                    data = result.scalars().first()
                    if data is None:
                        raise Exception("编辑用例断言失败")
        except Exception as e:
            cls.__log__.error(f"编辑用例断言失败:{e}")
            raise Exception(f"编辑用例断言失败:{e}") from e

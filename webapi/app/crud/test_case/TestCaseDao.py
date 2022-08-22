#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/1 14:04
# @Author  : 冉勇
# @Site    : 
# @File    : TestCaseDao.py
# @Software: PyCharm
# @desc    :  测试用例(dao)逻辑
import json
from datetime import datetime, timedelta
from typing import List, Dict
from sqlalchemy import desc, func, and_, asc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from webapi.app.crud import Mapper, ModelWrapper, connect
from webapi.app.crud.test_case.ConstructorDao import ConstructorDao
from webapi.app.crud.test_case.TestCaseAssertsDao import TestCaseAssertsDao
from webapi.app.crud.test_case.TestCaseDirectory import SakuraTestcaseDirectoryDao
from webapi.app.crud.test_case.TestCaseOutParametersDao import SakuraTestCaseOutParametersDao
from webapi.app.crud.test_case.TestcaseDataDao import SakuraTestCaseDataDao
from webapi.app.enums.ConstructorEnum import ConstructorType
from webapi.app.middleware.RedisManager import RedisHelper
from webapi.app.models import async_session
from webapi.app.models.constructor import Constructor
from webapi.app.models.out_parameters import SakuraTestCaseOutParameters
from webapi.app.models.project import Project
from webapi.app.models.test_case import TestCase
from webapi.app.models.testcase_asserts import TestCaseAsserts
from webapi.app.models.testcase_data import SakuraTestCaseData
from webapi.app.models.user import User
from webapi.app.schema.testcase_schema import TestCaseForm, TestCaseInfo


@ModelWrapper(TestCase)
class TestCaseDao(Mapper):

    @classmethod
    async def list_test_case(cls, directory_id: int = None, name: str = "", create_user: str = None):
        try:
            filters = [TestCase.deleted_at == 0]
            if directory_id:
                parents = await SakuraTestcaseDirectoryDao.get_directory_son(directory_id)
                filters = [TestCase.deleted_at == 0, TestCase.directory_id.in_(parents)]
                if name:
                    filters.append(TestCase.name.like(f"%{name}%"))
                if create_user:
                    filters.append(TestCase.created_user == create_user)
            async with async_session() as session:
                sql = select(TestCase).where(*filters).order_by(TestCase.name.asc())
                result = await session.execute(sql)
                return result.scalars().all()
        except Exception as e:
            cls.__log__.error(f"获取测试用例失败:{str(e)}")
            raise Exception(f"获取测试用例失败:{str(e)}") from e

    @staticmethod
    async def get_test_case_by_directory_id(directory_id: int):
        try:
            async with async_session() as session:
                sql = select(TestCase).where(TestCase.deleted_at == 0,
                                             TestCase.directory_id == directory_id).order_by(TestCase.name.asc())
                result = await session.execute(sql)
                ans = []
                case_map = {}
                for item in result.scalars():
                    ans.append({"title": item.name, "key": f"testcase_{item.id}"})
                    case_map[item.id] = item.name
                return ans, case_map
        except Exception as e:
            TestCaseDao.__log__.error(f"获取测试用例失败:{str(e)}")
            raise Exception(f"获取测试用例失败:{str(e)}") from e

    @staticmethod
    async def get_case_children(case_id: int):
        data = await TestCaseAssertsDao.list_test_case_asserts(case_id)
        return [dict(key=f"asserts_{d.id}", title=d.name, case_id=case_id) for d in data]

    @staticmethod
    async def get_case_children_length(case_id: int):
        data = await TestCaseAssertsDao.list_test_case_asserts(case_id)
        return len(data)

    @staticmethod
    async def _insert(session, case_id: int, user_id: int, form: TestCaseInfo, **fields: tuple):
        for field, model_info in fields.items():
            md, model = model_info
            field_data = getattr(form, field)
            for f in field_data:
                if hasattr(f, "case_id"):
                    setattr(f, "case_id", case_id)
                    data = model(**f.dict(), user_id=user_id)
                else:
                    data = model(**f.dict(), user_id=user_id, case_id=case_id)
                await md.insert_record(data, ss=session)

    @staticmethod
    async def insert_test_case(session, data: TestCaseInfo, user_id: int) -> None:
        """
        插入测试用例
        :param session:
        :param data:
        :param user_id:
        :return:
        """
        query = await session.execute(
            select(TestCase).where(TestCase.directory_id == data.case.directory_id, TestCase.name == data.case.name,
                                   TestCase.deleted_at == 0))
        if query.scalars().first() is not None:
            raise Exception("用例名称已存在")
        cs = TestCase(**data.case.dict(), create_user=user_id)
        # 添加用例,之后添加其他数据
        session.add(cs)
        await session.flush()
        session.expunge(cs)
        await TestCaseDao._insert(
            session, cs.id, user_id, data, contstructor=(ConstructorDao, Constructor),
            asserts=(TestCaseDao, TestCaseAsserts),
            out_parameters=(SakuraTestCaseOutParametersDao, SakuraTestCaseOutParameters),
            data=(SakuraTestCaseDataDao, SakuraTestCaseData))
        return cs

    @classmethod
    async def update_test_case(cls, test_case: TestCaseForm, user_id: int) -> TestCase:
        """
        编辑测试用例
        :param test_case:
        :param user_id:
        :return:
        """
        try:
            async with async_session() as session:
                async with session.begin():
                    query = await session.execute(
                        select(TestCase).where(TestCase.id == test_case.id, TestCase.deleted_at == 0))
                    data = query.scalars().first()
                    if data is None:
                        raise Exception("用例不存在")
                    cls.update_model(data, test_case, user_id)
                    await session.flush()
                    # 释放你的sql数据
                    session.expunge(data)
                    return data
        except Exception as e:
            cls.__log__.error(f"编辑用例失败:{str(e)}")
            raise Exception(f"编辑用例失败:{str(e)}") from e

    @staticmethod
    async def query_test_case(case_id: int) -> dict:
        """
        查询测试用例
        :param case_id:
        :return:
        """
        try:
            async with async_session() as session:
                sql = select(TestCase).where(TestCase.id == case_id, TestCase.deleted_at == 0)
                result = await session.execute(sql)
                data = result.scalars().first()
                if data is None:
                    raise Exception("用例不存在")
                # 获取断言部分
                asserts = await TestCaseAssertsDao.async_list_test_case_asserts(data.id)
                # 获取数据构造器
                constructors = await ConstructorDao.list_constructor(case_id)
                constructors_case = await TestCaseDao.query_test_case_by_constructors(constructors)
                test_data = await SakuraTestCaseDataDao.list_testcase_data(case_id=case_id)
                parameters = await SakuraTestCaseOutParametersDao.list_record(case_id=case_id,
                                                                              _sort=(
                                                                                  asc(SakuraTestCaseOutParameters.id),))
                return dict(asserts=asserts, constructors=constructors, case=data, constructors_case=constructors_case,
                            test_data=test_data, out_parameters=parameters)
        except Exception as e:
            TestCaseDao.__log__.error(f"用例查询失败:{str(e)}")
            raise Exception(f"用例查询失败:{str(e)}") from e

    @staticmethod
    async def query_test_case_by_constructors(constructors: List[Constructor]):
        try:
            # 找到所有用例名称
            constructors = [json.loads(x.constructor_json).get("case_id") for x in constructors if x.type == 0]
            async with async_session() as session:
                sql = select(TestCase).where(TestCase.id.in_(constructors), TestCase.deleted_at == 0)
                result = await session.execute(sql)
                data = result.scalars().all()
                return {x.id: x for x in data}
        except Exception as e:
            TestCaseDao.__log__.error(f"查询用例失败:{str(e)}")
            raise Exception(f"查询用例失败:{str(e)}") from e

    @staticmethod
    async def async_query_test_case(case_id) -> [TestCase, str]:
        try:
            async with async_session() as session:
                result = await session.execute(
                    select(TestCase).where(TestCase.id == case_id, TestCase.deleted_at == 0))
                data = result.scalars().first()
                if data is None:
                    return None, "用例不存在"
                return data, None
        except Exception as e:
            TestCaseDao.__log__.error(f"查询用例失败:{str(e)}")
            return None, f"查询用例失败: {str(e)}"

    @staticmethod
    async def list_testcase_tree(cls, projects: List[Project]) -> [List, dict]:
        try:
            result = []
            project_map = []
            project_index = {}
            for p in projects:
                project_map[p.id] = p.name
                result.append({
                    "label": p.name,
                    "value": p.id,
                    "key": p.id,
                    "children": []
                })
                project_index[p.id] = len(result) - 1
            async with async_session() as session:
                query = await session.execute(select(TestCase).where(
                    TestCase.project_id.in_(project_map.keys()),
                    TestCase.deleted_at == 0
                ))
                data = query.scalars().all()
                for d in data:
                    result[project_index[d.project_id]]['children'].append({
                        "label": d.name,
                        "value": d.id,
                        "key": d.id
                    })
                return result
        except Exception as e:
            cls.__log__.error(f"获取用例列表失败:{str(e)}")
            raise Exception(f"获取用例列表失败:{str(e)}") from e

    @staticmethod
    async def select_constructor(case_id: int) -> List[Constructor]:
        """
        通过case_id获取用例构造数据
        :param case_id:
        :return:
        """
        try:
            async with async_session() as session:
                query = await session.execute(select(Constructor).where(Constructor.case_id == case_id,
                                                                        Constructor.deleted_at == 0
                                                                        )).order_by(
                    desc(Constructor.created_at))
                return query.scalars().all()
        except Exception as e:
            TestCaseDao.__log__.error(f"查询构造数据失败:{str(e)}")
            raise Exception(f"查询构造数据失败:{str(e)}") from e

    @staticmethod
    async def async_select_constructor(case_id: int) -> List[Constructor]:
        """
        异步获取用例构造数据
        :param case_id:
        :return:
        """
        try:
            async with async_session() as session:
                sql = select(Constructor).where(Constructor.case_id == case_id,
                                                Constructor.deleted_at == 0).order_by(Constructor.created_at)
                data = await session.execute(sql)
                return data.scalars().all()
        except Exception as e:
            TestCaseDao.__log__.error(f"查询构数据失败:{str(e)}")
            raise Exception(f"查询构数据失败:{str(e)}") from e

    @staticmethod
    async def collect_data(case_id: int, data: List):
        """
        收集以case_id为前置条件的数据
        :param case_id:
        :param data:
        :return:
        """
        # 先获取数据构造器(前置条件)
        pre = dict(id=f"pre_{case_id}", label="前置条件", children=list())
        suffix = dict(id=f"suffix_{case_id}", label="后置条件", children=list())
        await TestCaseDao.collect_asserts(case_id, pre, suffix)
        data.append(pre)
        # 获取断言
        asserts = dict(id=f"asserts_{case_id}", label="断言", children=list())
        await TestCaseDao.collect_data(case_id, asserts)
        data.append(asserts)
        data.append(suffix)

    @staticmethod
    async def collect_constructor(case_id, parent, suffix):
        constructors = await TestCaseDao.async_select_constructor(case_id)
        for c in constructors:
            temp = dict(id=f"constructor_{c.id}", label=f"{c.name}", children=list())
            if c.type == ConstructorType.testcase:
                # 说明是用例,继续递归
                temp["label"] = "[CASE]:" + temp["label"]
                json_data = json.loads(c.constructor_json)
                await TestCaseDao.collect_data(json_data.get("case_id"), temp.get("children"))
            elif c.type == ConstructorType.sql:
                temp["label"] = "[SQL]:" + temp["label"]
            elif c.type == ConstructorType.redis:
                temp["label"] = "[REDIS]:" + temp["label"]
            elif c.type == ConstructorType.py_script:
                temp["label"] = "[PyScript]:" + temp["label"]
            elif c.type == ConstructorType.http:
                temp["label"] = "[HTTP Request]:" + temp["label"]
            # 否则正常添加数据
            if c.suffix:
                suffix.get("children").append(temp)
            else:
                parent.get("children").append(temp)

    @staticmethod
    async def collect_asserts(case_id, parent):
        """
        收集断言
        :param case_id:
        :param parent:
        :return:
        """
        asserts = await TestCaseAssertsDao.async_list_test_case_asserts(case_id)
        for a in asserts:
            temp = dict(id=f"assert_{a.id}", label=f"{a.name}", children=list())
            parent.get("children").append(temp)

    @staticmethod
    async def get_xmind_data(case_id: int):
        """
        获取xmind数据
        :param case_id:
        :return:
        """
        data = await TestCaseDao.query_test_case(case_id)
        cs = data.get("case")
        # 开始解析测试数据
        result = dict(id=f"case_{case_id}", label=f"{cs.name}({cs.id})")
        children = []
        await TestCaseDao.collect_data(case_id, children)
        result["children"] = children
        return result

    @classmethod
    async def generate_sql(cls):
        return select(TestCase.create_user, func.count(TestCase.id)) \
            .outerjoin(User, and_(User.deleted_at == 0, TestCase.create_user == User.id)).where(
            TestCase.deleted_at == 0).group_by(TestCase.create_user).order_by(
            desc(func.count(TestCase.id)))

    @staticmethod
    @RedisHelper.cache("rank")
    @connect
    async def query_user_case_list(cls, session: AsyncSession = None) -> Dict[str, List]:
        """
        查询用户case数量和排名
        :return:
        """
        ans = {}
        sql = await cls.generate_sql()
        query = await session.execute(sql)
        for i, q in enumerate(query.all()):
            user, count = q
            ans[str(user)] = [count, i + 1]
        return ans

    @staticmethod
    @RedisHelper.cache("rank_detail")
    @connect
    async def query_user_case_rank(cls, session: AsyncSession = None) -> List:
        """
        查询每周用户案例
        :param cls:
        :param session:
        :return:
        """
        ans = []
        sql = await cls.generate_sql()
        query = await session.execute(sql)
        for i, q in enumerate(query.all()):
            user, count = q
            ans.append(dict(id=user, count=count, rank=i + 1))
        return ans

    @staticmethod
    async def query_weekly_user_case(user_id: int, start_time: datetime, end_time: datetime) -> List:
        ans = dict()
        async with async_session() as session:
            async with session.begin():
                sql = select(TestCase.created_at, func.count(TestCase.id)).where(
                    TestCase.create_user == user_id,
                    TestCase.deleted_at == 0, TestCase.created_at.between(start_time, end_time)).group_by(
                    TestCase.created_at).order_by(asc(TestCase.created_at))
                query = await session.execute(sql)
                for i, q in enumerate(query.all()):
                    date, count = q
                    ans[date.strftime("%Y-%m-%d")] = count
        return await TestCaseDao.fill_data(start_time, end_time, ans)

    @staticmethod
    async def fill_data(start_time: datetime, end_time: datetime, data: dict):
        """
        填补数据
        :param start_time:
        :param end_time:
        :param data:
        :return:
        """
        start = start_time
        ans = []
        while start <= end_time:
            date = start.strftime("%Y-%m-%d")
            ans.append(dict(date=date, count=data.get(date, 0)))
            start += timedelta(days=1)
        return ans

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/1 14:12
# @Author  : 冉勇
# @Site    : 
# @File    : ConstructorDao.py
# @Software: PyCharm
# @desc    : 构造函数(dao)逻辑
from collections import defaultdict
from typing import List
from sqlalchemy import select, update
from webapi.app.crud import Mapper, ModelWrapper
from webapi.app.models import async_session, DatabaseHelper
from webapi.app.models.constructor import Constructor
from webapi.app.models.test_case import TestCase
from webapi.app.schema.constructor import ConstructorIndex, ConstructorForm


@ModelWrapper(Constructor)
class ConstructorDao(Mapper):
    @staticmethod
    async def list_constructor(case_id: int) -> List[Constructor]:
        """
        根据用例id获取数据结构器列表
        :param case_id:
        :return:
        """
        try:
            async with async_session() as session:
                sql = select(Constructor).where(Constructor.case_id == case_id, Constructor.deleted_at == 0) \
                    .order_by(Constructor.index, Constructor.updated_at)
                result = await session.execute(sql)
                return result.scalars().all()
        except Exception as e:
            ConstructorDao.__log__.error(f"获取初始化数据失败, {e}")
            raise Exception(f"获取初始化数据失败,{e}") from e

    @staticmethod
    async def insert_constructor(data: ConstructorForm, user_id: int) -> None:
        try:
            async with async_session() as session:
                async with session.begin():
                    sql = select(Constructor).where(Constructor.case_id == data.case_id, Constructor.name == data.name,
                                                    Constructor.deleted_at == 0)
                    result = await session.execute(sql)
                    if result.scalars().first() is not None:
                        raise Exception(f"{data.name}已存在")
                    constructor = Constructor(**data.dict(), user_id=user_id)
                    constructor.index = await constructor.get_index(session, data.case_id)
                    session.add(constructor)
        except Exception as e:
            ConstructorDao.__log__.error(f"新增前/后置条件:{data.name}失败,{e}")
            raise Exception(f"新增前/后置条件失败,{e}") from e

    @staticmethod
    async def update_constructor(data: ConstructorForm, user_id: int) -> None:
        """
        更新前后置条件
        :param data:
        :param user_id:
        :return:
        """
        try:
            async with async_session() as session:
                async with session.begin():
                    sql = select(Constructor).where(Constructor.id == data.id)
                    result = await session.execute(sql)
                    query = result.scalars().first()
                    if query is None:
                        raise Exception(f"{data.name}不存在")
                    DatabaseHelper.updata_model(query, data, user_id)
        except Exception as e:
            ConstructorDao.__log__.error(f"编辑前/后置条件:{data.name}失败,{e}")
            raise Exception(f"编辑前/后置条件失败,{e}") from e

    @classmethod
    async def delete_constructor(cls, id: int, user_id: int) -> None:
        """
        删除前/后置条件
        :param id:
        :param user_id:
        :return:
        """
        try:
            async with async_session() as session:
                async with session.begin():
                    sql = select(Constructor).where(Constructor.id == id)
                    result = await session.execute(sql)
                    query = result.scalars().first()
                    if query is None:
                        raise Exception(f"前/后置条件{id}不存在")
                    DatabaseHelper.delete_model(query, user_id)
        except Exception as e:
            cls.__log__.error(f"删除前/后置条件:{id}失败,{e}")
            raise Exception(f"删除前/后置条件失败,{e}")

    @classmethod
    async def update_constructor_index(cls, data: List[ConstructorIndex]) -> None:
        """
        更改前/后置条件顺序
        :param data:
        :return:
        """
        try:
            async with async_session() as session:
                async with session.begin():
                    for item in data:
                        await session.execute(
                            update(Constructor).where(Constructor.id == item.id).values(index=item.index)
                        )
        except Exception as e:
            cls.__log__.error(f"更新前/后置条件顺序失败,{e}")
            raise Exception(f"更新前/后置条件顺序失败,{e}") from e

    @classmethod
    async def get_constructor_tree(cls, name: str, suffix: bool) -> List[dict]:
        try:
            async with async_session() as session:
                # 获取所有构造函数
                search = [Constructor.public == True, Constructor.suffix == suffix, Constructor.deleted_at == 0]
                if name:
                    search.append(Constructor.name.like("%{}%".format(name)))
                query = await session.execute(select(Constructor).where(*search))
                constructor = query.scalars().first()
                if not constructor:
                    return []
                temp = defaultdict(list)
                # 建立caseID -> constructor的map
                for c in constructor:
                    temp[c.case_id].append(c)
                query = await session.execute(select(TestCase).where(TestCase.id.in_(temp.keys())))
                testcases = query.scalars().all()
                testcase_info = {t.id: t for t in testcases}
                result = []
                for k, v in temp.items():
                    result.append({
                        "key": f"caseId_{k}",
                        "disabled": True,
                        "title": testcase_info[k].name,
                        "children": [
                            {"key": f"constructor_{x.id}", "title": x.name, "value": f"constructor_{x.id}"} for x in v
                        ]
                    })
                return result
        except Exception as e:
            cls.__log__.error(f"获取前/后置条件树失败,{e}")
            raise Exception("获取前/后置条件失败") from e

    @staticmethod
    async def get_constructor_data(id_: int) -> None:
        """
        根据构造方法id获取构造方法数据
        :param id_:
        :return:
        """
        async with async_session() as session:
            query = await session.execute(select(Constructor).where(Constructor.id == id_, Constructor.deleted_at == 0))
            data = query.scalars().first()
            if data is None:
                raise Exception("前/后置条件不存在")
            return data

    @staticmethod
    async def get_case_and_constructor(constructor_type: int, suffix: bool) -> List[dict]:
        """
        根据构造类型返回构造方法树
        :param constructor_type:
        :param suffix:
        :return:
        """
        ans = list()
        async with async_session() as session:
            # 此处存放case_id -> 前置条件的映射
            constructors = defaultdict(list)
            # 根据传入的前后置条件类型,找出所有的前置条件,类型一致,共享打开
            query = await session.execute(
                select(Constructor).where(
                    Constructor.suffix == suffix,
                    Constructor.type == constructor_type,
                    Constructor.public == True,
                    Constructor.deleted_at == 0
                ))
            # 并把这些前置条件放到constructors里面
            for q in query.scalars().all():
                constructors[q.case_id].append(
                    {
                        "title": q.name,
                        "key": f"constructor_{q.id}",
                        "isLeaf": True,
                        "constructor_json": q.constructor_json
                    })
            if len(constructors.keys()) == 0:
                return []
            # 二次查询,查出有前置条件的case
            query = await session.execute(
                select(TestCase).where(TestCase.id.in_(constructors.keys()), TestCase.deleted_at == 0))
            for q in query.scalars().all():
                # 把用例id放入cs_list,这里就不用原生join了
                ans.append({
                    "title": q.name,
                    "key": f"caseId_{q.id}",
                    "disabled": True,
                    "children": constructors[q.id]
                })
        return ans

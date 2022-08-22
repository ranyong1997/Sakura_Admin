#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/2 10:30
# @Author  : 冉勇
# @Site    : 
# @File    : TestCaseDirectory.py
# @Software: PyCharm
# @desc    : 测试用例目录(dao)逻辑
import time
from collections import defaultdict
from datetime import datetime
from sqlalchemy import select, asc, or_
from webapi.app.crud import Mapper
from webapi.app.models import async_session
from webapi.app.schema.testcase_directory import SakuraTestcaseDirectoryForm
from webapi.app.models.testcase_directory import SakuraTestcaseDirectory
from webapi.app.utils.logger import Log


class SakuraTestcaseDirectoryDao(Mapper):
    log = Log("SakuraTestcaseDirectoryDao")

    @staticmethod
    async def query_directory(directory_id: int):
        """
        查询目录
        :param directory_id:
        :return:
        """
        try:
            async with async_session() as session:
                sql = select(SakuraTestcaseDirectory).where(SakuraTestcaseDirectory.id == directory_id,
                                                            SakuraTestcaseDirectory.deleted_at == 0)
                result = await session.execute(sql)
                return result.scalars().first()
        except Exception as e:
            SakuraTestcaseDirectoryDao.log.error(f"获取目录详情失败:{str(e)}")
            raise Exception(f"获取目录详情失败:{str(e)}") from e

    @staticmethod
    async def list_directory(project_id: int):
        """
        列出目录
        :param project_id:
        :return:
        """
        try:
            async with async_session() as session:
                sql = select(SakuraTestcaseDirectory).where(SakuraTestcaseDirectory.deleted_at == 0,
                                                            SakuraTestcaseDirectory.project_id == project_id) \
                    .order_by(asc(SakuraTestcaseDirectory.name))
                result = await session.execute(sql)
                return result.scalars().all()
        except Exception as e:
            SakuraTestcaseDirectoryDao.log.error(f"获取用例目录失败:{str(e)}")
            raise Exception(f"获取用例目录失败:{str(e)}") from e

    @staticmethod
    async def insert_directory(form: SakuraTestcaseDirectoryForm, user: int):
        """
        插入目录
        :param form:
        :param user:
        :return:
        """
        try:
            async with async_session() as session:
                sql = select(SakuraTestcaseDirectory).where(SakuraTestcaseDirectory.deleted_at == 0,
                                                            SakuraTestcaseDirectory.name == form.name,
                                                            SakuraTestcaseDirectory.parent == form.parent,
                                                            SakuraTestcaseDirectory.project_id == form.project_id)
                result = await session.execute(sql)
                if result.scalars().first() is not None:
                    raise Exception("目录已存在")
                session.add(SakuraTestcaseDirectory(form, user))
        except Exception as e:
            SakuraTestcaseDirectoryDao.log.error(f"创建目录失败:{str(e)}")
            raise Exception(f"创建目录失败:{str(e)}") from e

    @staticmethod
    async def update_directory(form: SakuraTestcaseDirectoryForm, user: int):
        try:
            async with async_session() as session:
                async with session.begin():
                    sql = select(SakuraTestcaseDirectory).where(SakuraTestcaseDirectory.id == form.id,
                                                                SakuraTestcaseDirectory.deleted_at == 0)
                    result = await session.execute(sql)
                    query = result.scalars().first()
                    if query is None:
                        raise Exception("目录不存在")
                    query.name = form.name
                    query.update_user = user
                    query.updated_at = datetime.now()
        except Exception as e:
            SakuraTestcaseDirectoryDao.log.error(f"更新目录失败:{str(e)}")
            raise Exception(f"更新目录失败:{str(e)}") from e

    @staticmethod
    async def delete_directory(id: int, user: int):
        """
        删除目录
        :param id:
        :param user:
        :return:
        """
        try:
            async with async_session() as session:
                async with session.begin():
                    sql = select(SakuraTestcaseDirectory).where(SakuraTestcaseDirectory.id == id,
                                                                SakuraTestcaseDirectory.deleted_at == 0)
                    result = await session.execute(sql)
                    query = result.scalars().first()
                    if query is None:
                        raise Exception("目录不存在")
                    query.deleted_at = int(time.time() * 1000)
                    query.update_user = user
        except Exception as e:
            SakuraTestcaseDirectoryDao.log.error(f"删除目录失败:{str(e)}")
            raise Exception(f"删除目录失败:{str(e)}") from e

    @staticmethod
    async def get_directory_tree(project_id: int, case_node=None, move: bool = False) -> (list, dict):
        """
        获取目录树
        :param project_id:
        :param case_node:
        :param move:
        :return:
        """
        res = await SakuraTestcaseDirectoryDao.list_directory((project_id))
        ans = []
        ans_map = {}
        case_map = {}
        parent_map = defaultdict(list)
        for directory in res:
            if directory.parent is None:
                # 如果没有父级,说明是底层数据
                ans.append(dict(
                    title=directory.name,
                    key=directory.id,
                    children=list()
                ))
            else:
                parent_map[directory.parent].append(directory.id)
            ans_map[directory.id] = directory
        # 获取到所有数据信息
        for r in ans:
            await SakuraTestcaseDirectoryDao.get_directory(ans_map, parent_map, r.get('ket'), r.get('children'),
                                                           case_map, case_node, move)
            if not move and not r.get('children'):
                r['disabled'] = True
        return ans, case_map

    @staticmethod
    async def get_directory(ans_map:dict, parent_map, parent, children, case_map, case_node=None, move=False):
        current = parent_map.get(parent)
        if case_node is not None:
            nodes, cs = await case_node(parent)
            children.extend(nodes)
            case_map.update(cs)
        if current is None:
            return
        for c in current:
            temp = ans_map.get(c)
            if case_node is None:
                child = []
            else:
                child, cs = await case_node(temp.id)
                case_map.update(cs)
            children.append(dict(
                title=temp.name,
                key=temp.id,
                children=child,
                disabled=len(child) == 0 and not move
            ))
            await SakuraTestcaseDirectoryDao.get_directory(ans_map, parent_map, temp.id, child, case_node, move=move)

    @staticmethod
    async def get_directory_son(directory_id: int):
        """
        获取目录子级菜单
        :param directory_id:
        :return:
        """
        parent_map = defaultdict(list)
        async with async_session() as session:
            ans = [directory_id]
            # 找出父类为directory_id 或者非根的目录
            sql = select(SakuraTestcaseDirectory) \
                .where(SakuraTestcaseDirectory.deleted_at == 0,
                       or_(SakuraTestcaseDirectory.parent == directory_id, SakuraTestcaseDirectory.parent != None)) \
                .order_by(asc(SakuraTestcaseDirectory.name))
            result = await session.execute(sql)
            data = result.scalars().all()
            for d in data:
                parent_map[d.parent].append(d.id)
            son = parent_map.get(directory_id)
            SakuraTestcaseDirectoryDao.get_sub_son(parent_map, son, ans)
            return ans

    @staticmethod
    def get_sub_son(parent_map: dict, son: list, result: list):
        """
        获取提交的子级菜单
        :param parent_map:
        :param son:
        :param result:
        :return:
        """
        if not son:
            return
        for s in son:
            result.append(s)
            sons = parent_map.get(s)
            if not sons:
                continue
            result.extend(sons)
            SakuraTestcaseDirectoryDao.get_sub_son(parent_map, sons, result)

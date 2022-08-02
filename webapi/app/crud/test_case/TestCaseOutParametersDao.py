#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/2 16:13
# @Author  : 冉勇
# @Site    : 
# @File    : TestCaseOutParametersDao.py
# @Software: PyCharm
# @desc    : 测试用例输出参数(dao)逻辑
import time
from datetime import datetime
from typing import List
from sqlalchemy import select, update
from webapi.app.crud import Mapper, ModelWrapper
from webapi.app.middleware.RedisManager import RedisHelper
from webapi.app.models import async_session
from webapi.app.models.out_parameters import SakuraTestCaseParameters
from webapi.app.schema.testcase_out_parameters import SakuraTestCaseOutParametersForm


@ModelWrapper(SakuraTestCaseParameters)
class SakuraTestCaseOutParametersDao(Mapper):

    @classmethod
    async def should_remove(cls, before, after):
        """
        找出要删除的数据
        :param before:
        :param after:
        :return:
        """
        data = []
        for b in before:
            for a in after:
                # for..else 语法:https://blog.csdn.net/weixin_48728769/article/details/123796020
                if a.id == b.id:
                    break
            else:
                data.append(b.id)
        return data

    @classmethod
    @RedisHelper.up_cache("dao")
    async def update_many(cls, case_id: int, data: List[SakuraTestCaseOutParametersForm], user_id: int):
        """
        批量更新数据
        :param case_id:
        :param data:
        :param user_id:
        :return:
        """
        result = []
        try:
            async with async_session() as session:
                async with session.begin():
                    source = await session.execute(select(SakuraTestCaseParameters).where(
                        SakuraTestCaseParameters.case_id == case_id,
                        SakuraTestCaseParameters.deleted_at == 0))
                    before = source.scalars().all()
                    should_remove = await cls.should_remove(before, data)
                    for item in data:
                        if item.id is None:
                            # 添加
                            temp = SakuraTestCaseParameters(**item.dict(), case_id=case_id, user_id=user_id)
                            session.add(temp)
                        else:
                            query = await session.execute(select(SakuraTestCaseParameters).where(
                                SakuraTestCaseParameters.id == item.id))
                            temp = query.scalars().all()
                            if temp is None:
                                # 新逻辑
                                temp = SakuraTestCaseParameters(**item.dict(), case_id=case_id, user_id=user_id)
                                session.add(temp)
                            else:
                                temp.name = item.name
                                temp.case_id = case_id
                                temp.expression = item.expression
                                temp.source = item.source
                                temp.match_index = item.match_index
                                temp.update_user = user_id
                                temp.updated_at = datetime.now()
                        await session.flush()
                        session.expunge(temp)
                        result.append(temp)
                    if should_remove:
                        await session.execute(
                            update(SakuraTestCaseParameters).where(
                                SakuraTestCaseParameters.id.in_(should_remove)
                            ).values(delete_at=int(time.time() * 1000)))
            return result
        except Exception as e:
            cls.__log__.error(f"批量更新出参数失败:{str(e)}")
            raise Exception(f"批量更新出参数失败:{str(e)}") from e

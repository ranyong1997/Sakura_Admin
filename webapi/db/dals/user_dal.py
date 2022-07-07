#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/4 16:29
# @Author  : 冉勇
# @Site    : 
# @File    : user_dal.py
# @Software: PyCharm
# @desc    :
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from webapi.db.models import User


class UserDAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def authenticate(self, *, username, password):
        q = await self.db_session.execute(select(User).where(User.username == username))
        user = q.scalar()
        if not user:
            return None
        if not User.verify_password(password, user.password_hash):
            return None
        return user

    async def get(self, *, id):
        q = await self.db_session.execute(select(User).where(User.id == id))
        user = q.scalar()
        return user

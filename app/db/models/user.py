#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/4 11:30
# @Author  : 冉勇
# @Site    : 
# @File    : user.py
# @Software: PyCharm
# @desc    :
from sqlalchemy import Text, Integer, Column, String
from passlib.context import CryptContext
from app.db.config import Base

pwd_context = context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, index=True)
    password_hash = Column(String(255))
    nickname = Column(String(64), unique=True, index=True)
    email = Column(String(64), unique=True, index=True)
    about_me = Column(Text)

    # generate hash password
    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    # verify login password
    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        return pwd_context.verify(password, hashed_password)

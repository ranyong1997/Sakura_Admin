#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/6/25 8:58 AM
# @Author  : ranyong
# @Site    : 
# @File    : schemas.py
# @Software: PyCharm
from pydantic import BaseModel, Field
from typing import Optional, List


class UserBase(BaseModel):  # 用户基础信息
    username: str


class UserCreate(UserBase):  # 用户创建信息
    password: str
    role: str
    jobnum: Optional[int] = None
    studentnum: Optional[int] = None
    sex: str = "男"
    age: int


class UserLogin(UserBase):  # 用户登录
    password: str


class UsersToken(UserBase):  # 用户token
    token: str


class UsernameRole(UserBase):  # 用户角色
    role: str


class UserChangepassword(BaseModel):  # 用户修改密码
    password: str
    newpassword: str


class MessageConent(BaseModel):  # 消息内容
    id: int
    connect: str


class RebackMessConnet(MessageConent):  # 回复信息
    rebackid: int


class Messages(BaseModel):  # 消息
    id: int
    senduser: str
    acceptusers: str
    read: bool
    sendtime: str
    addtime: str
    context: str


class MessagePid(Messages):  # 消息id
    pid: int


class MessageOne(Messages):  # 查询单条消息
    pid: List[MessagePid] = []


class Courses(BaseModel):  # 课程信息
    name: str
    icon: Optional[str]
    desc: Optional[str]
    catalog: Optional[str]
    onsale: Optional[int]
    owner: str
    likenum: int


class CoursesCommentBase(BaseModel):  # 课程评论基础信息
    users: str
    pid: int
    addtime: str
    context: str


class Coursescomment(CoursesCommentBase):  # 课程评论
    id: int
    top: int


class CoursesEdit(Courses):  # 课程修改信息
    id: int


class CousesDetail(Courses):  # 课程详情
    id: int
    commonet: List[Coursescomment] = []


class Coursecomment(BaseModel):  # 课程评论
    id: int
    comments: str
    pid: Optional[int]

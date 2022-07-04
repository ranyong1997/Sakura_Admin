#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/4 14:34
# @Author  : 冉勇
# @Site    : 
# @File    : comment.py
# @Software: PyCharm
# @desc    :
from datetime import datetime
from typing import Optional, List, Type
from pydantic import BaseModel, fields, EmailStr


class CommentCreateAdmin(BaseModel):
    post_id: int
    body: str
    replied_id: int = None


class CommentCreateAnonymous(CommentCreateAdmin):
    author: str = fields.Field(..., max_length=30)
    email: EmailStr = fields.Field(...)


class CommentCreate(BaseModel):
    post_id: int
    body: str
    author: str = fields.Field(..., max_length=30)
    email: EmailStr = fields.Field(...)
    from_admin: bool = False
    reviewed: bool = False
    replied_id: int = None


class CommentsListOutItemPost(BaseModel):
    id: int
    title: str

    class Config:
        orm_mode = True


class CommentsListOutItem(BaseModel):
    id: int
    author: str
    timestamp: datetime
    from_admin: bool
    reviewed: bool
    email: str
    body: str
    post: CommentsListOutItemPost

    class Config:
        orm_mode = True


class CommentsListOut(BaseModel):
    total: int
    items: List[CommentsListOutItem]


class CommentInUpdate(BaseModel):
    reviewed: bool = None

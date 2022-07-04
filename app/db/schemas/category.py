#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/4 14:17
# @Author  : 冉勇
# @Site    : 
# @File    : category.py
# @Software: PyCharm
# @desc    :
from typing import Optional, List
from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(CategoryBase):
    pass


class CategoryAllOutItem(BaseModel):
    id: int
    name: str
    posts: int

    class Config:
        orm_mode = True


class CategoryAllOut(BaseModel):
    total: int
    items: List[CategoryAllOutItem]


class CategorySelectionOutItem(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class CategorySelectionOut(BaseModel):
    __root__: List[CategorySelectionOutItem]

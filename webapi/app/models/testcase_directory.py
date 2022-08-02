#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/2 11:00
# @Author  : 冉勇
# @Site    : 
# @File    : testcase_directory.py
# @Software: PyCharm
# @desc    : 测试用例目录树
from datetime import datetime
from sqlalchemy import Column, INT, String, UniqueConstraint
from webapi.app.models.basic import SakuraBase
from webapi.app.schema.testcase_directory import SakuraTestcaseDirectoryForm


class SakuraTestcaseDirectory(SakuraBase):
    """
    用例目录表
    """
    __tablename__ = 'sakura_testcase_directory'
    # 联合索引,防止同一层次出现同名目录
    __table_args__ = (
        UniqueConstraint('project_id', 'name', 'parent', 'deleted_at')
    )
    id = Column(INT, primary_key=True)
    project_id = Column(INT, index=True)
    # 目录名称
    name = Column(String(18), nullable=False)
    # 目录上级目录,如果没有则为None
    parent = Column(INT)

    def __init__(self, form: SakuraTestcaseDirectoryForm, user):
        super().__init__(user)
        self.project_id = form.project_id
        self.name = form.name
        self.parent = form.parent
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.created_user = user
        self.update_user = user

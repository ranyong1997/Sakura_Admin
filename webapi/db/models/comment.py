#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/4 11:14
# @Author  : 冉勇
# @Site    : 
# @File    : comment.py
# @Software: PyCharm
# @desc    :
import datetime

from sqlalchemy import TEXT, Integer, Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from webapi.db.config import Base


class Comment(Base):
    __tablename__ = 'Comment'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.datetime.now, index=True)
    from_admin = Column(Boolean, default=False)
    reviewed = Column(Boolean, default=False)
    author = Column(String(30))
    email = Column(String(254))
    body = Column(TEXT)
    replied_id = Column(Integer, ForeignKey('Comment.id'))
    post_id = Column(Integer, ForeignKey('Post.id'))
    post = relationship('Post', back_populates='comments')
    replies = relationship('Comment', back_populates='replied', cascade='all, delete-orphan')
    replied = relationship('Comment', back_populates='replies', remote_side=[id])

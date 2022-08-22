'''
Descripttion: 
version: 
Author: 冉勇
Date: 2022-08-05 11:27:36
LastEditTime: 2022-08-19 10:26:39
'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/5 11:27
# @Author  : 冉勇
# @Site    : 
# @File    : result.py
# @Software: PyCharm
# @desc    : 测试结果
from datetime import datetime
from sqlalchemy import INT, Column, TIMESTAMP, String, BIGINT, SMALLINT, TEXT
from webapi.app.models import Base


class SakuraTestResult(Base):
    __tablename__ = "sakura_test_result"
    id = Column(INT, primary_key=True)
    directory_id = None
    # 报告id
    report_id = Column(INT, index=True)
    # 测试用例id
    case_id = Column(INT, index=True)
    # 测试用例名字
    case_name = Column(String(32))
    # 状态码
    status = Column(SMALLINT, comment="对应状态 0:成功 1:失败 2:出错 3:跳过")
    # 开始时间
    start_at = Column(TIMESTAMP, nullable=False)
    # 结束时间
    finished_at = Column(TIMESTAMP, nullable=False)
    # 测试日志
    case_log = Column(TEXT)
    # 重试次数,预留字段
    retry = Column(INT, default=0)
    # Http状态码
    status_code = Column(INT)
    # url
    url = Column(TEXT)
    # body
    body = Column(TEXT)
    # request_params
    request_params = Column(TEXT)
    # data_name
    data_name = Column(String(24))
    # data_id
    data_id = Column(INT)
    # request_method
    request_method = Column(String(12), nullable=True)
    # request_headers
    request_headers = Column(TEXT)
    # cost
    cost = Column(String(12), nullable=False)
    # 断言
    asserts = Column(TEXT)
    # response_headers
    response_headers = Column(TEXT)
    # response
    response = Column(TEXT)
    # cookies
    cookies = Column(TEXT)
    # deleted_at
    deleted_at = Column(BIGINT, nullable=False, default=0)

    def __init__(self, report_id: int, case_id: int, case_name: str, status: int,
                 case_log: str, start_at: datetime, finished_at: datetime,
                 url: str, body: str, request_method: str, request_headers: str, cost: str,
                 asserts: str, response_headers: str, response: str,
                 status_code: int, cookies: str, retry: int = None,
                 request_params: str = '', data_name: str = '', data_id: int = None):
        self.report_id = report_id
        self.case_id = case_id
        self.case_name = case_name
        self.status = status
        self.case_log = case_log
        self.start_at = start_at
        self.finished_at = finished_at
        self.url = url
        self.body = body
        self.request_method = request_method
        self.request_headers = request_headers
        self.cost = cost
        self.asserts = asserts
        self.response_headers = response_headers
        self.response = response
        self.status_code = status_code
        self.cookies = cookies
        self.retry = retry
        self.request_params = request_params
        self.data_name = data_name
        self.data_id = data_id
        self.deleted_at = 0

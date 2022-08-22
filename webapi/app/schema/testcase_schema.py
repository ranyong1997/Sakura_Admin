#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/1 15:40
# @Author  : 冉勇
# @Site    : 
# @File    : testcase_schema.py
# @Software: PyCharm
# @desc    : 测试用例表单
from typing import List
from pydantic import BaseModel, validator
from webapi.app.excpetions.ParamsException import ParamsError
from webapi.app.schema.base import SakuraModel
from webapi.app.schema.constructor import ConstructorForm
from webapi.app.schema.request import RequestInfo
from webapi.app.schema.testcase_data import SakuraTestcaseDataForm
from webapi.app.schema.testcase_out_parameters import SakuraTestCaseOutParametersForm


class TestCaseForm(BaseModel):
    id: int = None
    priority: str
    url: str = ""
    name: str = ""
    case_type: int = 0
    base_path: str = None
    tag: str = None
    body: str = None
    body_type: int = 0
    request_headers: str = None
    request_method: str = None
    status: int
    out_parameters: List[SakuraTestCaseOutParametersForm] = []
    directory_id: int
    request_type: int

    @validator("priority", "status", "directory_id", "request_type", "url", "name")
    def name_not_empty(cls, v):
        if isinstance(v, str) and len(v.strip()) == 0:
            raise ParamsError("不能为空")
        return v


class TestCaseAssertsForm(BaseModel):
    id: int = None
    name: str
    case_id: str
    assert_type: str
    expected: str
    actually: str

    @validator("name", "assert_type", "expected", "actually")
    def name_not_empty(cls, v):
        return SakuraModel.not_empty(v)


class TestCaseInfo(BaseModel):
    case: TestCaseForm = None
    asserts: List[TestCaseAssertsForm] = []
    data: List[SakuraTestcaseDataForm] = []
    constructor: List[ConstructorForm] = []
    out_parameters: List[SakuraTestCaseOutParametersForm] = []

    @validator("case")
    def name_not_empty(cls, v):
        return SakuraModel.not_empty(v)


class TestCaseGeneratorForm(BaseModel):
    directory_id: int
    requests: List[RequestInfo]
    name: str

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/12 14:22
# @Author  : 冉勇
# @Site    : 
# @File    : testcase.py
# @Software: PyCharm
# @desc    : 测试用例生成
import json
from datetime import datetime
from typing import List, TypeVar
from fastapi import APIRouter, Depends, UploadFile, File, Request
from webapi.app.core.request import get_convertor
from webapi.app.core.request.generator import CaseGenerator
from webapi.app.crud.project.ProjectRoleDao import ProjectRoleDao
from webapi.app.crud.test_case.ConstructorDao import ConstructorDao
from webapi.app.crud.test_case.TestCaseAssertsDao import TestCaseAssertsDao
from webapi.app.crud.test_case.TestCaseDao import TestCaseDao
from webapi.app.crud.test_case.TestCaseDirectory import SakuraTestcaseDirectoryDao
from webapi.app.crud.test_case.TestCaseOutParametersDao import SakuraTestCaseOutParametersDao
from webapi.app.crud.test_case.TestReport import TestReportDao
from webapi.app.crud.test_case.TestcaseDataDao import SakuraTestCaseDataDao
from webapi.app.enums.ConvertorEnum import CaseConvertorType
from webapi.app.excpetions.AuthException import AuthException
from webapi.app.handler.fatcory import SakuraResponse
from webapi.app.middleware.RedisManager import RedisHelper
from webapi.app.models.out_parameters import SakuraTestCaseOutParameters
from webapi.app.models.test_case import TestCase
from webapi.app.routers import Permission, get_session
from webapi.app.schema.constructor import ConstructorForm, ConstructorIndex
from webapi.app.schema.testcase_data import SakuraTestcaseDataForm
from webapi.app.schema.testcase_directory import SakuraTestcaseDirectoryForm, SakuraTestCaseDto
from webapi.app.schema.testcase_out_parameters import SakuraTestCaseOutParametersForm
from webapi.app.schema.testcase_schema import TestCaseForm, TestCaseInfo, TestCaseAssertsForm, TestCaseGeneratorForm

router = APIRouter(prefix="/testcase")
Author = TypeVar("Author", int, str)


@router.get("/list")
async def insert_testcase(directory_id: int = None, name: str = "", create_user: str = ''):
    data = await TestCaseDao.list_test_case(directory_id, name, create_user)
    return SakuraResponse.success(data)


@router.post("/insert")
async def insert_testcase(data: TestCaseForm, user_info=Depends(Permission())):
    try:
        record = await TestCaseDao.query_record(name=data.name, directory_id=data.directory_id)
        if record is not None:
            return SakuraResponse.failed("用例已存在")
        model = TestCase(**data.dict(), create_user=user_info['id'])
        model = await TestCaseDao.insert(model=model, log=True)
        return SakuraResponse.success(model.id)
    except Exception as e:
        return SakuraResponse.failed(e)


# V2版本船舰用例接口
@router.post("/create", summary="创建接口测试用例")
async def create_testcase(data: TestCaseInfo, user_info=Depends(Permission()), session=Depends(get_session)):
    async with session.begin():
        await TestCaseDao.insert_test_case(session, data, user_info['id'])
    return SakuraResponse.success()


@router.post("/update")
async def update_testcase(form: TestCaseForm, user_info=Depends(Permission())):
    try:
        data = await TestCaseDao.update_test_case(form, user_info['id'])
        result = await SakuraTestCaseOutParametersDao.update_many(form.id, form.out_parameters, user_info['id'])
        return SakuraResponse.success(dict(case_info=data, out_parameters=result))
    except Exception as e:
        return SakuraResponse.failed(e)


@router.delete("/delete", description="删除测试用例")
async def delete_testcase(id_list: List[int], user_info=Depends(Permission()), session=Depends(get_session)):
    try:
        # 删除case
        async with session.begin():
            await TestCaseDao.delete_records(session, user_info['id'], id_list)
            # 删除断言
            await TestCaseAssertsDao.delete_records(session, user_info['id'], id_list, column="case_id")
            # 删除测试用例
            await SakuraTestCaseDataDao.delete_record(session, user_info['id'], id_list, column="case_id")
            return SakuraResponse.success()
    except Exception as e:
        return SakuraResponse.failed(str(e))


@router.get("/query")
async def query_testcase(caseId: int, _=Depends(Permission())):
    try:
        data = await TestCaseDao.query_test_case(caseId)
        return SakuraResponse.success(SakuraResponse.dict_model_to_dict(data))
    except Exception as e:
        return SakuraResponse.failed(str(e))


@router.post("/asserts/insert")
async def insert_testcase_asserts(data: TestCaseAssertsForm, user_info=Depends(Permission())):
    try:
        new_assert = await TestCaseAssertsDao.insert_test_case_asserts(data, user_id=user_info['id'])
        return SakuraResponse.success(new_assert)
    except Exception as e:
        return SakuraResponse.failed(str(e))


@router.post("/asserts/update")
async def insert_testcase_asserts(data: TestCaseAssertsForm, user_info=Depends(Permission())):
    try:
        update = await TestCaseAssertsDao.update_test_case_asserts(data, user_id=user_info['id'])
        return SakuraResponse.success(update)
    except Exception as e:
        return SakuraResponse.failed(str(e))


@router.get("/asserts/delete")
async def insert_testcase_asserts(id: int, user_info=Depends(Permission())):
    await TestCaseAssertsDao.delete_test_case_asserts(id, user_id=user_info["id"])
    return SakuraResponse.success()


@router.post("/constructor/insert")
async def insert_constructor(data: ConstructorForm, user_info=Depends(Permission())):
    await ConstructorDao.insert_constructor(data, user_id=user_info["id"])
    return SakuraResponse.success()


@router.post("/constructor/update")
async def update_constructor(data: ConstructorForm, user_info=Depends(Permission())):
    await ConstructorDao.update_constructor(data, user_id=user_info["id"])
    return SakuraResponse.success()


@router.get("/constructor/delete")
async def update_constructor(id: int, user_info=Depends(Permission())):
    await ConstructorDao.delete_constructor(id, user_id=user_info["id"])
    return SakuraResponse.success()


@router.post("/constructor/order")
async def update_constructor(data: List[ConstructorIndex], user_info=Depends(Permission())):
    await ConstructorDao.update_constructor_index(data)
    return SakuraResponse.success()


@router.get("/constructor/tree")
async def get_constructor_tree(suffix: bool, name: str = "", user_info=Depends(Permission())):
    result = await ConstructorDao.get_constructor_tree(name, suffix)
    return SakuraResponse.success(result)


# 获取数据构造器树
@router.get("/constructor")
async def get_constructor_tree(id: int, user_info=Depends(Permission())):
    result = await ConstructorDao.get_constructor_data(id)
    return SakuraResponse.success(result)


# 获取所有数据构造器
@router.get("/constructor/list")
async def list_case_and_constructor(constructor_type: int, suffix: bool):
    ans = await ConstructorDao.get_case_and_constructor(constructor_type, suffix)
    return SakuraResponse.success(ans)


# 根据id查询具体报告内容
@router.get("/report")
async def query_report(id: int, user_info=Depends(Permission())):
    report, case_list, plan_name = await TestCaseDao.query(id)
    return SakuraResponse.success(dict(report=report, plan_name=plan_name, case_list=case_list))


# 获取构建历史列表
@router.get("/report/list")
async def list_report(page: int, size: int, start_time: str, end_time: str, executor: Author = None,
                      _=Depends(Permission())):
    start = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")
    report_list, total = await TestReportDao.list_report(page, size, start, end, executor)
    return SakuraResponse.success_with_size(data=report_list, total=total)


# 获取脑图数据
@router.get("/xmind")
async def get_xmind_data(case_id: int, user_info=Depends(Permission())):
    tree_data = await TestCaseDao.get_xmind_data(case_id)
    return SakuraResponse.success(tree_data)


# 获取case目录
@router.get("/directory")
async def get_testcase_directory(project_id: int, move: bool = False, user_info=Depends(Permission())):
    # 如果是move,则不需要禁用树
    tree_data, _ = await SakuraTestcaseDirectoryDao.get_directory_tree(project_id, move=move)
    return SakuraResponse.success(tree_data)


# 获取case目录+case
@router.get("/tree")
async def get_directory_and_case(project_id: int, user_info=Depends(Permission())):
    try:
        tree_data, cs_map = await SakuraTestcaseDirectoryDao.get_directory_tree(project_id,
                                                                                TestCaseDao.get_test_case_by_directory_id)
        return SakuraResponse.success(dict(tree=tree_data, case_map=cs_map))
    except Exception as e:
        return SakuraResponse.failed(str(e))


@router.get("/directory/query")
async def query_testcase_directory(directory_id: int, user_info=Depends(Permission())):
    try:
        data = await SakuraTestcaseDirectoryDao.query_directory(directory_id)
        await ProjectRoleDao.read_permission(data.project_id, user_info["id"], user_info["role"])
        return SakuraResponse.success(data)
    except AuthException:
        return SakuraResponse.forbidden()
    except Exception as e:
        return SakuraResponse.failed(str(e))


@router.post("/directory/insert")
async def insert_testcase_directory(form: SakuraTestcaseDirectoryForm, user_info=Depends(Permission())):
    try:
        await SakuraTestcaseDirectoryDao.insert_directory(form, user_info['id'])
        return SakuraResponse.success()
    except Exception as e:
        return SakuraResponse.failed(e)


@router.post("/directory/update")
async def insert_testcase_directory(form: SakuraTestcaseDirectoryForm, user_info=Depends(Permission())):
    try:
        await SakuraTestcaseDirectoryDao.update_directory(form, user_info["id"])
        return SakuraResponse.success()
    except Exception as e:
        return SakuraResponse.failed(str(e))


@router.get("/directory/delete")
async def insert_testcase_directory(id: int, user_info=Depends(Permission())):
    try:
        await SakuraTestcaseDirectoryDao.delete_directory(id, user_info['id'])
        return SakuraResponse.success()
    except Exception as e:
        return SakuraResponse.failed(str(e))


@router.post("/data/insert")
async def insert_testcase_data(form: SakuraTestcaseDataForm, user_info=Depends(Permission())):
    try:
        data = await SakuraTestCaseDataDao.insert_testcase_data(form, user_info['id'])
        return SakuraResponse.success(data)
    except Exception as e:
        return SakuraResponse.failed(str(e))


@router.post("/data/update")
async def update_testcase_data(form: SakuraTestcaseDataForm, user_info=Depends(Permission())):
    try:
        data = await SakuraTestCaseDataDao.update_testcase_data(form, user_info['id'])
        return SakuraResponse.success(data)
    except Exception as e:
        return SakuraResponse.failed(str(e))


@router.get("/data/delete")
async def delete_testcase_data(id: int, user_info=Depends(Permission())):
    try:
        await SakuraTestCaseDataDao.delete_testcase_data(id, user_info['id'])
        return SakuraResponse.success()
    except Exception as e:
        return SakuraResponse.failed(str(e))


@router.post("/move", description="移动case到其他目录")
async def move_testcase(form: SakuraTestCaseDto, user_info=Depends(Permission())):
    try:
        # 判断是否有移动case的权限
        await ProjectRoleDao.read_permission(form.project_id, user_info["id"], user_info["role"])
        await TestCaseDao.update_by_map(user_info["id"], TestCase.id.in_(form.id_list), directory_id=form.directory_id)
        return SakuraResponse.success()
    except AuthException:
        return SakuraResponse.forbidden()
    except Exception as e:
        return SakuraResponse.failed(str(e))


@router.post("/parameters/insert", summary="参数新增")
async def insert_testcase_out_parameters(form: SakuraTestCaseOutParametersForm, user_info=Depends(Permission())):
    query = await SakuraTestCaseOutParametersDao.query_record(name=form.name, case_id=form.case_id)
    if query is not None:
        return SakuraResponse.failed("参数名称已存在")
    data = SakuraTestCaseOutParameters(**form.dict(), user_id=user_info["id"])
    data = await SakuraTestCaseOutParametersDao.insert_record(data)
    return SakuraResponse.success(data)


@router.post("/parameters/update/batch", summary="批量更新出数据")
async def update_batch_testcast_out_parameters(case_id: int, form: List[SakuraTestCaseOutParametersForm],
                                               user_info=Depends(Permission())):
    result = await SakuraTestCaseOutParametersDao.update_many(case_id, form, user_info["id"])
    return SakuraResponse.success(result)


@router.post("/parameters/update", summary="参数更新")
async def update_testcase_out_parameters(form: SakuraTestCaseOutParametersForm, user_info=Depends(Permission())):
    data = await SakuraTestCaseOutParametersDao.update_record_by_id(user_info["id"], form)
    return SakuraResponse.success(data)


@router.get("/parameters/delete", summary="参数删除")
async def delete_testcase_out_parameters(id: int, user_info=Depends(Permission()), session=Depends(get_session)):
    await SakuraTestCaseOutParametersDao.delete_record_by_id(session, id, user_info['id'], log=False)
    return SakuraResponse.success()


@router.get("/record/start", summary="开始录制接口请求")
async def record_request(request: Request, regex: str, user_info=Depends(Permission())):
    await RedisHelper.set_address_record(user_info["id"], request.client.host, regex)
    return SakuraResponse.success(msg="开始录制,可以在浏览器/app上操作了")


@router.get("/record/stop", summary="停止录制接口请求")
async def record_requests(request: Request, _=Depends(Permission())):
    await RedisHelper.remove_address_record(request.client.host)
    return SakuraResponse.success(msg="停止成功,快去生成用例吧~")


@router.get("record/status", summary="获取录制接口请求状态")
async def record_requests(request: Request, _=Depends(Permission())):
    record = await RedisHelper.get_address_record(request.client.host)
    status = False
    regex = ''
    if record is not None:
        record_data = json.loads(record)
        regex = record_data.get('regex', '')
        status = True
    data = await RedisHelper.list_record_data(request.client.host)
    return SakuraResponse.success(dict(data=data, regex=regex, status=status))


@router.get("/record/remove", summary="删除录制接口")
async def remove_record(index: int, request: Request, _=Depends(Permission())):
    await RedisHelper.remove_record_data(request.client.host, index)
    return SakuraResponse.success()


@router.post("/generate", summary="生成用例")
async def generate_case(form: TestCaseGeneratorForm, user=Depends(Permission()), session=Depends(get_session)):
    if len(form.requests) == 0:
        return SakuraResponse.failed("无http请求,请检查参数")
    CaseGenerator.extract_field(form.requests)
    cs = CaseGenerator.generate_case(form.directory_id, form.name, form.requests[-1])
    constructors = CaseGenerator.generate_constructors(form.requests)
    info = TestCaseInfo(constructors=constructors, case=cs)
    async with session.begin():
        ans = await TestCaseDao.insert_test_case(session, info, user["id"])
        return SakuraResponse.success(ans)


@router.post("/import", summary="导入har或其他用例数据文件")
async def convert_case(import_type: CaseConvertorType, file: UploadFile = File(...), _=Depends(Permission())):
    convert, file_ext = get_convertor(import_type)
    if convert is None:
        return SakuraResponse.failed("不支持的导入数据")
    if not file.filename.endswith(f".{file_ext}"):
        return SakuraResponse.failed(f"请传入{file_ext}后缀文件")
    requests = convert(file.file)
    return SakuraResponse.success(requests)

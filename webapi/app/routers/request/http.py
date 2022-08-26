#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/1 11:12
# @Author  : 冉勇
# @Site    : 
# @File    : http.py
# @Software: PyCharm
# @desc    : 请求封装->后续更改httprunner
import asyncio
import json
import random
import uuid
from json import JSONDecodeError
from typing import List, Dict
from fastapi import Depends, APIRouter
from webapi.app.core.executor import Executor
from webapi.app.crud.test_case.TestcaseDataDao import SakuraTestCaseDataDao
from webapi.app.enums.CertEnum import CertType
from webapi.app.handler.fatcory import SakuraResponse
from webapi.app.middleware.AsyncHttpClient import AsyncRequest
from webapi.app.routers import Permission
from webapi.app.routers.request.http_schema import HttpRequestForm

router = APIRouter(prefix="/request")

CERT_URL = "http://mitm.it/cert"


@router.post("/http", summary="发起请求", tags=['Http'])
async def http_request(data: HttpRequestForm, _=Depends(Permission())):
    try:
        r = await AsyncRequest.client(data.url, data.body_type, headers=data.headers, body=data.body)
        response = await r.invoke(data.method)
        if response.get("status"):
            return SakuraResponse.success(response)
        return SakuraResponse.failed(response.get("msg"), data=response)
    except Exception as e:
        return SakuraResponse.failed(e)


@router.get("/cert", summary="证书", tags=['Http'])
async def http_request(cert: CertType):
    try:
        suffix = cert.get_suffix()
        client = AsyncRequest(CERT_URL + suffix)
        content = await client.download()
        shuffle = list(range(0, 9))
        random.shuffle(shuffle)
        filename = f"{''.join(map(lambda x: str(x), shuffle))}mitmproxy.{suffix}"
        with open(filename, 'wb') as f:
            f.write(content)
        return SakuraResponse.file(filename, f"mitmproxy.{suffix}")
    except Exception as e:
        return SakuraResponse.failed(e)


@router.get("/run", summary="发起请求", tags=['Http'])
async def execute_case(env: int, case_id: int, _=Depends(Permission)):
    try:
        executor = Executor()
        test_data = await SakuraTestCaseDataDao.list_testcase_data_by_env(env, case_id)
        ans = {}
        if not test_data:
            result, _ = await executor.run(env, case_id)
            ans["默认数据"] = result
        else:
            for data in test_data:
                params = json.loads(data.json_data)
                result, _ = await executor.run(env, case_id, request_params=params)
                ans[data.name] = result
        return SakuraResponse.success(ans)
    except JSONDecodeError:
        return SakuraResponse.failed("测试数据不为合法的JSON")
    except Exception as e:
        return SakuraResponse.failed(e)


@router.get("/retry", summary="根据测试数据重新运行测试用例", tags=['Http'])
async def re_run_case(env: int, case_id: int, data_id: int = 0, _=Depends(Permission())):
    try:
        executor = Executor()
        params = {}
        if data_id != 0:
            test_data = await SakuraTestCaseDataDao.query_record(id=data_id)
            params = json.loads(test_data.json_data)
        result, _ = await executor.run(env, case_id, request_params=params)
        return SakuraResponse.success(result)
    except JSONDecodeError:
        return SakuraResponse.failed("测试数据不为合法的JSON")


@router.post("/run/async", summary="异步发起请求", tags=['Http'])
async def execute_case(env: int, case_id: List[int]):
    data = {}
    await asyncio.gather(*(run_single(env, c, data) for c in case_id))
    return SakuraResponse.success()


@router.post("/run/sync", summary="同步发起请求", tags=['Http'])
async def execute_case(env: int, case_id: List[int]):
    data = {}
    task_id = uuid.uuid5(uuid.NAMESPACE_URL, "task")
    for c in case_id:
        executor = Executor()
        data[c] = await executor.run(env, c)
    return SakuraResponse.success(data)


@router.post("/run/multiple", summary="同、异发起请求", tags=['Http'])
async def execute_as_report(env: int, case_id: List[int], user_info=Depends(Permission())):
    report_id = await Executor.run_multiple(user_info['id'], env, case_id)
    return SakuraResponse.success(report_id)


async def run_single(env: int, case_id: int, data: Dict[int, tuple]):
    executor = Executor()
    data[case_id] = await executor.run(env, case_id)

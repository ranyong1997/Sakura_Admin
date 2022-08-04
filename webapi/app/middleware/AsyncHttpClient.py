#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/4 11:44
# @Author  : 冉勇
# @Site    : 
# @File    : AsyncHttpClient.py
# @Software: PyCharm
# @desc    : 异步 Http 客户端
import json
import time
import aiohttp
from aiohttp import FormData
from webapi.app.enums.RequestBodyEnum import BodyType
from webapi.app.middleware.oss import OssClient
from webapi.config import Config


class AsyncRequest(object):

    def __init__(self, url: str, timeout=15, **kwargs):
        self.url = url
        self.kwargs = kwargs
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.proxy = f"http://127.0.0.1:{Config.PROXY_PORT}" if Config.MOCK_ON else None

    def get_cookie(self, session):
        cookies = session.cookie_jar.filter_cookies(self.url)
        return {k: v.value for k, v in cookies.items()}

    def get_data(self, kwargs):
        return kwargs.get("data") if kwargs.get("json") is None else kwargs.get("json")

    async def invoke(self, method: str):
        start = time.time()
        async with aiohttp.ClientSession(cookies=aiohttp.CookieJar(unsafe=True)) as session:
            async with session.request(method, self.url, timeout=self.timeout, proxy=self.proxy, ssl=False,
                                       **self.kwargs) as resp:
                if resp.status != 200:
                    # 如果请求的状态码不为200,则给出提示:
                    return await self.collect(False, self.get_data(self.kwargs), resp.status, msg="http状态码不为200")
                cost = "%.0fms" % ((time.time() - start) * 1000)
                response, json_format = await AsyncRequest.get_resp(resp)
                cookie = self.get_cookie(session)
                return await self.collect(True, self.get_data(self.kwargs), resp.status, response, resp.headers,
                                          resp.request_info.headers, elapsed=cost,
                                          cookies=cookie, json_format=json_format)

    async def download(self):
        async with aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar(unsafe=True)) as session:
            async with session.request("GET", self.url, timeout=self.timeout, proxy=self.proxy, ssl=False,
                                       **self.kwargs) as resp:
                if resp.status != 200:
                    raise Exception("下载文件失败")
                return await resp.content.read()

    @staticmethod
    async def client(url: str, body_type: BodyType = BodyType.json, timeout=15, **kwargs):
        if not url.startswith(("http://", "https://")):
            raise Exception("请输入正确的url,记得带上http哦~")
        headers = kwargs.get("headers", {})
        if body_type == BodyType.json:
            if "Content-Type" not in headers:
                headers["Content-Type"] = "application/json; charset=UTF-8"
                # 新增json校验
            try:
                body = kwargs.get("body")
                if body:
                    body = json.loads(body)
            except Exception as e:
                raise Exception(f"JSON格式不正确:{str(e)}") from e
            r = AsyncRequest(url, headers=headers, timeout=timeout, json=body)
        elif body_type == BodyType.form:
            try:
                body = kwargs.get("body")
                form_data = None
                if body:
                    form_data = FormData()
                    # 因为是文本类型,所以需要反序列化
                    items = json.loads(body)
                    for item in items:
                        # 如果是文本类型,直接添加key-value
                        if item.get("type") == "TEXT":
                            form_data.add_field(item.get("key"), item.get("value", ""))
                        else:
                            client = OssClient.get_oss_client()
                            file_object = await client.get_file_object(item.get("value"))
                            form_data.add_field(item.get("key"), file_object)
                r = AsyncRequest(url, headers=headers, data=form_data, timeout=timeout)
            except Exception as e:
                raise Exception(f"解析form-data失败:{str(e)}") from e
        elif body_type == BodyType.x_form:
            body = kwargs.get("body", "{}")
            body = json.loads(body)
            r = AsyncRequest(url, headers=headers, data=body, timeout=timeout)
        else:
            # 暂不支持其他类型
            r = AsyncRequest(url, headers=headers, timeout=timeout, data=kwargs.get("body"))
        return r

    @staticmethod
    async def get_resp(resp):
        try:
            data = await resp.json(encoding='utf-8')
            # 说明是json格式
            return json.dumps(data, ensure_ascii=False, indent=4), True
        except Exception:
            data = await resp.text()
            # 说明不是json格式
            return data, False

    @staticmethod
    def get_request_data(body):
        request_body = body
        if isinstance(body, bytes):
            request_body = request_body.decode()
        if isinstance(body, FormData):
            request_body = str(body)
        if isinstance(request_body, str) or request_body is None:
            return request_body
        return json.dumps(request_body, ensure_ascii=False, indent=4)

    @staticmethod
    async def collect(status, request_data, status_code=200, response=None, response_headers=None, request_headers=None,
                      cookies=None, elapsed=None, msg="success", **kwargs):
        """
        收集http返回数据
        :param status: 请求状态
        :param request_data: 请求入参
        :param status_code: 状态码
        :param response: 响应
        :param response_headers: 返回headers
        :param request_headers: 请求headers
        :param cookies: cookies
        :param elapsed: 耗时
        :param msg: 报错信息
        :param kwargs:
        :return:
        """
        request_headers = json.dumps(dict(request_headers.items()) if request_headers is not None else {},
                                     ensure_ascii=False)
        response_headers = json.dumps(dict(response_headers.items()) if response_headers is not None else {},
                                      ensure_ascii=False)
        cookies = dict(cookies.items()) if cookies is not None else {}
        cookies = json.dumps(cookies, ensure_ascii=False)
        return {
            "status": status, "response": response, "status_code": status_code,
            "request_data": AsyncRequest.get_request_data(request_data),
            "response_headers": response_headers, "request_headers": request_headers,
            "msg": msg,
            "cost": elapsed,
            "cookies": cookies,
            **kwargs
        }

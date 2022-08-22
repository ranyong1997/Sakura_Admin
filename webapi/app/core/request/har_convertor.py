#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/12 14:28
# @Author  : 冉勇
# @Site    : 
# @File    : har_convertor.py
# @Software: PyCharm
# @desc    : har转换器
import json
import re
from typing import List
from webapi.app.core.request.convertor import Convertor
from webapi.app.excpetions.convert.ConvertException import HarConvertException
from webapi.app.schema.request import RequestInfo


class HarConvertor(Convertor):
    @staticmethod
    def convert_from_file(file, regex: str = None) -> List[RequestInfo]:
        with open(file, 'r', encoding="utf-8") as f:
            return HarConvertor._convert(f, regex)

    @staticmethod
    def _convert(f, regex: str = None):
        try:
            flag = None
            if regex is not None:
                flag = re.compile(regex)
            # 加载har请求数据
            data = json.load(f)
            ans = []
            entries = data.get("log", {}).get("entries")
            if not entries:
                raise HarConvertException("entries数据为空")
            for entry in entries:
                # 如果是fetch或xhr接口,说明是http请求
                if entry.get("_resourceType").lower() in ("fetch", "xhr"):
                    request_data = entry.get("request")
                    response_data = entry.get("response")
                    url = request_data.get("url")
                    if flag is not None and not re.findall(flag, url):
                        # 由于不符合预期的url,所以过滤掉
                        continue
                    info = RequestInfo(url=url, response_data=entry.get("response"),
                                       body=HarConvertor.get_body(request_data),
                                       status_code=response_data.get("status"),
                                       request_method=request_data.get("method"),
                                       request_headers=HarConvertor.get_kv(request_data),
                                       response_headers=HarConvertor.get_kv(response_data),
                                       cookies=HarConvertor.get_kv(response_data, "cookies"),
                                       request_cookies=HarConvertor.get_kv(request_data, "cookies"),
                                       response_content=response_data.get("content", {}).get("text"))
                    ans.append(info)
            return ans
        except HarConvertException as e:
            raise HarConvertException(f"har文件转换异常:{str(e)}") from e
        except Exception as e:
            raise HarConvertException(f"har文件转换失败:{str(e)}") from e

    @staticmethod
    def convert(file_data, regex: str = None) -> List[RequestInfo]:
        return HarConvertor._convert(file_data, regex)

    @staticmethod
    def get_kv(request_data: dict, key: str = "headers") -> dict:
        """
        通过response/request获取header信息
        :param request_data:
        :param key:
        :return:
        """
        headers = request_data.get(key)
        result = {}
        for h in headers:
            result[h.get("name")] = h.get("value")
        return result

    @staticmethod
    def get_body(request_data: dict):
        data = request_data.get("postData", {})
        return data.get("text", "")


if __name__ == '__main__':
    requests = HarConvertor.convert_from_file("./sakura.fun.har")
    print(requests)

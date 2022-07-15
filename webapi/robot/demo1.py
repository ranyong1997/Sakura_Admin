#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/15 10:51
# @Author  : 冉勇
# @Site    : 
# @File    : demo1.py
# @Software: PyCharm
# @desc    :
from urllib import request
import json

def get_tenant_access_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
    headers = {
        "Content-Type": "application/json"
    }
    req_body = {
        "app_id": "cli_a2456f89cbff1013",
        "app_secret": "0VtOpLW93Q2OMsl3GTxSgd7PzYTp8U0L"
    }

    data = bytes(json.dumps(req_body), encoding='utf8')
    req = request.Request(url=url, data=data, headers=headers, method='POST')
    try:
        response = request.urlopen(req)
    except Exception as e:
        print(e.read().decode())
        return ""

    rsp_body = response.read().decode('utf-8')
    rsp_dict = json.loads(rsp_body)
    code = rsp_dict.get("code", -1)
    if code != 0:
        print("get tenant_access_token error, code =", code)
        return ""
    return rsp_dict.get("tenant_access_token", "")


def send_message(token, open_id, text):
    url = "https://open.feishu.cn/open-apis/message/v4/send/"
    url = "https://open.feishu.cn/open-apis/contact/v3/users/"

    access_token = get_tenant_access_token()
    print(access_token)

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + access_token
    }
    req_body = {
        "open_id": "cli_a2456f89cbff1013",
        "msg_type": "text",
        "content": {
            "text": text
        }
    }

    # data = bytes(json.dumps(req_body), encoding='utf8')
    req = request.Request(url=url + open_id, headers=headers, method='GET')
    try:
        response = request.urlopen(req)
    except Exception as e:
        print(e)
        return

    rsp_body = response.read().decode('utf-8')
    rsp_dict = json.loads(rsp_body)
    print(rsp_dict)
    code = ''
    code = rsp_dict.get('data').get('user').get('name')
    print(code)
    if code == '':
        print("send message error, code = ", code, ", msg =", rsp_dict.get("msg", ""))


if __name__ == '__main__':
    open_id = "你好"
    open_id = ""
    send_message("你好")
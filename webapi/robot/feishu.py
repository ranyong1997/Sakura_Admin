#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/9/8 11:39
# @Author  : 冉勇
# @Site    : 
# @File    : feishu.py
# @Software: PyCharm
# @desc    :
import json
import requests

app_id = 'cli_a2456f89cbff1013'
app_secret = '0VtOpLW93Q2OMsl3GTxSgd7PzYTp8U0L'
receive_id = 'bebgg6ag'


# receive_id  =  open_id \ user_id \ union_id \ email \ chat_id
# https://open.feishu.cn/document/home/user-identity-introduction/how-to-get

# content & msg_type  =  text \ post \ image \ interactive
# https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/im-v1/message/create_json#c9e08671

# Authorization = access token
# https://open.feishu.cn/document/ukTMukTMukTM/uMTNz4yM1MjLzUzM#top_anchor


def get_tenant_access_token():
    """
    获取 tenant_access_token（企业自建应用）
    :return:
    """
    url = "	https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {'Content-Type': 'application/json'}
    params = {"app_id": app_id, "app_secret": app_secret}
    response = requests.request("POST", url, params=params, headers=headers)
    token = json.loads(response.content)
    return token['tenant_access_token']


def get_chat_id():
    """
    获取chat_id
    :return:
    """
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    headers = {
        'Authorization': 'Bearer ' + get_tenant_access_token(),
        'Content-Type': 'application/json'}
    params = {"receive_id_type": "user_id"}
    req = {
        "receive_id": receive_id,
        "content": json.dumps(text('get_chat_id')),
        "msg_type": "text", }
    response = requests.request("POST", url, params=params, headers=headers, data=json.dumps(req))
    chat = json.loads(response.content)
    return chat['data']['chat_id']


def get_chat_history():
    """
    获取会话（包括单聊、群组）的历史消息（聊天记录）
    :return:
    """
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    headers = {'Authorization': f'Bearer {get_tenant_access_token()}'}
    params = {"container_id_type": "chat", "container_id": get_chat_id()}
    response = requests.request("GET", url, params=params, headers=headers)
    return response.content


def text(t):
    """
    发送纯文本
    :param t:
    :return:
    """
    return {"text": f"{t}"}


# 富文本
def post():
    """
    发送富文本
    :return:
    """
    post = {
        "zh_cn": {
            "title": "我是一个标题",
            "content": [
                [{
                    "tag": "text",
                    "text": "第一行 :"
                },
                    {
                        "tag": "a",
                        "href": "http://www.feishu.cn",
                        "text": "超链接"
                    }
                ],
                [{
                    "tag": "img",
                    "image_key": "img_7ea74629-9191-4176-998c-2e603c9c5e8g"
                }]
            ]
        }
    }
    return post


def update_image():
    pass


def image():
    """
    发送图片
    :return:
    """
    # Get image_key
    # https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/image/create
    return {"image_key": "img_7ea74629-9191-4176-998c-2e603c9c5e8g"}


def interactive(title, link, text):
    """
    发送消息卡片
    :param title:
    :param link:
    :param text:
    :return:
    """
    interactive = {
        "elements": [
            {
                "tag": "markdown",
                "content": f"**[{title}]({link})**\n --------------\n{text}"
            }
        ]
    }
    return interactive


# 分享群名片
def share_chat():
    """
    分享名片
    :return:
    """
    return {"chat_id": "oc_0dd200d32fda15216d2c2ef1ddb32f76"}


def share_user():
    """
    分享个人名片
    :return:
    """
    return {"user_id": "ou_0dd200d32fda15216d2c2ef1ddb32f76"}


def file():
    """
    分享文件
    :return:
    """
    # 通过上传文件获取文件key
    # https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/file/create
    return {"file_key": "75235e0c-4f92-430a-a99b-8446610223cg"}


def audio():
    """
    分享语音
    :return:
    """
    # 通过上传文件获取文件key
    # https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/file/create
    return {"file_key": "75235e0c-4f92-430a-a99b-8446610223cg"}


def audio():
    """
    分享视频
    :return:
    """
    # 通过上传文件获取文件 file_key
    # https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/file/create
    # 通过上传图片获取视频封面 image_key
    # https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/reference/im-v1/image/create
    return {"file_key": "75235e0c-4f92-430a-a99b-8446610223cg", "image_key": "img_xxxxxx"}


def send(title, link, text):
    req = {"receive_id": receive_id,
           "content": json.dumps(interactive(title, link, text)),
           "msg_type": "interactive", }
    response = requests.request("POST", "https://open.feishu.cn/open-apis/im/v1/messages",
                                params={"receive_id_type": "user_id"},
                                headers={'Authorization': 'Bearer ' + get_tenant_access_token(),
                                         'Content-Type': 'application/json'},
                                data=json.dumps(req))
    return response.content


def send_message(text):
    """
    向某人指定发送纯文本
    :param text:
    :return:
    """
    url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=user_id"
    text = {"text": text}
    data = {"content": "{}".format(json.dumps(text)), "msg_type": "text", "receive_id": receive_id}
    payload = json.dumps(data)
    # print("a->>", json.dumps(data))
    # payload = json.dumps({
    #     "content": "{\"text\":\"dddf\"}",
    #     "msg_type": "text",
    #     "receive_id": receive_id
    # })
    # print("b->>", payload)
    headers = {'Authorization': 'Bearer ' + get_tenant_access_token(),
               'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    return response.text


def at_person_send_message(text):
    """
    @某人指定发送纯文本
    :param text:
    :return:
    """
    url = "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=user_id"
    text1 = {"text": "<at user_id={}".format(receive_id)+">"}
    data = {"content": "{}".format(json.dumps(text1))+">"+text+"</at>"+text+'',
            "msg_type": "text",
            "receive_id": receive_id}
    payload = json.dumps(data)
    print("b->>", payload)
    headers = {'Authorization': 'Bearer ' + get_tenant_access_token(),
               'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    return response.text

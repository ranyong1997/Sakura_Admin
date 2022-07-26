#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/7/14 15:47
# @Author  : 冉勇
# @Site    : 
# @File    : demo.py
# @Software: PyCharm
# @desc    :
import json
import requests
import time
import hmac
import hashlib
import base64
from datetime import datetime


class FeiShuRobot:

    def __init__(self, robot_id, secret) -> None:
        self.robot_id = robot_id
        self.secret = secret

    def get_sign(self):
        # 拼接timestamp和secret
        timestamp = int(round(time.time() * 1000))
        string_to_sign = '{}\n{}'.format(timestamp, self.secret)
        hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()

        # 对结果进行base64处理
        sign = base64.b64encode(hmac_code).decode('utf-8')
        print("---->", timestamp, sign)
        return str(timestamp), str(sign)

    def get_token(self):
        """获取应用token，需要用app_id和app_secret，主要是上传图片需要用到token"""
        url = r"https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
        headers = {"Content-Type": "text/plain"}
        Body = {
            "app_id": self.robot_id,
            "app_secret": self.secret
        }
        r = requests.post(url, headers=headers, json=Body)
        return json.loads(r.text['tenant_access_token'])

    def upload_image(self, image_path):
        """上传图片"""
        with open(image_path, 'rb') as f:
            image = f.read()
        resp = requests.post(url='https://open.feishu.cn/open-apis/image/v4/put/',
                             headers={'Authorization': "Bearer " + self.get_token()},
                             files={"image": image},
                             data={"images_type": "message"}, stream=True)
        resp.raise_for_status()
        content = resp.json()
        if content.get("code") == 0:
            return content['data']['image_key']
        else:
            return Exception(f'Call Api Error, errorCode is {content["code"]}')

    def send_text(self, text):
        """发送普通信息"""
        try:
            url = f"https://open.feishu.cn/open-apis/bot/v2/hook/{self.robot_id}"
            headers = {"Content-Type": "text/plain"}
            timestamp, sign = self.get_sign()
            data = {
                "timestamp": timestamp,
                "sign": sign,
                "msg_type": "text",
                "content": {
                    "text": text
                }
            }
            r = requests.post(url, headers=headers, json=data)
            print("发送飞书成功")
            return r.text
        except Exception as e:
            print("发送飞书失败:", e)

    def send_md(self):
        """发送普通信息"""
        try:
            url = f"https://open.feishu.cn/open-apis/bot/v2/hook/{self.robot_id}"
            headers = {"Content-Type": "text/plain"}
            data = {"msg_type": "interactive", "card": {"config": {"wide_screen_mode": True}},
                    "header": {"title": {"tag": "plain_text", "content": "注意咯！！注意咯！！！"}, "template": "red"},
                    "elements": [{"tag": "div", "text": {"content": self, "tag": "lark_md"}}]}
            r = requests.post(url, headers=headers, json=data)
            print("发送飞书成功")
            return r.text
        except Exception as e:
            print("发送飞书失败:", e)

    def send_img(self, path, bot):
        """发送图片信息"""
        url = f"https://open.feishu.cn/open-apis/bot/v2/hook/{bot}"
        headers = {"Content-Type": "text/plain"}
        data = {"msg_type": "image", "content": {"image_key": self.upload_image(path)}}
        r = requests.post(url, headers=headers, json=data)
        return r.text

    def send_markdown(self, text):
        """发送富文本消息"""
        url = "https://open.feishu.cn/open-apis/bot/v2/hook/fce32975-4d2f-49ab-b7a0-72921b173bb9"
        headers = {"Content-Type": "text/plain"}
        data = {"msg_type": "interactive", "card": {"config": {"wide_screen_mode": True}},
                "header": {"title": {"tag": "plain_text", "content": "注意咯！！注意咯！！！"}, "template": "red"},
                "elements": [{"tag": "div", "text": {"content": text, "tag": "lark_md"}}]}
        r = requests.post(url, headers=headers, json=data)
        return r.text

    def send_card(self):
        """发送卡片信息"""
        try:
            url = "https://open.feishu.cn/open-apis/bot/v2/hook/fce32975-4d2f-49ab-b7a0-72921b173bb9"
            headers = {"Content-Type": "text/plain"}
            data = {"msg_type": "interactive", "card": self}
            r = requests.post(url, headers=headers, json=data)
            return r.text
        except Exception as e:
            print("发送飞书失败:", e)


if __name__ == '__main__':
    robot_id = 'fce32975-4d2f-49ab-b7a0-72921b173bb9'
    secret = f'https://open.feishu.cn/open-apis/bot/v2/hook/{robot_id}'
    feishu = FeiShuRobot(robot_id, secret)
    # feishu.send_text("你好")
# 飞书模板
"""
AUTOTEST_LARK_MESSAGE_TEMPLATE = {
    "msg_type": "interactive",
    "card": {
        "config": {
            "wide_screen_mode": True
        },
        "elements": [
            {
                "fields": [
                    {
                        "is_short": False,
                        "text": {
                            "content": "**🗳 任务**: ${job_name} ",
                            "tag": "lark_md"
                        }
                    },
                    {
                        "is_short": False,
                        "text": {
                            "content": "**📍类型**: ${job_type}",
                            "tag": "lark_md"
                        }
                    },
                    {
                        "is_short": False,
                        "text": {
                            "content": "**💃 执行人**: ${execute_by}",
                            "tag": "lark_md"
                        }
                    },
                    {
                        "is_short": False,
                        "text": {
                            "content": "**🍕 测试通过率**: ${pass_rate}",
                            "tag": "lark_md"
                        }
                    }, {
                        "is_short": False,
                        "text": {
                            "content": "**🍔 执行通过率(忽略跳过)**: ${pass_rate_ignore_skipped}",
                            "tag": "lark_md"
                        }
                    },
                    {
                        "is_short": False,
                        "text": {
                            "content": "**🍤 执行用例数**: ${cases}",
                            "tag": "lark_md"
                        }
                    },
                    {
                        "is_short": False,
                        "text": {
                            "content": "**🌭 执行步骤数**: ${steps}",
                            "tag": "lark_md"
                        }
                    },
                    {
                        "is_short": False,
                        "text": {
                            "content": "**🍜 通过/失败/错误/跳过**: ${successes}/${failures}/${errors}/${skipped}",
                            "tag": "lark_md"
                        }
                    },
                    {
                        "is_short": False,
                        "text": {
                            "content": "**🍣 执行线程数**: ${threads}",
                            "tag": "lark_md"
                        }
                    },
                    {
                        "is_short": False,
                        "text": {
                            "content": "**⏰ 执行耗时**: ${duration}(s)",
                            "tag": "lark_md"
                        }
                    },
                    {
                        "is_short": False,
                        "text": {
                            "content": "**⏰ 开始时间**: ${start_at}",
                            "tag": "lark_md"
                        }
                    },
                    {
                        "is_short": False,
                        "text": {
                            "content": "**🔥 异常信息**: ${exception}",
                            "tag": "lark_md"
                        }
                    },
                ],
                "tag": "div"
            },
            {
                "actions": [
                    {
                        "tag": "button",
                        "text": {
                            "content": "查看报告",
                            "tag": "plain_text"
                        },
                        "type": "primary",
                        "url": "${report_address}"
                    }
                ],
                "tag": "action"
            }
        ],
        "header": {
            "template": "purple",
            "title": {
                "content": "📮 ARUN自动化测试报告",
                "tag": "plain_text"
            }
        }
    }}
"""

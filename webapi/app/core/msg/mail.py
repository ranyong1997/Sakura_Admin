#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/4 17:06
# @Author  : 冉勇
# @Site    : 
# @File    : mail.py
# @Software: PyCharm
# @desc    : 邮件通知
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import make_msgid
from awaits.awaitable import awaitable
from jinja2.environment import Template
from webapi.app.core.configuration import SystemConfiguration
from webapi.app.core.msg.notification import Notification
from webapi.config import Config


class Email(Notification):
    @staticmethod
    @awaitable
    def send_msg(subject, content, attachment=None, *receiver):
        configuration = SystemConfiguration.get_config()
        data = configuration.get("email")
        sender = data.get("sender")
        message = MIMEText(content, "html", "utf-8")
        message['From'] = sender
        # 抄送自己一份
        message['Subject'] = Header(subject, 'utf-8')
        message['Message-ID'] = make_msgid()

        try:
            smtp = smtplib.SMTP()
            smtp.connect(data.get("host"))
            smtp.set_debuglevel(1)
            smtp.login(sender, data.get("password"))
            smtp.sendmail(sender, [sender, *receiver], message.as_string())
        except Exception as e:
            raise Exception(f"发送测试报告邮件失败:{str(e)}") from e

    @staticmethod
    def render_html(filepath=Config.REPORT_PATH, **kwargs):
        with open(filepath, encoding="utf-8") as f:
            html = Template(f.read())
            # 渲染HTML模板
            return html.render(**kwargs)

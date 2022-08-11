#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/8/1 11:24
# @Author  : 冉勇
# @Site    : 
# @File    : executor.py
# @Software: PyCharm
# @desc    : 执行者
import asyncio
import json
import re
import time
from collections import defaultdict
from datetime import datetime
from typing import List, Any
from webapi.app.core.constructor.case_constructor import TestcaseConstructor
from webapi.app.core.constructor.http_constructor import HttpConstructor
from webapi.app.core.constructor.python_constructor import PythonConstructor
from webapi.app.core.constructor.redis_constructor import RedisConstructor
from webapi.app.core.constructor.sql_constructor import SqlConstructor
from webapi.app.core.msg.dingtalk import DingTalk
from webapi.app.core.msg.mail import Email
from webapi.app.core.paramters import ParameterParser
from webapi.app.core.ws_connection_manager import ws_manage
from webapi.app.crud.auth.UserDao import UserDao
from webapi.app.crud.config.AddressDao import SakuraGatewayDao
from webapi.app.crud.config.EnvironmentDao import EnvironmentDao
from webapi.app.crud.config.GConfigDao import GConfigDao
from webapi.app.crud.project.ProjectDao import ProjectDao
from webapi.app.crud.test_case.TestCaseAssertsDao import TestCaseAssertsDao
from webapi.app.crud.test_case.TestCaseDao import TestCaseDao
from webapi.app.crud.test_case.TestCaseOutParametersDao import SakuraTestCaseOutParametersDao
from webapi.app.crud.test_case.TestPlan import SakuraTestPlanDao
from webapi.app.crud.test_case.TestReport import TestReportDao
from webapi.app.crud.test_case.TestResult import TestResultDao
from webapi.app.crud.test_case.TestcaseDataDao import SakuraTestCaseDataDao
from webapi.app.enums.ConstructorEnum import ConstructorType
from webapi.app.enums.GconfigEnum import GConfigParserEnum, GConfigType
from webapi.app.enums.NoticeEnum import NoticeType
from webapi.app.enums.RequestBodyEnum import BodyType
from webapi.app.middleware.AsyncHttpClient import AsyncRequest
from webapi.app.models.constructor import Constructor
from webapi.app.models.out_parameters import SakuraTestCaseOutParameters
from webapi.app.models.project import Project
from webapi.app.models.test_case import TestCase
from webapi.app.models.test_plan import SakuraTestPlan
from webapi.app.models.testcase_asserts import TestCaseAsserts
from webapi.app.utils.case_logger import CaseLog
from webapi.app.utils.decorator import case_log, lock
from webapi.app.utils.gconfig_parser import StringGConfigParser, JSONGConfigParser, YamlGConfigParser
from webapi.app.utils.json_compare import JsonCompare
from webapi.app.utils.logger import Log
from webapi.config import Config


class Executor(object, Exception):
    log = Log("Executor")
    el_exp = r"\$\{(.+?)\}"
    pattern = re.compile(el_exp)
    # 需要替换全局变量你那个的字段
    fields = ['body', 'url', 'request_headers']

    def __init__(self, log: CaseLog = None):
        if log is None:
            self._logger = CaseLog()
            self._main = True
        else:
            self._logger = log
            self._main = False

    @property
    def logger(self):
        return self._logger

    @staticmethod
    def get_constructor_type(c: Constructor):
        if c.type == ConstructorType.testcase
            return TestcaseConstructor
        if c.type == ConstructorType.sql:
            return SqlConstructor
        if c.type == ConstructorType.redis:
            return RedisConstructor
        if c.type == ConstructorType.py_script:
            return PythonConstructor
        if c.type == ConstructorType.http:
            return HttpConstructor
        return None

    def append(self, content, end=False):
        self.logger.append(content, end)

    @case_log
    async def parse_gconfig(self, data, type_, env, *fields):
        """
        解析全局变量
        :param data:
        :param type_:
        :param env:
        :param fields:
        :return:
        """
        for f in fields:
            await self.parse_gconfig(data, f, GConfigType.text(type_), env)

    @case_log
    def get_parser(self, key_type):
        """
        获取变量解析器
        :param key_type:
        :return:
        """
        if key_type == GConfigParserEnum.string:
            return StringGConfigParser.parse
        if key_type == GConfigParserEnum.json:
            return StringGConfigParser.parse
        if key_type == GConfigParserEnum.yaml:
            return StringGConfigParser.parse
        raise Executor(f"全局变量类型:{key_type}不合法,请检查!")

    async def parse_field(self, data, field, name, env):
        """
        解析字段
        :param data:
        :param field:
        :param name:
        :param env:
        :return:
        """
        try:
            self.append("获取{}:[{}]字段:[{}]中的el表达式".format(name, data, field))
            field_origin = getattr(data, field)
            variables = self.get_el_expression(field_origin)
            for v in variables:
                key = v.split(".")[0]
                cf = await GConfigDao.async_get_gconfig_by_key(key, env)
                if cf is not None:
                    # 解析变量
                    parse = self.get_parser(cf.key_type)
                    new_value = parse(cf.value, v)
                    new_field = field_origin.replace("${%s}" % v, new_value)
                    setattr(data, field, new_field)
                    self.append("替换全局变量成功, 字段: [{}]:\n\n[{}] -> [{}]\n".format(field, "${%s}" % v, new_value))
                    field_origin = new_field
            self.append(f"获取{name}字段:[{field}]中的el表达式", True)
        except Exception as e:
            Executor.log.error(f"查询全局变量失败:{str(e)}")
            raise Executor(f"查询全局变量失败:{str(e)}")

    def replace_params(self, field_name, field_origin, params: dict):
        new_data = {}
        if not isinstance(field_origin, str):
            return new_data
        variables = self.get_el_expression(field_origin)
        for v in variables:
            key = v.split(".")
            if not params.get(key[0])
                continue
            result = params
            for branch in key:
                if isinstance(result, str):
                    # 说明需要反序列化
                    try:
                        result = json.loads(result)
                    except Exception as e:
                        self.append(f"反序列化失败,结果:{result}\n Error:{str(e)}")
                        break
                if branch.isdigit():
                    # 说明路径是数组
                    result = result[int(branch)]
                else:
                    result = result.get(branch)
                if result is None:
                    raise Exception(f"变量路径:{v}不存在,请检查JSON或路径")
            if field_name != "request_headers" and not isinstance(result, str):
                new_value = json.dumps(result, ensure_ascii=False)
            else:
                new_value = result
                if new_value is None:
                    self.append("替换变量失败,找不到对应的数据")
                    continue
            new_data["${%s}" % v] = new_value
        return new_data

    async def parse_params(self, data: TestCase, params: dict):
        self.append("正在替换变量")
        try:
            for c in data.__table__.columns:
                field_origin = getattr(data, c.name)
                replace_kv = self.replace_params(c.name, field_origin, params)
                for k, v in replace_kv.items():
                    new_field = field_origin.replace(k, v)
                    setattr(data, c.name, new_field)
                    self.append(f"替换流程变量成功,字段:[{c.name}]:\n\n[{k}] -> [{v}]\n")
        except Exception as e:
            Executor.log.error(f"替换变量失败:{str(e)}")
            raise Exception(f"替换变量失败:{str(e)}") from e

    @case_log
    async def get_constructor(self, case_id):
        """
        获取构造函数
        :param case_id:
        :return:
        """
        return await TestCaseDao.async_select_constructor(case_id)

    async def execute_constructors(self, env: int, path, case_info, params, req_params, constructors: List[Constructor],
                                   asserts, suffix=False):
        """
        开始构造数据
        :param env:
        :param path:
        :param case_info:
        :param params:
        :param req_params:
        :param constructors:
        :param asserts:
        :param suffix:
        :return:
        """
        if not constructors:
            self.append("前置条件为空,跳出该环节")
        current = 0
        for c in constructors:
            if c.suffix == suffix:
                await self.execute_constructors(env, current, path, params, req_params, c)
                self.replace_params(params, case_info, constructors, asserts)
                current += 1

    async def execute_constructor(self, env, index, path, params, req_params, constructor: Constructor):
        """
        执行构造函数
        :param env:
        :param index:
        :param path:
        :param params:
        :param req_params:
        :param constructor:
        :return:
        """
        if not constructor.enable:
            self.append(f"当前路径:{path},构造方法:{constructor.name}已关闭,不继续执行")
            return False
        construct = Executor.get_constructor_type(constructor)
        if construct is None:
            self.append(f"构造方法类型:{constructor.type}不合法,请检查")
            return
        await construct.run(self, env, index, path, params, req_params, constructor, executor_class=Executor)

    def add_header(self, case_info, headers):
        """
        添加请求头
        :param case_info:
        :param headers:
        :return:
        """
        if case_info.body_type == BodyType.none:
            return
        if case_info.body_type == BodyType.json and "Content-Type" not in headers:
            headers['Content-Type'] = "application/json; charset=utf-8"

    @case_log
    def extract_out_parameters(self, response_info, data: List[SakuraTestCaseOutParameters]):
        """
        提取参数数据
        :param response_info:
        :param data:
        :return:
        """
        result = {}
        for d in data:
            p = ParameterParser(d.source)
            result[d.name] = p(response_info, d.expression, d.match_index)
        return result

    async def run(self, env: int, case_id: int, params_pool: dict = None, request_params: dict = None, path="主case"):
        """
        开始执行用例
        :param env:
        :param case_id:
        :param params_pool:
        :param request_params:
        :param path:
        :return:
        """
        response_info = {}
        # 初始化case全局变量,只存在于case生命周期
        case_params = params_pool
        if case_params is None:
            case_params = {}

        req_params = request_params
        if req_params is None:
            req_params = {}

        try:
            case_info, err = await TestCaseDao.async_query_test_case(case_id)
            if err:
                return response_info, err
            response_info['case_id'] = case_info.id
            response_info['case_name'] = case_info.name
            method = case_info.request_method.upper()
            response_info["request_method"] = method

            # 步骤1:替换全局变量
            await self.parse_gconfig(case_info, GConfigType.case, env, *Executor.fields)
            self.append("解析全局变量", True)

            # 步骤2:获取构造数据
            constructors = await self.get_constructor(case_id)

            # 步骤3:解析前后置条件的全局变量
            for c in constructors:
                await self.parse_gconfig(c, GConfigType.constructor, env, "constructor_json")

            # 步骤4:获取断言
            asserts = await TestCaseAssertsDao.async_list_test_case_asserts(case_id)

            # 获取出参信息
            out_parameters = await SakuraTestCaseOutParametersDao.list_record(case_id=case_id)

            for ast in asserts:
                await self.parse_gconfig(ast, GConfigType.asserts, env, "expected", "actually")

            # 步骤5:替换参数
            self.replace_args(req_params, case_info, constructors, asserts)

            # 步骤6:执行前置条件
            await self.execute_constructors(env, path, case_info, case_params, constructors, asserts)

            # 步骤7:批量改写主方法参数
            await self.parse_params(case_info, case_params)

            if case_info.request_headers and case_info.request_headers != "":
                headers = json.loads(case_info.request_headers)
            else:
                headers = {}

            body = case_info.body if case_info.body != "" else None

            # 步骤8:替换请求参数
            body = self.replace_params(request_params, body, case_info.body_type)

            # 步骤9:替换base_path
            if case_info.base_path:
                base_path = await SakuraGatewayDao.query_gateway(env, case_info.base_path)
                case_info.url = f"{base_path}{case_info.url}"

            response_info["url"] = case_info.url

            # 步骤10: 完成http请求
            request_obj = await AsyncRequest.client(url=case_info.url, body_type=case_info.body_type, headers=headers,
                                                    body=body)
            res = await request_obj.invoke(method)
            self.append(f"http请求过程\n\n Request Method:{case_info.request_method}\n\n"
                        f"Request Headers:\n{headers}\n\nUrl:{case_info.url}"
                        f"\n\nBody:\n{body}\n\nResponse:\n{res.get('response', '未获取到返回值')}")
            response_info.update(res)

            # 步骤11: 提取出参
            out_dict = self.extract_out_parameters(response_info, out_parameters)

            # 步骤12: 替换主变量
            req_params.update(out_dict)

            # 步骤13: 写入response
            req_params["response"] = res.get("response", "")
            self.replace_params(req_params, asserts)
            self.replace_constructors(req_params, constructors)

            # 步骤14: 执行后置条件
            await self.execute_constructors(env, path, case_info, case_params, req_params, constructors, asserts, True)

            # 步骤15: 断言
            asserts, ok = self.my_assert(asserts, response_info.get("json_format"))
            response_info['status'] = ok
            response_info['asserts'] = asserts
            # 日志输出,如果不是主用例则不记录
            if self._main:
                response_info['logs'] = self.logger.join()
            return response_info, None
        except Exception as e:
            Executor.log.exception("执行用例失败:\n")
            self.append(f"执行用例失败,{str(e)}")
            if self._main:
                response_info['logs'] = self.logger.join()
            return response_info, f"执行用例失败:{str(e)}"

    @staticmethod
    def get_dict(json_data: str):
        return json.loads(json_data)

    def replace_cls(self, params: dict, cls, *fields: Any):
        for k, v in params.items():
            for f in fields:
                fd = getattr(cls, f, "")
                if fd is None:
                    continue
                if k in fd:
                    data = self.replace_params(f, fd, params)
                    for a, b in data.items():
                        fd = fd.replace(a, b)
                        setattr(cls, f, fd)

    def replace_args(self, params, data: TestCase, constructors: List[Constructor], asserts: List[TestCaseAsserts]):
        self.replace_testcase(params, data)
        self.replace_constructors(params, constructors)
        self.replace_asserts(params, asserts)

    def replace_testcase(self, params, data: TestCase):
        """
        替换测试用例中的参数
        :param params:
        :param data:
        :return:
        """
        self.replace_cls(params, data, "request_headers", "body", "url")

    def replace_constructors(self, params, constructors: List[Constructor]):
        """
        替换数据构造中的参数
        :param params:
        :param constructors:
        :return:
        """
        for c in constructors:
            self.replace_cls(params, c, "constructor_json")

    def replace_asserts(self, params, asserts: List[TestCaseAsserts]):
        """
        替换断言中的参数
        :param params:
        :param asserts:
        :return:
        """
        for a in asserts:
            self.replace_cls(params, a, "expected", "actually")

    @staticmethod
    async def run_with_test_data(env, data, report_id, case_id, params_pool: dict = None, request_param: dict = None,
                                 path="主case", name: str = "", data_id: int = None, retry_minutes: int = 0):
        retry_times = Config.RETRY_TIMES if retry_minutes > 0 else 0
        times = 0
        for i in range(retry_times + 1):
            start_at = datetime.now()
            executor = Executor()
            result, err = await executor.run(env, case_id, params_pool, request_param, path)
            finished_at = datetime.now()
            cost = "{}s".format((finished_at - start_at).seconds)
            if err is not None:
                status = 2
            else:
                stat = 0 if result.get("status") else 1
            # 若status 不为0,代表case执行失败,走重试逻辑
            if status != 0 and i < retry_times:
                await  asyncio.sleep(60 * retry_times)
                times += 1
                continue
            asserts = result.get("asserts")
            url = result.get("url")
            case_logs = result.get("logs")
            body = result.get("request_data")
            status_code = result.get("status_code")
            request_method = result.get("request_method")
            request_headers = result.get("request_headers")
            response = result.get("response")
            case_name = result.get("case_name")
            response_headers = result.get("request_headers")
            cookies = result.get("cookies")
            req = json.dumps(request_param, ensure_ascii=False)
            data[case_id].append(status)
            await TestResultDao.insert(report_id, case_id, case_name, status, case_logs, start_at, finished_at, url,
                                       body, request_method, request_headers, cost, asserts, response_headers, response,
                                       status_code, cookies, times, req, name, data_id)
            break

    @staticmethod
    async def run_single(env: int, data, report_id, case_id, params_pool: dict = None, path="主case", retry_minutes=0):
        test_data = await SakuraTestCaseDataDao.list_testcase_data_by_env(env, case_id)
        if not test_data:
            await Executor.run_with_test_data(env, data, report_id, case_id, params_pool, dict(), path, "默认数据",
                                              retry_minutes=retry_minutes)
        else:
            await asyncio.gather(
                *(Executor.run_with_test_data(env, data, report_id, case_id, params_pool,
                                              Executor.get_dict(x.json_data), path, x.name, x.id,
                                              retry_minutes=retry_minutes)) for x in test_data)

    @case_log
    def replace_body(self, req_params, body, body_type):
        """
        根据传入的构造参数进行参数替换
        :param req_params:
        :param body:
        :param body_type:
        :return:
        """
        if body_type != BodyType.json:
            self.append("当前请求数据不为JSON,跳过替换")
            return body
        try:
            if body:
                data = json.loads(body)
                if req_params is not None:
                    for k, v in req_params.items():
                        if data.get(k) is not None:
                            data[k] = v
                return json.dumps(data, ensure_ascii=False)
            self.append("body为空,不进行替换")
        except Exception as e:
            self.append(f"替换请求body失败:{str(e)}")
        return body

    @staticmethod
    def get_time():
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @case_log
    def my_assert(self, asserts: List, json_format: bool) -> [str, bool]:
        """
        断言验证
        :param asserts:
        :param json_format:
        :return:
        """
        result = {}
        ok = True
        if len(asserts) == 0:
            self.append("未设置断言,用例结束")
            return json.dumps(result, ensure_ascii=False), ok
        for item in asserts:
            try:
                # 解析预期/实际结果
                expected = self.translate(item.expected)
                # 判断请求地址返回是否是json格式,如果不是则进行loads操作
                actually = self.translate(item.actually)
                status, err = self.ops(item.assert_type, expected, actually)
                result[item.id] = {'status': status, 'msg': err}
            except Exception as e:
                if ok is True:
                    ok = False
                self.append(f"预期结果:{item.expected}\n 实际结果:{item.actually}\n")
                result[item.id] = {'status': False, 'msg': f"断言取值失败,请检查断言语句:{str(e)}"}
        return json.dumps(result, ensure_ascii=False), ok

    @case_log
    def ops(self, assert_type: str, exp, act) -> (bool, str):
        """
        通过断言类型进行校验
        :param assert_type:
        :param exp:
        :param act:
        :return:
        """
        if assert_type == "equal":
            if exp == act:
                return True, f"预期结果:{exp} 等于 实际结果:{act}【✔️】"
            return False, f"预期结果:{exp} 等于 实际结果:{act}【❌】"
        if assert_type == "not_equal":
            if exp != act:
                return True, f"预期结果:{exp} 不等于 实际结果:{act}【✔️】"
            return False, f"预期结果:{exp} 等于 实际结果:{act}【❌】"
        if assert_type == "in":
            if exp in act:
                return True, f"预期结果:{exp} 包含于 实际结果:{act}【✔️】"
            return False, f"预期结果:{exp} 不包含 于实际结果:{act}【❌】"
        if assert_type == "not_in":
            if exp not in act:
                return True, f"预期结果:{exp} 不包含 于实际结果:{act}【✔️】"
            return False, f"预期结果:{exp} 包含于 实际结果:{act}【❌】"
        if assert_type == "contain":
            if act in exp:
                return True, f"预期结果:{exp} 包含 实际结果:{act}【✔️】"
            return False, f"预期结果:{exp} 不包含 实际结果:{act}【❌】"
        if assert_type == "not_contain":
            if act not in exp:
                return True, f"预期结果:{exp} 不包含 实际结果:{act}【✔️】"
            return False, f"预期结果:{exp} 包含 实际结果:{act}【❌】"
        if assert_type == "length_eq":
            if exp == len(act):
                return True, f"预期数量:{exp} 等于 实际数量:{act}【✔️】"
            return False, f"预期数量:{exp} 不等于 实际数量:{act}【❌】"
        if assert_type == "length_gt":
            if exp > len(act):
                return True, f"预期数量:{exp} 大于 实际数量:{len(act)}【✔️】"
            return False, f"预期数量:{exp} 不大于 实际数量:{len(act)}【❌】"
        if assert_type == "length_eq":
            if exp >= len(act):
                return True, f"预期数量:{exp} 大于等于 实际数量:{len(act)}【✔️】"
            return False, f"预期数量:{exp} 小于 实际数量:{len(act)}【❌】"
        if assert_type == "length_le":
            if exp <= len(act):
                return True, f"预期数量:{exp} 小于 实际数量:{len(act)}【✔️】"
            return False, f"预期数量:{exp} 大于 实际数量:{len(act)}【❌】"
        if assert_type == "length_lt":
            if exp < len(act):
                return True, f"预期数量:{exp} 小于 实际数量:{len(act)}【✔️】"
            return False, f"预期数量:{exp} 不小于 实际数量:{len(act)}【❌】"
        if assert_type == "json_equal":
            data = JsonCompare().compare(exp, act)
            if len(data) == 0:
                return True, "预期JSON 等于 实际JSON【✔️】"
            return False, data
        if assert_type == "text_in":
            if isinstance(act, str):
                # 如果b是str,则不转换
                if exp in act:
                    return True, f"预期结果:{exp} 文本包含于 实际结果:{act}【✔️】"
                return False, f"预期结果:{exp} 文本不包含于 实际结果:{act}【❌】"
            temp = json.dumps(act, ensure_ascii=False)
            if exp in temp:
                return True, f"预期结果:{exp} 文本包含于 实际结果:{act}【✔️】"
            return False, f"预期结果:{exp} 文本不包含于 实际结果:{act}【❌】"
        if assert_type == "text_not_in":
            if isinstance(act, str):
                if exp in act:
                    return True, f"预期结果:{exp} 文本包含于 实际结果:{act}【❌】"
                return False, f"预期结果:{exp} 文本不包含于 实际结果:{act}【✔️】"
            temp = json.dumps(act, ensure_ascii=False)
            if exp in temp:
                return True, f"预期结果:{exp} 文本包含于 实际结果:{act}【❌】"
            return False, f"预期结果:{exp} 文本不包含于 实际结果:{act}【✔️】"
        return False, "不支持的断言的方式💔"

    def get_el_expression(self, string: str):
        """
        获取字符串中的el表达式
        :param string:
        :return:
        """
        return [] if string is None else re.findall(Executor.pattern, string)

    @case_log
    def translate(self, data):
        """
        反序列化为Py对象
        :param data:
        :return:
        """
        return json.loads(data)

    def replace_branch(self, branch: str, params: dict):
        if not params:
            return branch
        if branch.startswith("#"):
            # 说明branch也是个子变量
            data = branch[1:]
            if len(data) == 0:
                return branch
            dist = params.get(data)
            if dist is None:
                return branch
            return params.get(data)
        return branch

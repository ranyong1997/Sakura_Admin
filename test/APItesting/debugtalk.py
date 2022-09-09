import time
import random
import requests
from httprunner import __version__


def get_httprunner_version():
    return __version__


def sum_two(m, n):
    return m + n


def sleep(n_secs):
    time.sleep(n_secs)


def random_num():
    return random.randint(1, 10)


def setupHook(request):
    print("**********开始执行测试用例**********")
    print("request请求：{}".format(request))


def teardownHook(response):
    print("**********修改响应结果后再进行断言**********")
    response.status_code = 300
    response.body["success"] = "false"


def getToken():
    """
    获取token
    :return:
    """
    url = "http://192.168.1.243:7777/auth/login"
    header = {'Content-Type: application/json'}
    data = {
        "username": "root",
        "password": "123456"
    }
    res = requests.post(url,headers=header,data=data).json()
    return res['data']['token']
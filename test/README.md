# 使用HttpRunner 3.x实现接口自动化测试
**特点：**
- 继承了Requests的全部特性，可轻松实现 HTTP(S) 的各种测试需求
- 使用YAML或JSON格式定义测试用例，并使用Pytest以简洁优雅的方式运行用例
- 支持使用HAR实现接口录制并生成测试用例
- 支持variables/ extract/ validate/hooks机制，以应对非常复杂的测试场景
- 使用debugtalk.py插件自定义函数，可以在测试用例的任何部分调用
- 使用Jmespath，更加方便对返回的json进行校验
- 通过Pytest的强大插件生态补充了httprunner的功能
- 使用Allure，让测试报告更加美观，可读性更强
- 通过与locust的结合，可以很方便利用httprunner进行接口性能测试
- 支持CLI命令，更可与持续集成工具(CI/CD)完美结合，如Jenkins

HttpRunner官方网址：[HttpRunner 3.x文档](https://httprunner.com/httprunner/)

## HttpRunner安装

```python
pip install httprunner	# 安装httprunner，若下载失败请使用国内源下载
hrun -V		# 查看httprunner版本
# 版本显示正确表示安装完成，执行以下命令，通常安装httprunner时会一并安装，若不存在请通过pip命令单独安装
har2case -V	# 查看har2case版本
locusts -V	# 查看locust版本
```

```
PS E:\gitpush\Sakura_Admin\test\APItesting> hrun -V
3.1.11
PS E:\gitpush\Sakura_Admin\test\APItesting> locusts -V
E:\gitpush\Sakura_admin\venv\lib\site-packages\locust\__init__.py:11: MonkeyPatchWarning: Monkey-patching ssl after ssl has already been imported may lead to errors, including RecursionError on Python 3.6. It may also silently lead to incorrect behaviour on Python 3
.7. Please monkey-patch earlier. See https://github.com/gevent/gevent/issues/1016. Modules that had direct imports (NOT patched): ['urllib3.contrib.pyopenssl (E:\\gitpush\\Sakura_admin\\venv\\lib\\site-packages\\urllib3\\contrib\\pyopenssl.py)'].
  monkey.patch_all()
NOTICE: gevent monkey patches have been applied !!!
locust 2.12.0
```

安装完成后以下5个命令会自动写入系统环境变量中。

- httprunner：主命令，用于所有功能
- hrun：指令httprunner run的别名，用于运行YAML/JSON/Pytest测试用例
- hmake：指令httprunner make的别名，将YAML/JSON用例转换成Pytest用例
- har2case：指令httprunner har2case的别名，将HAR文件
- locust：利用locust运行性能测试

## YAML介绍

> HttpRunner3.x支持三种格式的测试用例：YAML、JSON以及Pytest

### YAML的语法规则：

- 大小写敏感（区分大小写）
- 使用缩进表示层级关系
- 不允许使用Tab键，只允许使用空格键进行缩进
- 缩进的空格数量无要求，但相同层级关系左侧必须对齐
- 使用#表示注释

### 支持的数据类型

- 对象：键值对的集合，又称为映射/哈希/字典

```yaml
key: # 键值之间的冒号后面需要有空格
    child-key: value
    child-key2: value2
```

- 数组：一组按次序排列的值，又称为序列/列表

```yaml
- 		# 以 - 开头的行表示构成一个数组，如下为两组数据
 - A	# 第一组数据只有A，A又独为一组
-		# 第二组数据有B和C，B和C又各为一组
 - B
 - C
```

- 纯量：单个的、不可再分的值

```yaml
# 字符串、布尔值、整数、浮点数、时间等属于纯量
string:
    - 这是字符串
    - 'Hello world'  #可以使用双引号或者单引号包裹特殊字符
    - newline
      newline2    #字符串可以拆成多行，每一行会被转化成一个空格
int:
    - 123
    - 0b1010_0111_0100_1010_1110    #二进制表示
```

## HttpRunner使用

> 可通过先快速搭建脚手架，使用命令**httprunner startproject 项目名称**，例如：**httprunner startproject APItesting**

![image-20220914104621068](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202209141046051.png)

### 用例结构及编写

> 以实际项目为例，请通过注释了解测试用例结构及编写方法，我这里用一个登录接口作为演示

```python
# Login.yaml文件
config: # 全局配置，每个测试用例都必须有config部分
    name: 登录接口测试  # 用例描述，name是必须要有的，其它配置项为可选项，根据实际项目增删
    base_url: ${ENV(HOST)}  # 项目路径，亦可配置在环境配置env文件中
    variables:  # 参数变量
        Opertype: ADD
        poolId: e3cc3d8b90b4465998ddfec569a66612
        resType: SECURITYGROUP
        name: dyd${random_num()}  # 此处调用了在debugtalk.py中定义的生成随机数的函数
        secGType: SECURITY_VM
        adapterType: SINGLE
        approvalType: SECURITYGROUP-ADD
    verify: False  # 指定是否验证服务器的 TLS 证书。如果我们想记录测试用例执行的 HTTP 流量，这尤其有用，因为如果 verify 未设置或设置为 True，则会发生 SSLError。

teststeps:  # 每个测试用例都有1个或多个测试步骤，name，request是必须有的，其它根据实际项目配置
-   name: 登录平台  # 步骤一，登录平台
    request:  # 配置请求信息，（请求方法、url、头信息、传参等）
        method: POST
        url: ${ENV(HOST)}/auth/login  # 因全局配置中已存在base_url,故在测试步骤不必填写，其会自动拼接
        headers:
            accept: application/json
            Content-Type: application/json
        data: # 入参参数
            username: ${ENV(USERNAME)}  # 引用env环境配置中的账号和密码
            password: ${ENV(PASSWORD)}
    extract:  # 提取响应数据中的access_token值
        access_token: body.data.token # # body是响应体json的根节点
    validate: # 判断是否成功，可使用多个断言
      - eq: ["status_code", 200]
```

上面示例中用到env文件和debugtalk.py文件

通常在自动化测试项目的根目录中创建 **.env** 文件，并将敏感数据信息放置到其中，存储采用 **name=value** 的格式，通过脚手架生成的接口测试项目中，会自动生成**.env**文件，可直接在**.env**中添加环境变量，**.env**文件中除注释外，其它行都不允许存在空格，引用环境变量的方法**${ENV(name)}**

![image-20220914105208096](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202209141052659.png)

debugtalk.py文件名不能变更，脚手架生成的接口测试项目中也会自动生成，在此文件中写python脚本，然后在YAML文件中调用，调用方法`${func()}`，例如上文中用到的随机数`${random_num()}`

```python
# debugtalk.py
import random
def random_num():
    return random.randint(1,10)
```

## 用例执行

```python
hrun testcases/xxx.yml 						# 运行指定路径的用例
hrun testcases/xxx1.yml testcases/xxx2.yml	# 运行指定路径的多个用例
hrun testcases	# 运行testcases目录下所有的用例
```

hrun先将YAML/JSON转为pytest(python)格式，然后再运行pytest，所以运行yml文件后会自动在同一目录下生成pytest文件，生成的pytest用例名增加_test后缀，且.yml/yaml/.json替换为.py

以后可以直接通过pytest命令执行.py格式的测试用例，hrun也可以直接使用pytest的参数，比如hrun -sv login.yml，以下示例是上文中参数化示例执行后生成的.py文件内容

```python
from httprunner import HttpRunner, Config, Step, RunRequest, RunTestCase


class TestCaseLogin(HttpRunner):

    config = (
        Config("登录接口测试")
        .variables(
            **{
                "Opertype": "ADD",
                "poolId": "e3cc3d8b90b4465998ddfec569a66612",
                "resType": "SECURITYGROUP",
                "name": "dyd${random_num()}",
                "secGType": "SECURITY_VM",
                "adapterType": "SINGLE",
                "approvalType": "SECURITYGROUP-ADD",
            }
        )
        .base_url("${ENV(HOST)}")
        .verify(False)
    )

    teststeps = [
        Step(
            RunRequest("登录平台")
            .post("${ENV(HOST)}/auth/login")
            .with_headers(
                **{"accept": "application/json", "Content-Type": "application/json"}
            )
            .with_data({"username": "${ENV(USERNAME)}", "password": "${ENV(PASSWORD)}"})
            .extract()
            .with_jmespath("body.data.token", "access_token")
            .validate()
            .assert_equal("status_code", 200)
        ),
    ]


if __name__ == "__main__":
    TestCaseLogin().test_start()
```

## 测试报告

allure-pytest需要单独安装`pip install allure-pytest`

```python
hrun testcases --alluredir=/report/allure	# 生成中间结果
allure serve /report/allure					# 在线打开报告
allure generate report/allure -o report/allure/html	# 生成html报告
```

![image-20220914105959405](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202209141100632.png)

## 压力测试

locust详细使用方法后续单独开篇，此处简单介绍一下，命令为`locusts -f file.py`，使用-f指定`YAML/JSON`格式的测试用例时，会首先转换为pytest，然后运行负载测试，所以可以直接压测测试接口时已自动生成的.py格式的文件，下图为压测结果的部分截图

![image-20220914110410741](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202209141104597.png)

![image-20220914110415486](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202209141104543.png)

## 录制与生成测试用例

### Mac Charles操作方法

[Charles使用指南](https://www.jianshu.com/p/0db984415bd7)

![image-20220914110800171](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202209141108765.png)

### Windows Fiddler操作方法

[Fiddler使用指南](https://blog.csdn.net/weixin_44330336/article/details/125522082)



![image-20220914111450582](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202209141114881.png)

![image-20220914111709734](https://cdn.jsdelivr.net/gh/ranyong1997/image_collect@main/img/202209141117285.png)

## 生成测试用例

可以使用命令`har2case`将HAR文件转成测试用例

```python
har2case list_user.har		# 默认转为json格式
har2case list_user.har -2y	# -2y表示转为yaml格式
```

下面是转换为yaml格式的内容，通常是需要修改的，比如：断言，关联关系、参数化等都是需要修改完善的

```yaml
config:
    name: testcase description
    variables: {}
    verify: false
teststeps:
-   name: /auth/listUser
    request:
        cookies:
            Pycharm-e98a1fd0: 1808989d-bcda-4392-80de-9c1674e9bd9a
        headers:
            Accept-Encoding: gzip, deflate, br
            Accept-Language: zh-CN,zh;q=0.9,en;q=0.8
            Connection: keep-alive
            Cookie: Pycharm-e98a1fd0=1808989d-bcda-4392-80de-9c1674e9bd9a
            Host: localhost:7777
            Referer: http://localhost:7777/docs
            Sec-Fetch-Dest: empty
            Sec-Fetch-Mode: cors
            Sec-Fetch-Site: same-origin
            User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
                (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36
            accept: application/json
            sec-ch-ua: '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"'
            sec-ch-ua-mobile: ?0
            sec-ch-ua-platform: '"Windows"'
            token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2NjMzODQzNTAsImlkIjoxLCJ1c2VybmFtZSI6InJvb3QiLCJuYW1lIjoicm9vdCIsImVtYWlsIjoicm9vdEByb290LmNvbSIsInJvbGUiOjIsInBob25lIjpudWxsLCJjcmVhdGVkX2F0IjoiMjAyMi0wOC0zMCAyMTo0Nzo1MSIsInVwZGF0ZWRfYXQiOiIyMDIyLTA4LTMwIDIxOjQ3OjUxIiwiZGVsZXRlZF9hdCI6MCwidXBkYXRlX3VzZXIiOm51bGwsImxhc3RfbG9naW5fYXQiOiIyMDIyLTA5LTE0IDExOjEyOjMwIiwiYXZhdGFyIjpudWxsLCJpc192YWxpZCI6dHJ1ZX0.ZpiU6EW1_naK0-GdaiP9I9febxmdGcxIT7trNDXzG74
        method: GET
        url: http://localhost:7777/auth/listUser
    validate:
    -   eq:
        - status_code
        - 200
    -   eq:
        - body.code
        - 0
    -   eq:
        - body.msg
        - 操作成功

```

对生成的测试用例进行修改完善后就可以执行测试啦

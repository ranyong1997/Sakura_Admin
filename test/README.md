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
 是
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

### 用例结构及编写

> 以实际项目为例，请通过注释了解测试用例结构及编写方法，我这里用一个登录接口作为演示


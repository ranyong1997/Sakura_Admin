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

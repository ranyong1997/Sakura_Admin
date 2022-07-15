# NOTE: Generated By HttpRunner v3.1.11
# FROM: testcases\demo_testcase_ref.yml


import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


from httprunner import HttpRunner, Config, Step, RunRequest, RunTestCase

from testcases.demo_testcase_request_test import (
    TestCaseDemoTestcaseRequest as DemoTestcaseRequest,
)


class TestCaseDemoTestcaseRef(HttpRunner):

    config = (
        Config("request methods testcase: reference testcase")
        .variables(
            **{
                "foo1": "testsuite_config_bar1",
                "expect_foo1": "testsuite_config_bar1",
                "expect_foo2": "config_bar2",
            }
        )
        .base_url("https://postman-echo.com")
        .verify(False)
    )

    teststeps = [
        Step(
            RunTestCase("request with functions")
            .with_variables(
                **{"foo1": "testcase_ref_bar1", "expect_foo1": "testcase_ref_bar1"}
            )
            .call(DemoTestcaseRequest)
            .export(*["foo3"])
        ),
        Step(
            RunRequest("post form data")
            .with_variables(**{"foo1": "bar1"})
            .post("/post")
            .with_headers(
                **{
                    "User-Agent": "HttpRunner/${get_httprunner_version()}",
                    "Content-Type": "application/x-www-form-urlencoded",
                }
            )
            .with_data("foo1=$foo1&foo2=$foo3")
            .validate()
            .assert_equal("status_code", 200)
            .assert_equal("body.form.foo1", "bar1")
            .assert_equal("body.form.foo2", "bar21")
        ),
    ]


if __name__ == "__main__":
    TestCaseDemoTestcaseRef().test_start()

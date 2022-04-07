import unittest
from Common.handle_data import EnvData, clear_EnvData_attrs, replace_mark_with_data
from Common.myddt import ddt, data

from Common.handle_excel import HandleExcel
from Common.handle_path import datas_dir
from Common.handle_requests import send_requests
from Common.handle_db import HandleDB
from Common.my_logger import logger
from Common.handle_phone import get_old_phone
from jsonpath import jsonpath
from time import sleep

he = HandleExcel(datas_dir + "\\api_cases.xlsx", "sku业务流")
cases = he.read_all_datas()
he.close_file()
db = HandleDB()


@ddt
class TestSkuMasterFlow(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        # 清理环境变量EnvData
        clear_EnvData_attrs()

        # 得到登陆的用户名和密码
        user, passwd = get_old_phone()
        # 登陆接口调用。
        resp = send_requests("POST", "/auth/login", {"username": user, "password": passwd})
        setattr(EnvData, "token", jsonpath(resp.json(), "$..token")[0])

    @data(*cases)
    def test_masterflow(self, case):
        logger.info("*********   执行用例{}：{}   *********".format(case["id"], case["title"]))

        # 步骤 测试数据 - 发起请求
        # 发起请求,判断是否需要传递token
        if hasattr(EnvData, "token"):
            if case["check_sql"]:
                # 获取id
                logger.info("执行sql：{}".format(case["check_sql"]))
                sql = case["check_sql"]
                data = db.select_one_data(sql)
                logger.info("获取审核的id：{}".format(data['id']))

                # 替换提交的数据，id
                if case['url'].find("{id}") or case['request_data'].find("{id}") != -1:
                    case = replace_mark_with_data(case, "{id}", str(data['id']))

            # 需要token就传入，不需要就执行else
            response = send_requests(case["method"], case["url"], case["request_data"], token=EnvData.token)
        else:
            response = send_requests(case["method"], case["url"], case["request_data"])

        # 期望结果，从字符串转换成字典对象。
        expected = eval(case["expected"])

        logger.info("用例的期望结果为：{}".format(case["expected"]))

        try:
            self.assertEqual(response.status_code, expected["code"])
            if ('user' in response.json()):
                self.assertEqual(response.json()["user"]["roles"], expected["message"])
            else:
                self.assertEqual(response.json()["message"], expected["message"])
        except AssertionError:
            logger.exception("断言失败！")
            raise


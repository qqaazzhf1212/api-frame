import unittest
from Common.myddt import ddt, data

from Common.my_logger import logger
from Common.handle_excel import HandleExcel
from Common.handle_requests import send_requests
from Common.handle_path import datas_dir
from Common.handle_db import HandleDB

he = HandleExcel(datas_dir + "\\api_cases.xlsx", "登陆")
case = he.read_all_datas()
he.close_file()
db = HandleDB()


@ddt
class TestLogin(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        logger.info("************** 加标接口 开始测试 ************")

    @classmethod
    def tearDownClass(cls) -> None:
        logger.info("************** 加标接口 结束测试 ************")

    @data(*case)
    def test_login(self, case):
        logger.info("*********   执行用例{}：{}   *********".format(case["id"], case["title"]))

        # 步骤 测试数据 - 发起请求
        response = send_requests(case["method"], case["url"], case["request_data"])

        # 期望结果，从字符串转换成字典对象。
        expected = eval(case["expected"])

        logger.info("用例的期望结果为：{}".format(case["expected"]))

        try:
            self.assertEqual(response.status_code, expected["code"])
            self.assertEqual(response.json()["user"]["roles"], expected["msg"])
            # 如果check_sql有值，说明要做数据库校验。
            if case["check_sql"]:
                logger.info()
                result = db.select_one_data(case["check_sql"])
                self.assertIsNotNone(result)
        except AssertionError:
            logger.exception("断言失败！")
            raise

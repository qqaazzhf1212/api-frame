import unittest
from unittest.suite import TestSuite
import time
from BeautifulReport import BeautifulReport
from unittestreport import TestRunner

from Common.handle_path import cases_dir, reports_dir, debug_dir

# 收集用例
ctime = time.strftime('%Y-%m-%d-%H-%M-%S')
report_name = ctime + '-测试报告.html'
suite = unittest.TestLoader().discover(start_dir=cases_dir, pattern='test*.py')

# 生成报告方法一
# runner = TestRunner(suite=suite, filename=report_name, report_dir=reports_dir, title='主数据接口自动化报告', tester='LH',
#                     desc='api测试验证')
# runner.run()


# 生成报告方法二
br = BeautifulReport(suite)
br.report(filename=report_name, description='测试报告', report_dir=reports_dir, theme='theme_default')

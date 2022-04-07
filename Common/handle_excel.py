"""
excel类，你的需求是实现是什么?
1、读取表头
2、读取数据 - 读取表头以外的所有数据。 - 返回值：列表，成员是每一行数据

初始化工作？  加载一个excel,打开一个表单。

"""
from openpyxl import load_workbook
import json


class HandleExcel:

    def __init__(self, file_path, sheet_name):
        self.wb = load_workbook(file_path)
        self.sh = self.wb[sheet_name]

    def __read_titles(self):
        titles = []
        for item in list(self.sh.rows)[0]:  # 遍历第1行当中每一列
            titles.append(item.value)
        return titles

    def read_all_datas(self):
        all_datas = []
        titles = self.__read_titles()
        for item in list(self.sh.rows)[1:]:  # 遍历数据行
            values = []
            for val in item:  # 获取每一行的值
                values.append(val.value)
            res = dict(zip(titles, values))  # title和每一行数据，打包成字典
            all_datas.append(res)
        return all_datas

    def close_file(self):
        self.wb.close()


if __name__ == '__main__':
    import os
    # file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "TestDatas\\api_cases.xlsx")
    # print(file_path)
    # exc = HandleExcel(file_path, "登陆")
    # he = HandleExcel(file_path , "基础数据搜索")
    # he = HandleExcel(file_path , "基础数据搜索")
    # he = HandleExcel(file_path, "spu搜索")
    # print(he.read_all_datas())
    # cases = exc.read_all_datas()
    # print(cases)
#     exc.close_file()
#     for case in cases:
#         print(case)

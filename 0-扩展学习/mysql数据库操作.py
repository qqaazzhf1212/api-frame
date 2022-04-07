"""
各大数据库操作文章：http://www.lemfix.com/topics/306

mysql数据库：pymysql
pip install pymysql

数据库操作步骤：
1、连接数据库，创建游标
2、执行sql语句
3、获取执行的结果
4、关闭数据库连接。
"""

import pymysql

# 1、建立连接
conn = pymysql.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="123456",
    database="djtest",
    charset="utf8",
    cursorclass=pymysql.cursors.DictCursor
)

# 2、创建游标
cur = conn.cursor()

# 3、执行sql语句
# sql = 'select * from member where mobile_phone="13030780869"'
sql = 'select * from jobs_job where id=7'
count = cur.execute(sql)  # 返回的是，sql语句执行结果的行数。

# 4、获取sql语句 执行后的，数据结果
one = cur.fetchone()  # 获取结果集当中一条数据。
print("第一条数据：",one)
# two = cur.fetchone()
# print("第二条数据：",two)
# print("*****************************************")
# # 获取所有的结果
# all = cur.fetchall()  # 获取所有的数据。列表。
# print("所有数据：",all)



# 5、关闭游标 ，关闭数据库连接。
cur.close()
conn.close()
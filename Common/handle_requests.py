"""
基于项目做定制化封装
1、鉴权:token
2、项目通用的请求头:
    {"XXXX": "XXXX"}
    
3、请求体格式：application/json
"""
import requests
import json

from Common.my_logger import logger
from Common.handle_config import conf


#
def send_requests(method, url, data=None, token=None):
    """
    :param method:
    :param url:
    :param data:字典形式的数据。
    :param token:
    :return:
    """
    logger.info("发起一次HTTP请求")
    # 得到请求头
    headers = __handle_header(token)
    # 得到完整的url - 拼接url
    url = __pre_url(url)
    # 请求数据的处理 - 如果是字符串，则转换成字典对象。
    data = __pre_data(data, token)
    # 将请求数据转换成字典对象。
    logger.info("请求头为：{}".format(headers))
    logger.info("请求方法为：{}".format(method))
    logger.info("请求url为：{}".format(url))
    logger.info("请求数据为：{}".format(data))
    # 根据请求类型，调用请求方法
    method = method.upper()  # 大写处理
    if method == "GET":
        resp = requests.get(url, data, headers=headers, verify=True)
    else:
        resp = requests.post(url, json=data, headers=headers, verify=True)
    logger.info("响应状态码为：{}".format(resp.status_code))
    logger.info("响应数据为：{}".format(resp.json()))
    return resp


def __handle_header(token=None):
    """
    处理请求头。加上项目当中必带的请求头。如果有token，加上token。
    :param token: token值
    :return: 处理之后headers字典
    """
    headers = {"Content-Type": "application/json"}
    if token:
        headers["authorization"] = "Bearer {}".format(token)
    return headers


def __pre_url(url):
    """
    拼接接口的url地址。
    """
    base_url = conf.get("server", "base_url")
    if url.startswith("/"):
        return base_url + url
    elif url.startswith("http://") or url.startswith("https://"):
        return url
    else:
        return base_url + "/" + url


def __pre_data(data, token=None):
    """
    如果data是字符串，则转换成字典对象。
    """
    if data is not None and isinstance(data, str):
        # 如果有null，则替换为None
        if data.find("null") != -1:
            data = data.replace("null", "None")
        # 使用eval转成字典.eval过程中，如果表达式有涉及计算，会自动计算。
        data = eval(data)

    # 如果是v3版本，需要加上sign和timestamp2个参数。
    if conf.get("server", "auth_type") == "lemonban.v3" and token is not None:
        from Common.handle_rsa import generator_sign
        sign, timestamp = generator_sign(token)
        data["sign"] = sign
        data["timestamp"] = timestamp

    return data

# if __name__ == '__main__':
# login_url = "http://api.lemonban.com/futureloan/member/login"
# login_datas = {"mobile_phone": "13845467789", "pwd": "1234567890"}
# resp = send_requests("POST",login_url,login_datas)
# print(resp.json())
# # token = resp.json()["data"]["token_info"]["token"]
# member_id =  resp.json()["data"]["id"]
#
# recharge_url = "http://api.lemonban.com/futureloan/member/recharge"
# recharge_data = {"member_id": member_id, "amount": 2000}
# resp = send_requests("POST",recharge_url,recharge_data)
# print(resp.json())

# login_url="https://api-zhushuju.jk.com/auth/login"
# login_datas={"username":"test","password":"atjxwJ2SilprUAr7avYwNRiBMeEcy9OmNIQcDK/7ct2H21gwgGjW1Aiwy+Alqckchpqi2n10fXzuJD14Fo2EfQ=="}
# resp=send_requests("POST",login_url,login_datas)
# # print(resp.json())
#
# search_url="https://api-zhushuju.jk.com/product/sku/page"
# search_datas={"page":1,"size":10,"sort":["id,desc"],"approvalStatus":"4","drugType":"2"}
# resp1=send_requests("POST",search_url,search_datas)
#
#
# if ('user' in resp.json()):
#     print('1')
# else:
#     print('2')

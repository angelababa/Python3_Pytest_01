#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# author:laobai
# datetime:2020/5/1 08:38
from utils.RequestsUtil import requests_get,requests_post,Request
from config.Conf import ConfigYaml
import pytest,json
from utils.AssertUtil import AssertUtil
from common.Base import init_db
'''
login_4	登录	登录成功	http://211.103.136.242:8064/authorizations/
POST	json	{"username":"python","password":"12345678"}	user_id': 1, 'username': 'python'			n			200
'''
# 登录
# 1、导入包
import requests
# 2、定义登录方法
def test_login():
# 3、定义测试数据
    conf_y = ConfigYaml()
    url_path = conf_y.get_conf_url()
    url = url_path + "/authorizations/"
#     url = "http://211.103.136.242:8064/authorizations/"
    data = {"username":"python","password":"12345678"}
# 4、发送POST请求
#     r = requests.post(url,json=data)
#     r = requests_post(url,json=data)
    request = Request()
    r = request.post(url,json=data)
# 5、输出结果
#     print(r.json())
    print(r)
    # 返回状态码
    code = r['code']
    AssertUtil().assert_code(code,200)
    body = r['body']
    # print(body)
    AssertUtil().assert_in_body(body,'"username": "python"')

    # 1、初始化数据库对象
    conn = init_db('db_1')
    # 2、查询结果
    res_db = conn.fetchone("select id from tb_users where username='python'")
    print("数据库查询结果:",res_db)
    # 3、验证
    user_id = body['user_id']
    assert user_id == res_db['id']


'''
Info_2	个人信息	获取个人信息正确	/user/	
login_4	get			id': 1, 'username': 'python', 'mobile': '17701397029', 'email': '952673638@qq.com'			y	{"Authorization": "JWT ${token}$"}		200	select id,username,mobile,email from tb_users where username='python'
headers: {
    'Authorization':'JWT ' + this.token
}
'''
def test_info():
    # 1、参数
    conf_y = ConfigYaml()
    url_path = conf_y.get_conf_url()
    url = url_path + "/user/"
    # url = 'http://211.103.136.242:8064/user/'
    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1ODg1MDIzMjgsInVzZXJuYW1lIjoicHl0aG9uIiwiZW1haWwiOiI5NTI2NzM2MzhAcXEuY29tIiwidXNlcl9pZCI6MX0.uQuz0gCtfHAM4RzhmNfTuqCRemU-A77UcK9SIl5ps5o'
    headers = {
        'Authorization':'JWT ' + token
        }
    # 2、get请求
    # r = requests.get(url,headers=headers)
    # r = requests_get(url,headers = headers)
    request = Request()
    r = request.get(url,headers=headers)
    # 3、输出
    # print(r.json())
    print(r)
'''
cate_1	商品列表数据	商品列表数据正确	/categories/115/skus/		
get	json	" {
 ""page"":""1"",
 ""page_size"": ""10"",
 ""ordering"": ""create_time""
 }"				n			200	
'''
def goods_list():
    # 1、参数
    conf_y = ConfigYaml()
    url_path = conf_y.get_conf_url()
    url = url_path + "/categories/115/skus/"
    # url = "http://211.103.136.242:8064/categories/115/skus/"
    data = {
            "page":"1",
            "page_size": "10",
            "ordering": "create_time"
            }
    # 2、请求
    r = requests.get(url,json=data)
    # 3、结果
    print(r.json())

'''
cart_1	购物车	添加购物车成功	/cart/	login_4	
post	json	{"sku_id": "3","count": "1", "selected": "true"}	sku_id': 3, 'count': 1			n	{"Authorization": "JWT ${token}$"}		201	
'''

def cart():
    # 1、参数
    conf_y = ConfigYaml()
    url_path = conf_y.get_conf_url()
    url = url_path + "/cart/"
    # url = "http://211.103.136.242:8064/cart/"
    data = {"sku_id": "3","count": "1", "selected": "true"}
    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1ODg0MDc0MTUsInVzZXJuYW1lIjoicHl0aG9uIiwiZW1haWwiOiI5NTI2NzM2MzhAcXEuY29tIiwidXNlcl9pZCI6MX0.9vLuVHskV89xPDKy4EvhGNqULD1c5ciHFRIHyKH-29U'
    headers = {
        'Authorization': 'JWT ' + token
    }
    # 2、请求
    # r = requests.post(url,json=data,headers=headers)
    r = requests_post(url,json=data,headers=headers)
    # 3、结果
    # print(r.json())
    print(r)
'''
order_1	订单	保存订单	/orders/	login_4	
post	json	{ "address":"1","pay_method":"1" }	order_id			n	{"Authorization": "JWT ${token}$"}		201	
'''
def order():
    # 1、参数
    # conf_y = ConfigYaml()
    # url_path = conf_y.get_conf_url()
    # url = url_path + "/orders/"
    url = 'http://211.103.136.242:8064/orders/'
    data = { "address":"1","pay_method":"1" }
    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1ODg0MDc0MTUsInVzZXJuYW1lIjoicHl0aG9uIiwiZW1haWwiOiI5NTI2NzM2MzhAcXEuY29tIiwidXNlcl9pZCI6MX0.9vLuVHskV89xPDKy4EvhGNqULD1c5ciHFRIHyKH-29U'
    headers = {
        'Authorization': 'JWT ' + token
    }
    # 2、请求
    # r = requests.post(url,json=data,headers=headers)
    r = requests_post(url,json=data,headers=headers)
    # 3、结果
    # print(r.json())
    print(r)

if __name__ == "__main__":
    # test_login()
    # info()
    # goods_list()
    # cart()
    # order()

    # 1、根据默认运行原则，调整py文件命名，函数命名
    # 2、pytest.main()运行，或者命令行直接pytest运行
    pytest.main(["Test_Mall.py"])
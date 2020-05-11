#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# author:laobai
# datetime:2020/5/1 09:18
import requests
from utils.LogUtil import my_log
# GET方法封装
# 1、创建封装get方法
def requests_get(url,headers=None):
    # 2、 发送requests get请求
    r = requests.get(url,headers=headers)
    # 3、获取结果相应内容
    code = r.status_code
    try:
        body = r.json()
    except Exception as e:
        body = r.text
    # 4、内容存到字典
    res = dict()
    res['code'] = code
    res['body'] = body
    # 5、字典返回
    return res

# POST方法封装
# 1、创建post封装方法
def requests_post(url,json=None,headers=None):
    # 2、发送requests post请求
    r = requests.post(url,json=json,headers=headers)
    # 3、获取结果相应内容
    code = r.status_code
    try:
        body = r.json()
    except Exception as e:
        body = r.text
    # 4、内容存到字典
    res = dict()
    res['code'] = code
    res['body'] = body
    # 5、字典返回
    return res

# 重构
# 1、创建类
class Request:
    def __init__(self):
        self.log = my_log("Requests")
    # 2、定义公共方法
    def requests_api(self,url,data=None,json=None,headers=None,cookies=None,method='get'):
        # 增加方法的参数，根据参数来验证方法get/post方法请求
        if method == 'get':
            self.log.debug("发送get请求")
            r = requests.get(url,data=data,json=json,headers=headers,cookies=cookies)
        elif method == 'post':
            self.log.debug("发送post请求")
            r = requests.post(url,data=data,json=json,headers=headers,cookies=cookies)

        # 获取结果相应内容
        code = r.status_code
        try:
            body = r.json()
        except Exception as e:
            body = r.text
        # 内容存到字典
        res = dict()
        res['code'] = code
        res['body'] = body
        # 字典返回
        return res
    # 3、重构get/post方法
    # get
    def get(self,url,**kwargs):
        return self.requests_api(url,method='get',**kwargs)

    # post
    def post(self,url,**kwargs):
        return self.requests_api(url,method='post',**kwargs)
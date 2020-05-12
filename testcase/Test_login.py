#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# author:laobai
# datetime:2020/5/3 11:36
from config import Conf
import os,pytest
from utils.YamlUtil import YamlReader
from config.Conf import ConfigYaml
from utils.RequestsUtil import Request
# 1、获取测试用例内容
# 获取testlogin.yml文件路径
test_file = os.path.join(Conf.get_data_path(),'testlogin.yml')
# 使用工具类读取多个文档内容
data_list = YamlReader(test_file).data_all()
# 2、参数化执行用例

@pytest.mark.parametrize('login',data_list)
def test_yaml(login):
    # 初始化url，data
    url = ConfigYaml().get_conf_url() + login['url']
    data = login['data']
    # post请求
    request = Request()
    res = request.post(url,json=data)

if __name__ == "__main__":
    pytest.main(['-s','Test_login.py'])
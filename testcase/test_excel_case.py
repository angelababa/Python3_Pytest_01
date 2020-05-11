#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# author:laobai
# datetime:2020/5/3 15:14
from config.Conf import ConfigYaml
import os,json,pytest,allure
from common.ExcelData import Data
from utils.LogUtil import my_log
from common import ExcelConfig
from utils.RequestsUtil import Request
from common import Base
from utils.AssertUtil import AssertUtil
from common.Base import init_db
from config import Conf

# 1、初始化信息
# 1.1、初始化测试用例文件
case_file = os.path.join("../data",ConfigYaml().get_execl_file())
# 1.2、测试用例sheet名称
sheet_name = ConfigYaml().get_execl_sheet()
# 1.3、获取运行测试用例列表
data_init = Data(case_file,sheet_name)
run_list = data_init.get_run_data()
# 1.4、日志
log = my_log()
# 初始化dataconfig
data_key = ExcelConfig.DataConfig
# 2、测试用例方法，参数化运行
# 一个用例的运行
class TestExcel:

    def run_api(self,url,method,params=None,header=None,cookie=None):
        """
        发送请求api
        :return:
        """
        request = Request()
        if len(str(params).strip()) is not 0:
            params = json.loads(params)
        if str(method).lower() == "get":
            # 增加Headers和cookies
            res = request.get(url, json=params, headers=header, cookies=cookie)
        elif str(method).lower() == "post":
            res = request.post(url, json=params, headers=header, cookies=cookie)
        else:
            log.error("错误请求method: %s" % method)
        return res


    def run_pre(self,pre_case):
        url = ConfigYaml().get_conf_url() + pre_case[data_key.url]
        method = pre_case[data_key.method]
        params = pre_case[data_key.params]
        headers = pre_case[data_key.headers]
        cookies = pre_case[data_key.cookies]

        # 判断headers是否存在，json转义
        # if headers:
        #     header = json.loads(headers)
        # else:
        #     header = headers
        header = Base.json_parse(headers)
        # 增加cookies
        # if cookies:
        #     cookie = json.loads(cookies)
        # else:
        #     cookie = cookies
        cookie = Base.json_parse(cookies)
        res = self.run_api(url,method,params,header,cookie)
        print("前置用例执行：%s"%res)
        return res

    # a、初始化信息，url，data
    @pytest.mark.parametrize('case',run_list)
    def test_run(self,case):
        # data_key = ExcelConfig.DataConfig
        # run_list第一个用例
        url = ConfigYaml().get_conf_url() + case[data_key.url]
        # print(url)
        case_id = case[data_key.case_id]
        case_model = case[data_key.case_model]
        case_name = case[data_key.case_name]
        pre_exec = case[data_key.pre_exec]
        method = case[data_key.method]
        params_type = case[data_key.params_type]
        params = case[data_key.params]
        expect_result = case[data_key.expect_result]
        headers = case[data_key.headers]
        cookies = case[data_key.cookies]
        code = case[data_key.code]
        db_verify = case[data_key.db_verify]

        # # 判断headers是否存在，json转义
        # if headers:
        #     header = json.loads(headers)
        # else:
        #     header = headers
        # # 增加cookies
        # if cookies:
        #     cookie = json.loads(cookies)
        # else:
        #     cookie = cookies

        # 验证前置条件
        if pre_exec:
            # 执行测试用例
            pre_case = data_init.get_case_pre(pre_exec)
            # print("前置条件为：%s"%pre_case)
            pre_res = self.run_pre(pre_case)
            headers,cookies = self.get_correlation(headers,cookies,pre_res)
        header = Base.json_parse(headers)
        cookie = Base.json_parse(cookies)
        res = self.run_api(url,method,params,header,cookie)
        print("测试用例执行：%s" % res)

        # allure
        '''
        sheet名称 feature 一级标签
        模块  story   二级标签
        用例ID+接口名称   title
        请求url、请求类型、期望结果、实际结果    描述
        '''
        allure.dynamic.feature(sheet_name)
        allure.dynamic.story(case_model)
        allure.dynamic.title(case_id + case_name)
        desc = "<font color='red'> 请求URL：</font> {} <Br/> " \
               "<font color='red'> 请求类型：</font> {} <Br/> " \
               "<font color='red'> 期望结果：</font> {} <Br/> " \
               "<font color='red'> 实际结果：</font> {} ".format(url,method,expect_result,res)
        allure.dynamic.description(desc)


        # 断言验证
        # 状态码，返回结果内容，数据库相关结果验证
        assert_util = AssertUtil()
        assert_util.assert_code((res['code']),int(code))
        # 返回结果内容，body
        assert_util.assert_in_body(str(res["body"]),str(expect_result))
        # 数据库断言
        Base.assert_db("db_1",res['body'],db_verify)
        # sql = init_db("db_1")
        # db_res = sql.fetchone(db_verify)
        # log.debug("数据库查询结果：{}".format(str(db_res)))
        # verify_list = dict(db_res).keys()
        # for line in verify_list:
        #     res_line = res['body'][line]
        #     res_db_line = dict(db_res)[line]
        #     assert_util.assert_body(res_line,res_db_line)


        # b、接口请求
        # request = Request()
        # if len(str(params).strip()) is not 0:
        #     params = json.loads(params)
        # if str(method).lower()=="get":
        #     # 增加Headers和cookies
        #     res = request.get(url,json=params,headers=header,cookies=cookie)
        # elif str(method).lower()=="post":
        #     res = request.post(url,json=params,headers=header,cookies=cookie)
        # else:
        #     log.error("错误请求method: %s"%method)
        # print(res)

    def get_correlation(self,headers,cookies,pre_res):
        headers_para,cookies_para = Base.params_find(headers,cookies)
        if len(headers_para):
            headers_data = pre_res["body"][headers_para[0]]
            headers =Base.res_sub(headers,headers_data)
        if len(cookies_para):
            cookies_data = pre_res["body"][cookies_para[0]]
            cookies = Base.res_sub(cookies,cookies_data)
        return headers,cookies


if __name__ == '__main__':
    report_path = Conf.get_report_path() + os.sep + 'report'
    report_html_path = Conf.get_report_path() + os.sep + 'html'
    pytest.main(['-s','test_excel_case.py','--alluredir',report_path])
    Base.allure_report(report_path,report_html_path)
    Base.send_mail(title="接口测试报告结果",content=report_html_path)



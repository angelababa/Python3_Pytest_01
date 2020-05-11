#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# author:laobai
# datetime:2020/5/1 15:54
import os
from utils.YamlUtil import YamlReader
# 1.获取项目基本目录
# 获取当前项目的绝对路径
current = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(os.path.dirname(current))
# 定义config目录的路径
_config_path = BASE_DIR + os.sep + "config"
# 定义data目录的路径
_data_path = BASE_DIR + os.sep + "data"
# 定义conf.yml文件的路径
_config_file = _config_path + os.sep + 'conf.yml'

# 定义db_conf.yml文件的路径
_db_config_file = _config_path + os.sep + 'db_conf.yml'

# 定义logs文件路径
_log_path = BASE_DIR +os.sep + "logs"

# 定义report目录的路径
_report_path = BASE_DIR + os.sep + "report"

def get_config_path():
    return _config_path

def get_data_path():
    return _data_path

def get_config_file():
    return _config_file

def get_db_config_file():
    return _db_config_file

def get_log_path():
    return  _log_path

def get_report_path():
    """
    获取report绝对路径
    :return:
    """
    return _report_path

# 2.读取配置文件
# 创建类
class ConfigYaml:
    # 初始yaml读取配置文件
    def __init__(self):
        self.config = YamlReader(get_config_file()).data()
        self.db_config = YamlReader(get_db_config_file()).data()
    # 定义方法获取需要的信息
    def get_conf_url(self):
        return self.config["BASE"]["test"]["url"]

    def get_conf_log(self):
        return  self.config["BASE"]["log_level"]

    def get_conf_extension(self):
        return  self.config["BASE"]["log_extension"]

    # 获取测试用例excel名称
    def get_execl_file(self):
        return self.config["BASE"]["test"]["case_file"]

    # 获取测试用例所在sheet名
    def get_execl_sheet(self):
        return self.config["BASE"]["test"]["case_sheet"]

    def get_db_conf_info(self,db_alias):
        """
        根据db_alias获取该名称下的数据库信息
        """
        return self.db_config[db_alias]

    def get_email_info(self):
        """
        获取邮件配置相关信息
        :return:
        """
        return self.config['email']

if __name__ == "__main__":
    conf_read = ConfigYaml()
    # print(conf_read.get_conf_url())
    # print(conf_read.get_conf_log())
    # print(conf_read.get_conf_extension())
    # print(conf_read.get_db_conf_info("db_2"))
    # print(conf_read.get_execl_file())
    # print(conf_read.get_execl_sheet())
    print(conf_read.get_email_info())
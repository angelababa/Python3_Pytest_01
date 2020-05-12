#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# author:laobai
# datetime:2020/5/1 01:38
import os
import pytest
from config import Conf

if __name__ == '__main__':
    report_path = Conf.get_report_path() + os.sep + 'report'
    report_html_path = Conf.get_report_path() + os.sep + 'html'
    pytest.main(['-s','--alluredir',report_path])

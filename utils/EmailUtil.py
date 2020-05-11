#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# author:laobai
# datetime:2020/5/9 22:33
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config.Conf import ConfigYaml
import smtplib
# 初始化
# —— smtp地址，用户名，密码，接收者邮箱，邮件标题，邮件内容，邮件附件
class SendEmail:
    def __init__(self,smtp_address,username,password,
                 receiver,title,content=None,file=None):
        self.smtp_address = smtp_address
        self.username = username
        self.password = password
        self.receiver = receiver
        self.title = title
        self.content = content
        self.file = file

    # 发送邮件方法
    def send_mail(self):
        # MIME
        msg = MIMEMultipart()
        # 初始化邮件信息
        msg.attach(MIMEText(self.content,_charset='utf-8'))
        msg['Subject'] = self.title
        msg['From'] = self.username
        msg['To'] = self.receiver
        # 邮件附件
        # 判断是否有附件
        if self.file:
            # MIMEText读取文件
            att = MIMEText(open(self.file).read())
            # 设置内容类型
            att["Content-Type"] = 'application/octet-stream'
            # 设置附件头
            att["Content-Disposition"] = 'attachment;filename="%s"'%self.file
            # 将内容附加到邮件主体中
            msg.attach(att)
        # 登录邮件服务器
        self.smtp = smtplib.SMTP(self.smtp_address,port=25)
        self.smtp.login(self.username,self.password)
        # 发送邮件
        self.smtp.sendmail(self.username,self.receiver,msg.as_string())


if __name__ == "__main__":
    # 初始化类
    email_info = ConfigYaml().get_email_info()
    smtp_address = email_info['smtpserver']
    username = email_info['username']
    password = email_info['password']
    receiver = email_info['receiver']
    email = SendEmail(smtp_address,username,password,receiver,"测试")
    email.send_mail()
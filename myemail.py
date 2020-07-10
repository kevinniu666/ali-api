# -*- coding: utf-8 -*-
# Author: Kevin Liu
# @Time: 2020/5/8 17:29
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from email.header import Header


def mail(to, subject, body, attachment=None):
    # 构造邮件内容
    sender = 'ops@163.com'#更换你自己的邮箱
    sender_password = 'password'#更换你自己的邮箱密码
    message = MIMEMultipart()
    message['From'] = formataddr(['运维组', sender])
    message['To'] = Header(','.join(to), 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')
    message.attach(MIMEText(body))
    if attachment:
        if os.path.isfile(attachment):
            attachment_path = os.path.basename(attachment)
            attachment_content = MIMEText(open(attachment, 'rb').read(), 'base64', 'utf-8')
            attachment_content['Content-Type'] = 'application/octet-stream'
            attachment_content.add_header('Content-Disposition', 'attachment', filename=('gbk', '', attachment_path))
            message.attach(attachment_content)
        else:
            print("附件错误")
            return "附件读取错误"
    try:
        server = smtplib.SMTP_SSL('smtp.163.com', 465)  # 这个邮箱SMTP服务器和使用的发送邮箱匹配
        server.login(sender, sender_password)
        server.sendmail(sender, to, message.as_string())
    except Exception as e:
        print("发送邮件失败")
    finally:
        server.quit()

if __name__=='__main__':

    current_path = os.path.abspath('.')
    attachment = os.path.join(current_path, 'pie.xlsx')
    receiver = ['user@163.com', '12345678@qq.com']
    subject = '[告警]mha已经迁移到另外一个节点'
    body = 'mha已经迁移到另外一个节点'
    mail(receiver, subject, body)

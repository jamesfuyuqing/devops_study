#!/usr/bin/env python
#_*_coding:utf-8_*_

import yagmail
import sys

def send_mail(to_address,subject,content):
    smtp_server = "smtp.exmail.qq.com"
    mail_user = "monitor@ou.com"
    mail_password = "abc2345"
    try:
        smtp_object = yagmail.SMTP(user=mail_user,password=mail_password,host=smtp_server)
        result = smtp_object.send(to_address,subject,content)
        if result == {}:
            return "send success"
    except Exception,e:
        return "smtp server connect error:", e
    finally:
        smtp_object.close()

if __name__ == '__main__':
    to_address = "fuyuqing@163.com"
    subject = "test"
    content = "this is test mail"
    print send_mail(to_address,subject,content)
    # send_mail(sys.argv[1],sys.argv[2],sys.argv[3])
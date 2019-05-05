#!/usr/bin/env python
#_*_coding:utf-8_*_
__author__ = 'FYQ'
import time
import os
import sys
from call_aliyun_sms import AliyunSms
from get_ip import getip
from yagmail_demo import send_mail
import json

class ErrorLog(object):
    def __init__(self,fileLocation,fileSeek=0):
        '''
        初始化两个参数
        :param fileLocation: 要监控的文件位置
        :param fileSeek:  上一次监控的文件指针，默认为从该文件的开头
        '''
        self.fileObject = open(fileLocation,'r')
        self.fileSeek = fileSeek

    def checkError(self):
        '''
        创建对应错误日志的文件对象，seek到上次检测到的文件位置使用readline
        :return: 返回错误行的一个集合列表
        '''
        errorLogList = []
        self.fileObject.seek(self.fileSeek)
        for line in self.fileObject.readlines():
            if 'MISS_FATAL_EXCEPTION' in line:   #此处添加日志筛选条件
                errorLogList.append(line.strip())
        return errorLogList

    def getFileSeek(self):
        '''
        record the file seek.
        :return:
        '''
        fileNowSeek = self.fileObject.tell()
        self.fileObject.close()
        return fileNowSeek

def callSms(fileName,address,phone_number):
    '''
    call the aliyun sms service to developer user phone number.
    :return:
    '''
    aliyun_sms = AliyunSms()
    aliyun_sms.set_params(fileName,address)
    result = aliyun_sms.send_sms(phone_number)
    return result

def callMail(business,host,to_address):
    '''
    This method is used to call the mailbox interface to send an alarm message.
    '''
    subject = "错误日志报警"
    content = "%s正在报警，\n报警主机：%s\n报警关键字：MISHOU_FATAL_EXCEPTION.\n请尽快处理" % (business,host)
    result = send_mail(to_address,subject,content)
    return result

def main():
    '''
    /tmp/monitor_dir/errorlog/ 此目录需自行创建：
            mkdir -p /tmp/monitor_dir/errorlog/
    :return:
    '''
    work_dir = "/tmp/monitor_dir/errorlog/"
    if os.path.exists(work_dir):
        pass
    else:
        print "请先创建"+work_dir
        sys.exit(1);

    now = time.strftime("%Y-%m-%d",time.localtime(time.time()))
    fileLocation = '/usr/local/nginx/logs/host.access.log'
    file_size = os.stat(fileLocation)[6]

    try:
        fileSeek = open(work_dir + now + '.txt', 'r')
    except IOError:
        fileSeek = open(work_dir + now + '.txt', 'w')
        fileSeek.close()
        fileSeek = open(work_dir + now + '.txt', 'r')
        
    fileSeekRead = fileSeek.read().strip()
    
    if fileSeekRead:
        if file_size == int(fileSeekRead):  #与上次相比相等，说明日志没有变化
            print "无输出"
            sys.exit(0);
        elif file_size > int(fileSeekRead): #当前size比上次大，说明有输出
            errorLog = ErrorLog(fileLocation,int(fileSeekRead))
            print "日志有刷新内容，向下监控。"
        else:          #否则说明日志被清空或更换了文件句柄，所以将位置重置为 0
            errorLog = ErrorLog(fileLocation)
            print "日志被清空或更换文件句柄，从头开始。"
    else:
        errorLog = ErrorLog(fileLocation)

    fileSeek.close()

    fileSeek = open(work_dir + now + '.txt', 'w')
    errMessage = errorLog.checkError()
    fileSeek.write(str(errorLog.getFileSeek()))
    fileSeek.close()
    mobile_list = ["你的电话","总监的电话"] #此处添加要接收短信的手机号
    mail_list = ["你的邮箱","总监的邮箱"] #此处添加要接收报警的邮箱账号
    result_dict = {}
    if errMessage:
        local_ip  = getip("eth0").split('.')
        local_ip = local_ip[-2] + '.' + local_ip[-1]
        fileLocation_format = fileLocation.split('/')
        fileLocation_format = fileLocation_format[-2] + '的业务日志'
        for mail in mail_list:
            result = callMail(fileLocation_format,local_ip,mail)
            if result:
                print "send mail to %s success" % mail
        for phone in mobile_list:
            sms_result = callSms(fileLocation_format,local_ip,phone)
            status = json.loads(sms_result)["Code"]
            result = [{"send_sms":status,"error_log":errMessage}]
            result_dict[phone] = result
        return json.dumps(result_dict)
    else:
        return

if __name__ == '__main__':
    print main()

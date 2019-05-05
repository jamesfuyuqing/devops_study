#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from aliyunsdkcore.client import AcsClient
import uuid
from aliyunsdkcore.profile import region_provider

reload(sys)
sys.setdefaultencoding("utf8")

class AliyunSms(object):
    def __init__(self):
        self._REGION = "cn-beijing"
        self._PRODUCT_NAME = "Dysmsapi"
        self._DOMAIN = "dysmsapi.aliyuncs.com"

        # ACCESS_KEY_ID/ACCESS_KEY_SECRET 根据实际申请的账号信息进行替换
        self._ACCESS_KEY_ID = "this is api key"
        self._ACCESS_KEY_SECRET = "this is api key secret code"
        self._TEMPLATE_CODE = "this is sms template"
        self._SIGN_NAME = "阿里云短信测试专用"
        self.acs_client = AcsClient(self._ACCESS_KEY_ID, self._ACCESS_KEY_SECRET, self._REGION)
        region_provider.add_endpoint(self._PRODUCT_NAME,self._REGION,self._DOMAIN)
        self._business_id = uuid.uuid1()
        self.params = None

    def set_params(self,filename,ip_address):
        '''This method be use for params join.
            note: char size cannot gt 20.
        '''
        self.params = "{\"filename\":\""+filename+"\",\"ip_address\":\""+ip_address+"\"}"
        print self.params
        return self.params

    def send_sms(self,phone_number):
        smsRequest = SendSmsRequest.SendSmsRequest()
        # 申请的短信模板编码,必填
        smsRequest.set_TemplateCode(self._TEMPLATE_CODE)
        # 短信模板变量参数
        if self.params is not None:
            smsRequest.set_TemplateParam(self.params)
        # 设置业务请求流水号，必填。
        smsRequest.set_OutId(self._business_id)
        # 短信签名
        smsRequest.set_SignName(self._SIGN_NAME);
        # 短信发送的号码列表，必填。
        smsRequest.set_PhoneNumbers(phone_number)
        # 调用短信发送接口，返回json
        smsResponse = self.acs_client.do_action_with_exception(smsRequest)
        return smsResponse

if __name__ == '__main__':
    aliyun_sms = AliyunSms()
    aliyun_sms.set_params("test业务的错误日志","1.233")
    print aliyun_sms.send_sms("13333333333")

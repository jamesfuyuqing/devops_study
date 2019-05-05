#_*_coding:utf-8_*_

import os.path
import time

logpath = os.path.join(os.path.dirname(__file__),'logs')
date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

def log_define(logname,message):
    with open(logpath+'/'+logname,'a') as f:
        f.write(date+' '+message)

mysql_config = {
    'host':'10.0.0.2',
    'port':3306,
    'db':'monitor',
    'user':'root',
    'password':'123456'
}

mongo_config = {
    'host': '10.0.0.2',
    'port': 27017,
    'db' : 'hostinfo'
}

server_config = {
    'host': '10.0.0.3',
    'port': 8080
}
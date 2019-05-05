#_*_coding:utf-8_*_

import socket
import sys
import os
import time
import json
from Mongo_Story import mongo_Config

mongo = mongo_Config()
def log_define(logname,message):
    log_path = os.path.join(os.path.dirname(__file__),'logs')
    date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    with open(log_path+'/'+logname,'a') as f:
        f.write(date+' '+str(message)+'\n')

try:
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#    hostname = socket.gethostname()
    hostaddr = '10.0.0.3'
    port = 8080
    server.bind((hostaddr,port))
    server.listen(10)
except Exception,e:
    message = "Error Message: ",e
    log_define('socket.log',message)
    sys.exit();

print "server is run on %rs %r" % (hostaddr,port)

while True:
    conn,addr = server.accept()
    if conn:
        message = "connect by ",addr
        log_define('socket.log',message)
        data = conn.recv(2048)
        data = json.loads(data)
        print type(data)
        mongo.mongo_insert(addr[0],data)
        dic = {'name': addr[0]}
        print mongo.mongo_query(dic)
    conn.close()

server.close()

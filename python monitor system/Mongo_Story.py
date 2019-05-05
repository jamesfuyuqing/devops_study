#_*_coding:utf-8_*_

import pymongo
import sys
import os.path
import config
import time

class mongo_Config(object):
    def __init__(self):
        conn = pymongo.MongoClient(config.mongo_config['host'],config.mongo_config['port'])
        self.db = conn[config.mongo_config['db']]
        self.logpath = os.path.join(os.path.dirname(__file__),'logs')

    def log_define(self,logname,message):
        date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        with open(self.logpath+'/'+logname,'a') as f:
            f.write(date+' '+str(message)+'\n')

    def mongo_insert(self,client_addr,data):
        try:
            coll = self.db.data_collection
            coll.insert_one({'name' : client_addr, 'data': data})
        except Exception as e:
            message = "Error Message: ",e
            self.log_define('mongodb.log',message)
            sys.exit();

    def mongo_query(self,find_data):
        try:
            coll = self.db.data_collection
            if find_data:
                return coll.find_one(find_data)
            else:
                message="Error Message: please insert a dict type!"
                self.log_define('mongodb.log',message)
                return  message
        except Exception as e:
            message="Error Message: ",e
            self.log_define('mongodb.log',message)
            sys.exit();

    def mongo_object(self):
        try:
            coll = self.db.data_collection
            return coll
        except Exception,e:
            return "Error Message: ",e

if __name__ == '__main__':
    mongo_config = mongo_Config()
    print mongo_config.mongo_object()
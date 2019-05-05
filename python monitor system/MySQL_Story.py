#_*_coding:utf-8_*_

import config
import MySQLdb as mysql
import sys
import os.path
import time

class db_Config(object):
    def __init__(self):
        host = config.mysql_config['host']
        port = config.mysql_config['port']
        db = config.mysql_config['db']
        user = config.mysql_config['user']
        password = config.mysql_config['password']
        self.conn = mysql.connect(host=host,port=port,user=user,passwd=password,db=db)
        self.logpath = os.path.join(os.path.dirname(__file__),'logs')

    def log_define(self,logname,message):
        date = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        with open(self.logpath+'/'+logname,'a') as f:
            f.write(date+' '+str(message))

    def db_model(self,sql):
        try:
            self.conn.autocommit(True)
            cursor = self.conn.cursor()
            sql = cursor.execute(sql)
            result = cursor.fetchmany(sql)
        except Exception as e:
            message = "Error Message", e
            self.log_define('mysql.log',message)
            sys.exit();
        self.log_define('mysql.log',result)
        return result

    def db_version(self):
        try:
            self.conn.autocommit(True)
            cursor = self.conn.cursor()
            sql = cursor.execute('select version()')
            result = cursor.fetchmany(sql)
        except Exception,e:
            return "Error Message: ",e
        return result

if __name__ == '__main__':
    db_config = db_Config()
    print db_config.db_version()

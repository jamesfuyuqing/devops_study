#_*_coding:utf-8_*_

from basic_token import Basic
import json
import requests
import gevent
import time
from gevent import monkey
monkey.patch_all()

class Host_get(Basic):
    def __init__(self):
        super(Host_get,self).__init__()
        self.tokenid = self.getToken()
        self.data = {
            "jsonrpc":"2.0",
            "method":"host.get",
            "params": {
                "output":["hostid","host"],
                "selectInterfaces":["interfaceid","ip"]
            },
            "id":2,
            "auth": self.tokenid
        }
        self.result_data = {}

    def getHost(self):
        host_dict = {}
        try:
            response = requests.post(url=self.url,json=self.data,headers=self.header)
        except Exception, e:
            return e
        for i in json.loads(response.text)['result']:
            host_dict[i['host']] = i['hostid']
        return host_dict

    def getHostItem(self,hostid,tokenid,hostname):
        data = {
            "jsonrpc":"2.0",
            "method":"item.get",
            "params": {
                "output": "extend",
                "hostids":hostid,
                "search":{
                    "key_":"vfs.fs.size"
                },
                "sortfied" : "name"
            },
            "auth":tokenid,
            "id":1
        }
        response = requests.post(url=self.url,json=data,headers=self.header)
        value = {}
        for i in json.loads(response.text)['result']:
            if 'pfree' in i['key_']:
                value[i['key_']] = i['lastvalue']
        self.result_data[hostname] = [value]
        return self.result_data

    @classmethod
    def run(cls):
        '''
        此方法使用gevent创建了相应的协程，并发了getHostItem()方法
        :return:
        '''
        cls = cls()
        tokenid = cls.tokenid
        hostmessage = cls.getHost()
        job_list = []
        for hostname, hostid in hostmessage.items():
            job_list.append(gevent.spawn(cls.getHostItem,hostid,tokenid,hostname))
        gevent.joinall(job_list)
        return json.dumps(cls.result_data,indent=3)

if __name__ == '__main__':
    host_get = Host_get()
    t1 = time.time()
    print Host_get.run()
    t2 = time.time()
    print "异步执行时间为：", t2 - t1

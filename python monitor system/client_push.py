#_*_coding:utf-8_*_

import socket
import sys
import config
import time
from sysinfo import SystemInfo

sys_info = SystemInfo()

class client_Push(object):
    def data_metrics(self):
        data = dict(
            cpu = sys_info.cpu(),
            memory = sys_info.memory(),
            swap = sys_info.swap(),
            disk = sys_info.disk(),
            network = sys_info.network(),
            load = sys_info.load()
        )
        return data

    def client_push(self):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((config.server_config['host'], config.server_config['port']))
        except Exception, e:
            message = "Error Message: ", e
            config.log_define('error.log', message)
            sys.exit()

        while True:
            try:
                client.sendall(self.data_metrics())
                data = client.recv(1024)
                if data == 1:
                    message = "send successfully!"
                    config.log_define('monitor.log',message)
                    break
                else:
                    time.sleep(2)
                    continue
            except Exception,e:
                message = "Error Message: ",e
                config.log_define('monitor.log',message)
                sys.exit();
        client.close()

if __name__ == '__main__':
    client = client_Push()
    client.client_push()
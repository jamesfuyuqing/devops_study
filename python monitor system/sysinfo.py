#_*_coding:utf-8_*_

from __future__ import division
import os
import sys

try:
    import psutil
except ImportError as e:
    print "Error Message: ",e
    sys.exit(1)

class SystemInfo(object):
    def cpu(self):
        #cpu percent metrics
        cpu_metrics = dict(
            user = psutil.cpu_times_percent().user,
            idle = psutil.cpu_times_percent().idle,
            nice = psutil.cpu_times_percent().nice,
            system = psutil.cpu_times_percent().system,
            iowait = psutil.cpu_times_percent().iowait
        )
        return cpu_metrics

    def memory(self):
        #memory percent metrics
        total = psutil.virtual_memory().total
        memory_metrics = dict(
            available = psutil.virtual_memory().available/total,
            used = psutil.virtual_memory().used/total
        )
        return memory_metrics

    def swap(self):
        #swap percent metrics
        total = psutil.swap_memory().total
        swap_metrics = dict(
            available = psutil.swap_memory().available/total,
            used = psutil.swap_memory().used/total
        )
        return swap_metrics

    def disk(self):
        #disk partitions mountpoint
        disk_result = psutil.disk_partitions()
        partition = [l.mountpoint for l in disk_result]
        disk_metrics = {}

        for i in partition:
            disk_metrics[i] = dict(
                total = psutil.disk_usage(i).total,
                used = psutil.disk_usage(i).used,
                free = psutil.disk_usage(i).free,
                percent = psutil.disk_usage(i).percent
            )

        disk_metrics['IOPS'] = dict(
            read_count = psutil.disk_io_counters().read_count,
            write_count = psutil.disk_io_counters().write_count,
            read_time = psutil.disk_io_counters().read_time,
            write_time = psutil.disk_io_counters().write_time
        )
        return disk_metrics

    def network(self):
        #network interface traffic metrics
        network_metrics = {}
        for k,v in psutil.net_if_stats().iteritems():
            if v.speed == 0:
                continue
            pernic = psutil.net_io_counters(pernic=True)[k]
            network_metrics[k] = dict(
                    bytes_sent = pernic.bytes_sent,
                    bytes_recv = pernic.bytes_recv
                )
        return network_metrics

    def load(self):
        #system load and uptime
        load_command = os.popen('uptime').read().strip().split(',')
        load_metrics = dict(
            load_1 = load_command[3].split(' ')[-1],
            load_5 = load_command[4],
            load_15 = load_command[5],
            uptime = load_command[0]
        )
        return load_metrics

    def system_version(self):
        #system version
        a = os.popen('cat /etc/issue').read()
        return a

if __name__ == '__main__':
    sysinfo = SystemInfo()
    print sysinfo.system_version()

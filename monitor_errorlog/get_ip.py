#!/usr/bin/python 
#_*_coding:utf-8_*_
import socket 
import struct 
import fcntl 

def getip(ethname): 
    s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    result = socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0X8915, struct.pack('256s', ethname[:15]))[20:24]) 
    s.close()
    return result

if __name__=='__main__': 
    print getip('ens37')

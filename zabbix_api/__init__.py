#!/usr/bin/env python3
#_*_coding:utf-8_*_
import pexpect
import sys

def ssh(host,password,command):
    host="101.201.116.97"
    password="aaa"
    command='ssh %s ls -l /opt/scripts/' % host
    try:
        process = pexpect.spawn(command, timeout=5)
        choice = process.expect(['password:','(yes/no)?'])
        with open('./pexpect_test2.log','awb') as f:
            if choice == 0:
                process.sendline("%s" % password)
            elif choice == 1:
                process.sendline("yes")
                process.expect("password:")
                process.sendline("%s" % password)
            process.expect('\w+')
            #process.sendeof()
            #process.readlines()
            process.expect(pexpect.EOF,timeout=None)
            print(process.before,process.after)
            sys.stdout.write(process.before)
            f.write(process.before)
    except Exception as e:
        print(e.message)
    finally:
        process.close()
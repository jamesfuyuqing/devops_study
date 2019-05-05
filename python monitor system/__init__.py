#_*_coding:utf-8_*_

import json
import os.path
import datetime

json_test = os.path.join(os.path.dirname(__file__),'json_test.txt')

a = dict(
    b = 1,
    c = 2,
    z = str(datetime.datetime.now())
)

d = json.dumps(a,indent=2,)
print d

try:
    with open(json_test,'w') as f:
        f.write(d)
except Exception,e:
    print "Error Message",e

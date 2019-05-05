#_*_coding:utf-8_*_
from flask import Flask,request,Response
from host_get_gevent import Host_get
import json


app = Flask(__name__)

def getData():
    data = Host_get.run()
    return data

@app.route('/')
def index():
    return getData()

@app.route('/get_list/')
def get_list():
    host_get = Host_get()
    return json.dumps(host_get.getHost(),indent=3)

@app.route("/metrics/find/  ")
def metrics():
    if request.args.get('query') == '*':
        return Response(getData())
    else:
        try:
            host = request.args.get("query")
            return Response(json.dumps(json.loads(getData())[host],indent=3))
        # elif request.args.get('query') == host:
        #     return json.loads(data)[host]
        except KeyError as e:
            return Response(json.dumps({"errorMsg":"KeyError:   The %s is not found" % host},indent=3))

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=11111,debug=True)
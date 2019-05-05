#_*_coding:utf-8_*_

import tornado.web
import tornado.options
import tornado.httpserver
import tornado.ioloop
import pymongo
import sys
import os.path
import config

from tornado.options import define,options

define('port',9000,type=int,help="run this given port")

class IndexHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        self.write('hello world')

class ApiHandler(tornado.web.RequestHandler):
    def post(self):
        self.write({'errmsg':'not found'})
        self.set_status(404)

class Application(tornado.web.Application):
    def __init__(self):
        try:
            conn = pymongo.MongoClient(config.mongo_config['host'],config.mongo_config['port'])
            self.db = conn[config.mongo_config['db']]
        except Exception,e:
            message = "Error Message: ",e
            config.log_define('tornado.log',message)
            sys.exit();
        handler = [
            (r'/', IndexHandler),
            (r'/json_api/v1/monitor',ApiHandler)
        ]
        setting = dict(
            template_path = os.path.join(os.path.dirname(__file__),'template_bak'),
            static_path = os.path.join(os.path.dirname(__file__),'static')
        )
        tornado.web.Application.__init__(self,handlers=handler,**setting)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = Application()
    httpserver = tornado.httpserver.HTTPServer(app)
    httpserver.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
# Tornado imports
import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define, options

from core.models import session
from urls import handlers

# Options
define("port", default=8000, help="run on the given port", type=int)
define("domain", default='vagrant.intra.douban.com:8000')


class Application(tornado.web.Application):

    def __init__(self):
        settings = dict(debug=options.debug, autoreload=True)
        tornado.web.Application.__init__(self, handlers, **settings)
        self.db = session

app = Application()

if __name__ == "__main__":
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

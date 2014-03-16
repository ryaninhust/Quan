# Tornado imports
import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.web
import yaml
from raven.contrib.tornado import AsyncSentryClient
from tornado.options import define, options

from core.models import session
from urls import handlers

# config
with open('app.yaml') as config_yaml:
    app_config = yaml.load(config_yaml)

# Options
define("port", default=8000, help="run on the given port", type=int)
define("domain", default='vagrant.intra.douban.com:8000')


class Application(tornado.web.Application):

    def __init__(self):
        settings = dict(debug=options.debug, autoreload=True)
        tornado.web.Application.__init__(self, handlers, **settings)
        self.db = session
        self.sentry_client = AsyncSentryClient(app_config['sentry'])

app = Application()

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

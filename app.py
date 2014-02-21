# Python imports


# Tornado imports
import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.web
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from tornado.options import define, options

from core.models.base import install_model
from urls import handlers

# Sqlalchemy imports

# App imports

# Options
define("port", default=8000, help="run on the given port", type=int)
define("debug", default=False, type=bool)
define("db_path", default='mysql://root:@localhost/simi', type=str)
#define("db_path", default='sqlite:////tmp/test.db', type=str)
define("domain", default='vagrant.intra.douban.com:8000')


class Application(tornado.web.Application):

    def __init__(self):
        settings = dict(
            debug=options.debug,
            autoreload=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)
        engine = create_engine(
            options.db_path, convert_unicode=True, echo=options.debug)
        install_model(engine)
        self.db = scoped_session(sessionmaker(bind=engine))

app = Application()

if __name__ == "__main__":
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

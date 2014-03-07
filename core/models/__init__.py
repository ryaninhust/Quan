from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from tornado.options import define, options

from core.models.base import install_model
from core.models.subjects import *

define("debug", default=False, type=bool)
define("db_path",
       default='mysql://root:@localhost/simi?charset=utf8', type=str)
# define("db_path", default='sqlite:////tmp/test.db', type=str)

engine = create_engine(
    options.db_path, convert_unicode=True, echo=options.debug)
install_model(engine)
session = scoped_session(sessionmaker(bind=engine))

__all__ = [engine, session]

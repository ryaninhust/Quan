from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer
from sqlalchemy.ext.declarative import AbstractConcreteBase, declarative_base

from tornado.options import options

Base = declarative_base()


def install_model(engine):
    """Sync model into database, Invoked from application
    """
    Base.metadata.create_all(bind=engine)
    print "Models Installed"


# Put your models here
class BaseModel(AbstractConcreteBase, Base):
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.now)
    is_archived = Column(Boolean, default=True)

    def __repr__(self):
        return '<%s: %d>' % (self.__class__.__name__, self.id)

    @property
    def url(self):
        return options.domain + '/%s/%d' % (self.__tablename__, self.id)

    @property
    def json(self):
        raise NotImplementedError

    def update(self, update_dict):
        [setattr(self, key, value) for key, value in update_dict.iteritems()]

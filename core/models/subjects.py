import hmac
import uuid
from hashlib import sha1

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import backref, relationship
from tornado.options import options

from core.models.base import BaseModel
from core.lib.time import datetime_to_unixtime


class User(BaseModel):
    __tablename__ = 'user'

    email = Column(String(100))
    password = Column(String(100))
    name = Column(String(100))
    description = Column(String(100))

    cell_phone = Column(String(15), index=True, unique=True)
    avatar_url = Column(String(100))
    first_login = Column(DateTime())

    last_login = Column(DateTime())
    is_active = Column(Boolean())
    access_token = Column(String(100))
    circles = association_proxy('membership', 'circles')

    @property
    def json(self):
        return {
            'url': self.url,
            'cell_phone': self.cell_phone,
            'email': self.email,
            'name': self.name,
            'description': self.description,
            'avatar_url': self.avatar_url,
            'circle_url': self.circles_url,
        }

    @property
    def circles_url(self):
        return "%s/cirlces/" % self.url

    def __init__(self, cell_phone, password):
        self.cell_phone = cell_phone
        self.generate_password(password)

    def check_password(self, password, encryption=lambda x: x):
        return encryption(password) == self.password

    def generate_password(self, password, encryption=lambda x: x):
        self.password = encryption(password)

    def generate_key(self):
        unique = uuid.uuid4()
        self.access_token = hmac.new(unique.bytes, digestmod=sha1).hexdigest()
        return self.access_token


class Circle(BaseModel):
    __tablename__ = 'circle'

    name = Column(String(100))
    description = Column(String(256))
    members = association_proxy('membership', 'member')

    @property
    def members_url(self):
        return "%s/members/" % self.url

    @property
    def json(self):
        return {
            'url': self.url,
            'name': self.name,
            'description': self.description,
            'members_url': self.members_url,
        }


class Membership(BaseModel):
    __tablename__ = 'membership'

    user_id = Column(Integer, ForeignKey('user.id'))
    circle_id = Column(Integer, ForeignKey('circle.id'))
    circle = relationship(Circle, backref=backref('membership'))
    member = relationship(User, backref=backref('membership'))
    status = Column(Integer)

    @property
    def url(self):
        return "%s/circle/%d/member/%d/" % (options.domain, self.circle_id,
                                            self.user_id)


class Status(BaseModel):
    __tablename__ = 'status'
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    circle_id = Column(Integer, ForeignKey('circle.id'), nullable=False)
    content = Column(String(240), nullable=False)
    user = relationship(User, backref=backref('status'))
    cirlce = relationship(Circle, backref=backref('status'))

    @property
    def url(self):
        return "%s/circle/%d/status/%d/" % (options.domain, self.circle_id,
                                            self.user_id)

    @property
    def json(self):
        return {
            'content': self.content,
            'user': self.user.url,
            'circle': self.cirlce.url,
            'timestamp': datetime_to_unixtime(self.timestamp),
        }

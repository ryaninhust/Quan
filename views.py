# -*- coding: utf-8 -*-
from datetime import datetime

from core import exceptions as local_exc
from core.views import AppHandler
from core.models.subjects import Circle, User, Status, Membership

from permissions import CirclePermission
import consts


class LoginHandler(AppHandler):

    def json_validate(self):

        self.validate_field_exist('cell_phone')
        self.validate_field_exist('password')

    def post(self):
        cell_phone = self.request_json['cell_phone']
        password = self.request_json['password']
        user = self.db.query(User).filter_by(cell_phone=cell_phone).first()
        if user:
            if user.check_password(password):
                user.last_login = datetime.now()
                user.access_token = user.generate_key()
                token_dict = {'access_token': user.access_token}
                self.db.commit()
                self.write(token_dict)
            else:
                raise local_exc.LoginError
        else:
            raise local_exc.UserNotExistError


class UserListHandler(AppHandler):

    def validate_post(self):
        self.validate_field_exist('cell_phone')
        self.validate_field_exist('password')

    def post(self):
        cell_phone = self.request_json['cell_phone']
        password = self.request_json['password']
        user = User(cell_phone=cell_phone, password=password)
        self.db.add(user)
        self.db.commit()
        token_dict = {'access_token': user.generate_key(),
                      'url': user.url}
        self.write(token_dict)

    def get(self):
        users = self.db.query(User).all()
        self.write({'list': [user.json for user in users]})


class UserDetailHandler(AppHandler):

    def prepare(self):
        super(UserDetailHandler, self).prepare()
        user_id = self.path_kwargs['uid']
        self.query_user = self.db.query(User).get(user_id)
        if not self.query_user:
            raise local_exc.UserNotExistError

    def get(self, **kwargs):
        self.write(self.query_user.json)

    def validate_put(self):
        valide_keys = ['password', ]
        self.validate_fields_scope(self.request_json.keys(), valide_keys)

    def put(self, **kwargs):
        password = self.request_json.get('password', None)
        if password:
            self.query_user.generate_password(password)
            del self.request_json['password']
        self.query_user.update(self.request_json)
        self.db.commit()
        self.write(self.query_user.json)


class CircleListHandler(AppHandler):

    def validate_post(self):
        self.validate_field_exist('name')
        self.validate_field_exist('description')

    def get(self):
        circles = self.db.query(Circle).all()
        self.write({'list': [circle.json for circle in circles]})

    def post(self):
        name = self.request_json['name']
        description = self.request_json['description']
        circle = Circle(name=name, description=description)
        self.db.add(circle)
        membership = Membership(member=self.current_user, circle=circle)
        membership.status = consts.ACCEPTED
        self.db.add(membership)
        self.write(circle.json)
        self.db.commit()


class CircleHandler(AppHandler):

    def prepare(self):
        cirlce_id = self.path_kwargs['cid']
        self.query_circle = self.db.query(Circle).get(cirlce_id)
        if not self.query_circle:
            raise local_exc.CircleNotExistError
        super(CircleHandler, self).prepare()


class CircleDetailHandler(CircleHandler):

    permission_class = CirclePermission

    def get(self, **kwargs):
        self.write(self.query_circle.json)

    def validate_put(self):
        valide_keys = ['name', 'description']
        self.validate_fields_scope(self.request_json.keys(), valide_keys)

    def put(self, **kwargs):
        self.query_circle.update(self.request_json)
        self.db.commit()
        self.write(self.query_circle.json)


class CircleStatusHandler(CircleHandler):

    def get(self, **kwargs):
        self.write({'list': [
                   status.json for status in self.query_circle.status]})

    def validate_post(self):
        self.validate_field_exist('content')

    def post(self, **kwargs):
        status = Status(content=self.request_json['content'])
        status.user = self.current_user
        status.cirlce = self.query_circle
        self.db.add(status)
        self.db.commit()
        self.write(status.json)


class CircleMemberHandler(CircleHandler):

    permission_class = CirclePermission

    def get(self, **kwargs):
        self.write({'list': [user.json for user in self.query_circle.members]})

    def validate_post(self):
        self.validate_field_exist('member_id')
        valide_keys = ['member_id', ]
        self.validate_fields_scope(self.request_json.keys(), valide_keys)

    def post(self, **kwargs):
        new_member = self.db.query(User).get(self.request_json['member_id'])
        if not new_member:
            raise local_exc.UserNotExistError
        membership = Membership(member=new_member, circle=self.query_circle)
        membership.status = consts.WATING_ACCEPT
        self.db.add(membership)
        self.db.commit()
        self.write(membership.json)


class CircleMemberDetailHandler(CircleHandler):

    permission_class = CirclePermission

    def prepare(self):
        query_dict = {'user_id': self.path_kwargs['mid'],
                      'circle_id': self.path_kwargs['cid']}

        self.membership = self.db.query(Membership).filter_by(**query_dict).first()
        if not self.membership:
            raise local_exc.MembershipNotExistError

        super(CircleMemberDetailHandler, self).prepare()

    def get(self, **kwargs):
        self.write(self.membership.json)

    def validate_put(self):
        self.validate_field_exist('status')
        valide_keys = ['status', ]
        self.validate_fields_scope(self.request_json.keys(), valide_keys)

    def put(self, **kwargs):
        self.membership.update(self.request_json)
        self.db.commit()
        self.write(self.membership.json)

# -*- coding: utf-8 -*-
from datetime import datetime

import consts
from core import exceptions as local_exc
from core.models.subjects import (
    Circle,
    Discussion,
    Membership,
    OauthToken,
    Status,
    User
)
from core.views import AppHandler
from permissions import CirclePermission


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
                user.generate_key()
                self.db.commit()
                token_dict = {'access_token': user.access_token}
                self.write(token_dict)
            else:
                raise local_exc.LoginError
        else:
            raise local_exc.UserNotExistError


class ThirdPartLoginHandler(AppHandler):

    def json_validate(self):
        self.validate_field_exist('oauth_token')
        self.validate_field_exist('token_type')
        self.validate_field_exist('third_uid')

        valide_keys = ['oauth_token', 'token_type', 'third_uid']
        self.validate_fields_scope(self.request_json.keys, valide_keys)

    def post(self):
        uid = self.request_json['third_uid']
        token_type = self.request_json['token_type']
        query_dict = {"uid": uid, token_type: 'token_type'}
        token = self.db.query(OauthToken).filter_by(**query_dict).first()

        if not token:
            user = User()
            self.db.add(user)
            token = OauthToken(user=user, **self.request_json)
            self.db.add(token)

        token.user.last_login = datetime.now()
        token.user.generate_key()
        self.db.commit()
        self.write({'access_token': token.user.access_token})


class UserListHandler(AppHandler):

    def validate_post(self):
        valide_keys = ['cell_phone', 'password']
        self.validate_fields_scope(self.request_json.keys(), valide_keys)

    def post(self):
        user = User(**self.request_json)
        self.db.add(user)
        self.db.commit()

        token_dict = {'access_token': user.generate_key(), 'url': user.url}
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
        valide_keys = ['password', 'loc_uid', 'last_login']
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

        self.membership = self.db.query(
            Membership).filter_by(**query_dict).first()
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


class StatusHandler(AppHandler):

    def prepare(self):
        status_id = self.path_kwargs['sid']
        self.query_status = self.db.query(Status).get(status_id)
        if not self.query_status:
            raise local_exc.StatusNotExistError
        super(StatusHandler, self).prepare()


class StatusDiscussionListHandler(StatusHandler):

    def get(self, **kwargs):
        self.write({'list': [d.json for d in self.query_status.discussions]})

    def validate_post(self):
        self.validate_field_exist('user_id')
        self.validate_field_exist('content')
        valide_keys = ['user_id', 'content']
        self.validate_fields_scope(self.request_json.keys(), valide_keys)

    def post(self, **kwargs):
        discussion = Discussion(**self.request_json)
        discussion.status = self.query_status
        self.db.add(discussion)
        self.db.commit()
        self.write(discussion.json)

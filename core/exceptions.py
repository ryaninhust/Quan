# -*- coding: utf-8 -*-
import json

from sqlalchemy.orm.exc import NoResultFound
from tornado.web import HTTPError


class AppException(HTTPError):

    """App exception base class
    """

    def __init__(self, status, end_message, dev_message=None, error_code=None):
        error_message = {
            'dev_message': dev_message,
            'end_message': end_message,
            'error_code': error_code,
            }
        log_message = json.dumps(error_message)
        HTTPError.__init__(self, status, log_message)


class UserNotExistError(AppException):

    def __init__(self, *args, **kwargs):
        AppException.__init__(self, 400, '用户不存在')


class CircleNotExistError(AppException):

    def __init__(self, *args, **kwargs):
        AppException.__init__(self, 400, '圈子不存在')


class MembershipNotExistError(AppException):

    def __init__(self, *args, **kwargs):
        AppException.__init__(self, 404, '关系不存在')


class AuthError(AppException):

    def __init__(self, *args, **kwargs):
        AppException.__init__(self, 401, '权限认证失败')


class LoginError(AppException):

    def __init__(self, *args, **kwargs):
        AppException.__init__(self, 401, '登录密码错误')


class PermissionError(AppException):

    def __init__(self, *args, **kwargs):
        AppException.__init__(self, 403, '没有权限访问')

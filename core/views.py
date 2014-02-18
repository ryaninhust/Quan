import sys
import traceback
from core import exceptions as local_exc
from core.permissions import BasePermission
from tornado.web import RequestHandler

from core.models.subjects import User
from core.mixins import JsonRequestResponseMixin


class BaseHandler(RequestHandler):

    permission_class = BasePermission

    def initialize(self):
        """Initalize db as property
        """
        self.db = self.application.db

    def get_current_user(self):
        """Get request user from 'Authorization' header
        If got a valid user, return it, otherwise return None
        """
        access_token = self.request.headers.get('Authorization', None)

        if not access_token:
            raise local_exc.AuthError

        try:
            return self.db.query(User).filter_by(
                access_token=access_token).one()
        except local_exc.NoResultFound:
            return None

    def prepare(self):
        self.check_permission()

    def check_permission(self):
        """Check permission, if premission denied this request,
        will raise a premission error
        """
        permission = self.permission_class(self)
        if not permission.check_permission():
            raise local_exc.PermissionError

    def _handle_request_exception(self, e):
        """Handlle uncaught exceptions
        """
        self.db.rollback()
        print traceback.format_exc()
        self.log_exception(*sys.exc_info())
        if self._finished:
            return
        if isinstance(e, local_exc.AppException):
            self.set_status(e.status_code)
            self.finish(e.log_message)
        else:
            self.send_error(500, exc_info=sys.exc_info())

    def on_finish(self):
        """Do something before done
        """
        self.db.close()


class AppHandler(BaseHandler, JsonRequestResponseMixin):

    """Application main Handler
    """

    def prepare(self):
        BaseHandler.prepare(self)
        JsonRequestResponseMixin.prepare(self)
        RequestHandler.prepare(self)

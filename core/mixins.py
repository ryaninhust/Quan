# -*- coding: utf-8 -*-
import json

from tornado.web import HTTPError


class JsonRequestError(HTTPError):

    def __init__(self, error_message, *args, **kwargs):
        super(JsonRequestError, self).__init__(400, error_message)


class JsonValidateMessagesMixin(object):
    default_error_message = ''

    def validate_field_exist(self, key):
        value = self.request_json.get(key, None)
        if not value:
            raise JsonRequestError("%s is required" % key)

    def validate_fields_scope(self, json_keys, valide_keys):
        if set(json_keys) - set(valide_keys):
            raise JsonRequestError("Invalide key included")

    def validate_post(self):
        pass

    def validate_put(self):
        pass

    def json_validate(self, request_method):
        validate_method = getattr(self, request_method)
        validate_method()


class JsonRequestResponseMixin(JsonValidateMessagesMixin):

    """
    Extends JSONResponseMixin.  Attempts to parse request as JSON.  If request
    is properly formatted, the json is saved to self.request_json as a Python
    object.  request_json will be None for imparsible requests.
    Set the attribute require_json to True to return a 400 "Bad Request" error
    for requests that don't contain JSON.

    Note: To allow public access to your view, you'll need to use the
    csrf_exempt decorator or CsrfExemptMixin.

    """

    error_response_message = 'Improperly formatted request'
    json_required = {'GET': False, 'POST': True,
                     'PUT': True, 'DELETE': False}

    def json_validate(self):
        pass

    def render_bad_request_response(self, error_dict=None):
        if error_dict is None:
            error_dict = self.error_response_dict
        self.set_status(400)
        self.finish(error_dict)

    def get_request_json(self):
        try:
            return json.loads(self.request.body)
        except ValueError:
            raise JsonRequestError(error_message=self.error_response_message)

    def prepare(self):
        if self.json_required[self.request.method]:
            self.request_json = self.get_request_json()
            self.json_validate()

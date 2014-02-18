class BasePermission(object):

    def __init__(self, handler, *args, **kwargs):
        self.request = handler.request
        self.handler = handler

    def check_permission(self):
        """Check method permission
        """
        method = getattr(self, self.request.method.lower())
        return method()

    def get(self):
        return True

    def post(self):
        return True

    def put(self):
        return True

    def delete(self):
        return True

from core.permissions import BasePermission


class CirclePermission(BasePermission):

    @property
    def is_member(self):
        return self.handler.current_user in self.handler.query_circle.members

    def get(self):
        return self.is_member

    def put(self):
        return self.is_member

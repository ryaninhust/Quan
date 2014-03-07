from datetime import datetime


def update_last_login(func):
    def check_update_user(self, *args, **kwargs):
        user = func(self, *args, **kwargs)
        if user:
            user.last_login = datetime.now()
            self.db.commit
        return user
    return check_update_user

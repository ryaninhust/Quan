from tornado.web import url

import views

handlers = [
    url(r'/login/', views.LoginHandler, name='login'),
    url(r'/user/', views.UserListHandler, name='users'),
    url(r'/user/(?P<uid>[0-9])/', views.UserDetailHandler, name='user_detail'),
    url(r'/circle/', views.CircleListHandler, name='circles'),
    url(r'/circle/(?P<cid>[0-9])/', views.CircleDetailHandler, name='circle_detail'),
    url(r'/circle/(?P<cid>[0-9])/status/', views.CircleStatusHandler, name='circle_status'),
    url(r'/circle/(?P<cid>[0-9])/member/', views.CircleMemberHandler, name='circle_members'),
    url(r'/circle/(?P<cid>[0-9])/member/(?P<mid>[0-9])/', views.CircleMemberDetailHandler, name='circle_member'),
    url(r'/status/(?P<sid>[0-9])/discussion/', views.StatusDiscussionListHandler, name='status_discussion'),
]

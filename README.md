Quan
====
A restful service demo using tornado &amp; sqlalchemy

##Quan Auth: 
使用Authorization header作为认证token交换方式 ```{'Authorization': token}```

##Quan API:

| API | Description          |
| ------------- | ----------- |
| /login      | 登录|
| /user/     | 复数用户信息     |
| /user/{id}/ | 单个用户信息 |
| /circle/ | 复数quan信息 |
| /circle/{id}/ | 单个quan信息 |
| /circle/{id}/status | 单个quan下面的复数circle信息|



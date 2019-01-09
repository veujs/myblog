from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'^login/$', views.user_login, name="user_login"),
    url(r'^logout/$', auth_views.logout,{"template_name":"account/logout.html"}, name="user_logout"),
    url(r'^register/$', views.register, name="user_register"),

    url(r'^password-change/$', auth_views.password_change,
        {"post_change_redirect":"/account/password-change-done",
         "template_name":"account/password_change_form.html"},
        name="password_change"),
    url(r'^password-change-done/$', auth_views.password_change_done,
        {"template_name":"account/password_change_done.html"},
        name="password_change_done"),

    # 相关密码修改的路由如下：利用内置的方法
    url(r'^password-reset/$', auth_views.password_reset,
        {"template_name": "account/password_reset_form.html",
         "email_template_name":"account/password_reset_email.html",
        "subject_template_name":"account/password_reset_subject.txt",
         "post_reset_redirect": "/account/password-reset-done"
         },
        name="password_reset"),

    url(r'^password-reset-done/$', auth_views.password_reset_done,
        {"template_name": "account/password_reset_done.html" },
        name="password_reset_done"),

    url(r'^password-reset-confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$', auth_views.password_reset_confirm,
        {"template_name": "account/password_reset_confirm.html",
         "post_reset_redirect":"/account/password-reset-complete"},
        name="password_reset_confirm"),

    url(r'^password-reset-complete/$', auth_views.password_reset_complete,
        {"template_name": "account/password_reset_complete.html"},
        name="password_reset_complete"),


    # 个人信息展示
    url(r'^my-information/$',views.myself,name="my_information"),

    # 个人信息添加
    url(r'^my-information-edit/$', views.myself_edit, name="my_information_edit"),

    # 头像添加
    url(r'^my-image/$', views.my_image, name="my_image"),
]



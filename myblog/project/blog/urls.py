from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    url(r'^index/$', views.index),
    url(r'^$',views.blog_title, name="blog_title"),
    url(r'(?P<article_id>\d)/$', views.blog_article, name="blog_article"),
]
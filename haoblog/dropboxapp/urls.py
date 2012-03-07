# coding=utf8

from django.conf.urls.defaults import *
from haoblog.dropboxapp import views

# Uncomment the next two lines to enable the admin:
#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('dropbox',

    url(r'^oauth_start/$', views.oauth_start, {}, name='oauth_start'),
    url(r'^oauth/$', views.dropbox_oauth, {}, name='dropbox_oauth'),
    url(r'^settings/$', views.dropbox_settings, {}, name='dropbox_settings'),

    url(r'^test/$', views.test, {}, name='test'),
    url(r'^check/(?P<para_name>[\w-]+)/(?P<para_value>[\w-]+)/$', views.check, {}, name='check'),



)

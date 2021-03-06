# coding=utf8

from django.conf.urls.defaults import *
#from django.views.generic.list_detail import object_list, object_detail
from haoblog.settings import MEDIA_ROOT

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Example:
    # (r'^haoblog/', include('haoblog.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    # Tiny-MCE 富文本编辑器js文件
    #(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': MEDIA_ROOT}),
    (r'^static_media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': MEDIA_ROOT}),

    # blog 展示
    (r'^blog/', include('haoblog.blog.urls')),


    # Dropbox
    (r'^dropbox/', include('haoblog.dropboxapp.urls')),

    # dropblog
    (r'^dropblog/', include('haoblog.dropblog.urls')),
)

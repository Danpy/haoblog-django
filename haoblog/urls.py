# coding=utf8

from django.conf.urls.defaults import *
#from django.views.generic.list_detail import object_list, object_detail

#from haoblog.blog import views
from haoblog import views
#from haoblog.blog.models import Entry, Tag, Catalog

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

'''
entry_list_info = {
        'queryset': Entry.objects.all(),
        'template_name': 'templates/index.html',
}

tag_list_info = {
        'queryset': Tag.objects.all(),
        'template_name': 'templates/index.html',
}'''

urlpatterns = patterns('',
    # Example:
    # (r'^haoblog/', include('haoblog.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    
    
    # (r'^test/$', views.test),
    # (r'^$', views.index),
    # (r'^blog/$', views.index),
    # (r'^blog/index/$', views.index),
    # (r'^blog/(?P<entry_title>[\w-]+)/$', views.entry_detail),
    # (r'^blog/category/(?P<category_name>[\w-]+)/$', views.category_detail),
    # (r'^blog/tag/(?P<tag_name>[\w-]+)/$', views.tag_detail),'''
    
    (r'^test/$', views.test),
    #(r'^$', views.index),


    # 首页与文章分页
    url(r'^blog/$', views.index, {}, name='index'),
    url(r'^blog/page/(?P<page_num>\d+)/$', views.index, {'is_page': True}, name='blog_page'),

    # 单篇文章浏览
    url(r'^blog/(?P<entry_title>[\w-]+)/$', views.entry_detail, {}, name='entry_detail'),

    # 分类目录与目录分页
    url(r'^blog/category/(?P<category_name>[\w-]+)/$', views.category_detail, {}, name='category_index'),
    url(r'^blog/category/(?P<category_name>[\w-]+)/page/(?P<page_num>\d+)/$', views.category_detail, {}, name='category_page'),

    # 标签与标签分页
    url(r'^blog/tag/(?P<tag_name>[\w-]+)/$', views.tag_detail, {}, name='tag_index'),
    url(r'^blog/tag/(?P<tag_name>[\w-]+)/page/(?P<page_num>\d+)/$', views.tag_detail, {}, name='tag_page'),
)

# coding=utf8

from django.conf.urls.defaults import *
from haoblog.blog import views
from haoblog.blog.feeds import LatestEntriesFeed

urlpatterns = patterns('blog',

    # 首页与文章分页
    url(r'^$', views.index, {}, name='index'),
    url(r'^page/(?P<page_num>\d+)/$', views.index, {'is_page': True}, name='blog_page'),

    # 单篇文章浏览
    url(r'^(?P<entry_title>[\w-]+)/$', views.entry_detail, {}, name='entry_detail'),

    # 提交文章评论
    url(r'^comment/add/$', views.add_comment, {}, name='add_comment'),

    # 分类目录与目录分页
    url(r'^category/(?P<category_name>[\w-]+)/$', views.category_detail, {}, name='category_index'),
    url(r'^category/(?P<category_name>[\w-]+)/page/(?P<page_num>\d+)/$', views.category_detail, {}, name='category_page'),

    # 标签与标签分页
    url(r'^tag/(?P<tag_name>[\w-]+)/$', views.tag_detail, {}, name='tag_index'),
    url(r'^tag/(?P<tag_name>[\w-]+)/page/(?P<page_num>\d+)/$', views.tag_detail, {}, name='tag_page'),

    # rss 输出
    (r'^latest/feed/$', LatestEntriesFeed()),
)

# coding=utf8

from django.contrib.syndication.views import Feed
from haoblog.blog.models import Entry

class LatestEntriesFeed(Feed):
    title = u'haoblog 最新文章'
    link = u'/latest/'
    description = u'haoblog 最新文章'
    
    def items(self):
        return Entry.objects.order_by('-time_published')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
    #    return item.content_preview
        return item.content

    #def link(self, item):
    #    return item.get_absolute_url()

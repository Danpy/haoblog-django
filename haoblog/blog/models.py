# coding=utf8

from datetime import datetime
from django.db import models
#from django.utils.encoding import iri_to_uri

# Create your models here.


STATUS_CHOICES = (
    (0, 'Draft'),
    (1, 'Published'),
)

class Tag(models.Model):
    #count = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return u'%s' % self.name
    
    @models.permalink
    def get_absolute_url(self):
        #return 'blog/tag/%s' % self.name
        return ('tag_index', (), {'tag_name': self.name})
'''
    def __init__(self, count, tags):
        if self.tags in Tag.objects.all():
            self.count += 1

    def save(self, *args, **kwargs):
        if self.tag in Tag.objects.all():
            self.count += 1
        super(Tag, self).save(*agrs, **kwargs)'''


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __unicode__(self):
        return u'%s' % self.name

    @models.permalink
    def get_absolute_url(self):
        #return '/blog/category/%s' % self.name
        return ('category_index', (), {'category_name': self.name})


class Entry(models.Model):
    title = models.CharField(max_length=100)
    _url_title = models.CharField(max_length=100, blank=True, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    content = models.TextField()
    author = models.ForeignKey('auth.User', related_name='entries')
    tags = models.ManyToManyField(Tag)
    catalog = models.ManyToManyField(Category, related_name='catalogues')

    time_created = models.DateTimeField(auto_now_add=True, blank=True, editable=False)
    time_modified = models.DateTimeField(auto_now=True, blank=True, null=True)
    time_published = models.DateTimeField(default=datetime.now, blank=False, null=False)

    @property
    def content_preview(self):
        '''文章预览，用于首页显示所有文章'''
        return self.content[ :len(self.content)/4]

    @property
    def url_title(self):
        if self._url_title:
            return self._url_title
        else:
            return self.id

    class Meta:
        ordering = ('-time_published',)
        #verbose_name_plural = 'Entries'

    def __unicode__(self):
        return u'%s, %s, %s' % (self.title, self.author, self.time_published)

    @models.permalink
    def get_absolute_url(self):
        '''
        return ('entry_date_detail', (), {
            'year': self.time_published.year,
            'month': self.time_published.month,
            'day': self.time_published.day,
            'slug': self.title
        })'''
        #return ('django.views.generic.list_detail.object_detail', None, {'object_id': self.id})
        #return 'blog/%s' % self.url_title
        return ('entry_detail', (), {'entry_title': self.url_title})

'''
class EntryManager(models.Manager):
    def drafts(self):
        """
        Returns a queryset with drafts
        """
        return self.get_query_set().filter(status=0)

    def published(self):
        """
        Returns a queryset with published entries
        """
        return self.get_query_set().filter(status=1, date_published__lte=datetime.now())

    def recent(self, limit=2):
        """
        Returns a queryset with recent entries
        """
        return self.published()[:limit]'''

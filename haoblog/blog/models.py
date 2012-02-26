# coding=utf8

from datetime import datetime
from django.db import models
#from django.utils.encoding import iri_to_uri


# 控制Entry和Comment的显示或隐藏
STATUS_CHOICES = (
    (0, 'Draft'), # 隐藏
    (1, 'Published'), # 显示
)


class Tag(models.Model):
    #count = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=20)

    @property
    def entry_count(self):
        return Entry.objects.filter(tags=self.id).count()

    def __unicode__(self):
        return u'%s' % self.name

    @models.permalink
    def get_absolute_url(self):
        #return 'blog/tag/%s' % self.name
        return ('tag_index', (), {'tag_name': self.name})


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)

    @property
    def entry_count(self):
        return Entry.objects.filter(catalog=self.id).count()

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
        '''文章的URL标题，用于显示在URL中，如果没添加英文标题，则设置为id'''
        if self._url_title:
            return self._url_title
        else:
            return self.id

    @property
    def total_comments(self):
        '''返回当前文章的所有评论'''
        return Comment.objects.filter(entry=self.id)

    @property
    def total_tags(self):
        '''取得当前Entry的所有Tag'''
        return self.tags.all()

    @property
    def total_categories(self):
        '''取得当前Entry的所有Category'''
        return self.catalog.all()

    class Meta:
        ordering = ('-time_published',)
        #verbose_name_plural = 'Entries'

    def __unicode__(self):
        return u'%s, %s, %s' % (self.title, self.author, self.time_published)

    @models.permalink
    def get_absolute_url(self):
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


class Comment(models.Model):
    time_published = models.DateTimeField(default=datetime.now, blank=False, null=False)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1) # 默认Published为显示
    email = models.EmailField(max_length=75, blank=True, null=True)
    author = models.CharField(max_length=30, blank=True, null=True, default='None')
    site_url = models.URLField(verify_exists=False, max_length=100, blank=True, null=True)
    content = models.CharField(blank=False, null=False, max_length=1000)
    entry = models.ForeignKey(Entry)

    class Meta:
        ordering = ('time_published',)

    def __unicode__(self):
        return u'%s, %s, %s, %s' % (self.author, self.time_published,
                self.email, self.site_url
        )

    @models.permalink
    def get_absolute_url(self):
        return ''

BEGIN TRANSACTION;
CREATE TABLE "blog_entry" (
    "id" integer NOT NULL PRIMARY KEY,
    "title" varchar(100) NOT NULL,
    "_url_title" varchar(100),
    "status" integer NOT NULL,
    "content" text NOT NULL,
    "author_id" integer NOT NULL REFERENCES "auth_user" ("id"),
    "time_created" datetime NOT NULL,
    "time_modified" datetime,
    "time_published" datetime NOT NULL
);
INSERT INTO "blog_entry" VALUES(1,'hao-book','',1,'法就是犯贱啊了当时警方垃圾散发设计的弗拉基的山路附近拉就是到了附近
上的浪费空间阿隆索的减肥啦即使到了附近
阿隆索的减肥啦即使到了附近
放假啦即使到了放假啊了
法律开始的警方立即啊法律纠纷拉萨解放了结
法律就是到了放假啊涉及地方ja上发牢骚打开解放拉萨来的房价
反垃圾啊流口水的减肥；啦就；家啊山东雷锋哈的森林和法兰克就是了',1,'2012-02-06 19:19:06.689747','2012-02-06 19:21:46.150504','2012-02-06 19:18:18');
INSERT INTO "blog_entry" VALUES(2,'How PGP works','how-PGP-works',1,'faljsdflkjalsdfjla了空间发牢骚的减肥了卡建设力度及法律jflakjsdlfj

放假啦即使到了附近阿拉斯加的法律界阿隆索的减肥啦结束了j
阿拉斯加法律界阿斯利得解放啦建设的；放假啊伤的房间啊善良的房价


法律上打开解放啦即使到了放假啊历史的减肥啦就是j弗拉就是地方拉就是地方看见
解放啦即使到了放假啊；是',1,'2012-02-06 19:22:30.236626','2012-02-06 20:12:18.194655','2012-02-06 19:21:46');
INSERT INTO "blog_entry" VALUES(3,'常用bash命令 - 在mac或者电脑上捣腾的一切 - 博客大巴','test',1,'发生的法迪斯科飞机阿隆索的减肥垃圾的山路附近阿里js

解放了卡就诞生了解放啦即使到了附近

啊开始大幅拉升的垃圾分类jslj 


阿斯的发掘的山路口附近阿隆索',1,'2012-02-06 20:12:48.919656','2012-02-06 20:12:48.919691','2012-02-06 20:12:18');
INSERT INTO "blog_entry" VALUES(4,'漫话中文分词算法','my-book',1,'flkajsdlfjalsjdlfj会计师地方啦建设的龙卷风
法律涉及地方拉就是；的房间； a
阿斯的房价拉就是地方垃圾啊

房价阿隆索的减肥垃圾；

的房价阿隆索的减肥；拉接受的；了放假啊了；建设的法律界阿隆索的减肥啦就是

弗拉建设的法律及阿桑德拉房价；啊建设的； 

饭店房间啊可怜的手机反抗了就',1,'2012-02-06 20:13:34.515929','2012-02-06 20:13:34.515963','2012-02-06 20:12:49');
INSERT INTO "blog_entry" VALUES(5,'how to design index?','how-to-design-index',1,'{% extends ''base.html'' %}

{% block entries %}
    {% if entries %}
        {% for entry in entries %}
            <div id="entry">
                <h3><a href="{{ entry.get_absolute_url }}/blog/{{ entry.url_title }}">{{ entry.title }}</a></h3>
                <h5>{{ entry.author}}, {{ entry.time_published|date:"f A, Y-n-j l" }}</h5>
                <div id="entry_content">
                    {{ entry.content_preview|linebreaks }}
                </div>
            </div>
        {% endfor %}
    {% endif %}
{% endblock %}

{% block categories %}
    {% if categories %}
        <ul id="categories_list">
            {% for category in categories %}
                <li><a href="{{ category.get_absolute_url }}" title="{{ category.name }}目录下的所有文章">{{ category.name }}</li>
            {% endfor %}
        </ul>
    {% endif %}
{% endblock %}

{% block tags %}
    {% if tags %}
        <ul id="tags_list">
            {% for tag in tags %}
                <li>{{ tag.name }}</li>
            {% endfor %}
        </ul>
    {% endif %}
{% endblock %}
',1,'2012-02-06 20:14:23.387866','2012-02-06 20:14:23.387900','2012-02-06 20:13:34');
INSERT INTO "blog_entry" VALUES(6,'paste_form.html','test-category-paging',1,'#coding=utf8

from django.shortcuts import render_to_response
from django.http import Http404
from haoblog.blog.models import Entry, Tag, Category

ENTRY_PER_PAGE = 2


def test(request):
    return render_to_response(''templates/test.html'', {})

def index(request, page_num=1, is_page=False):
    #assert False
    page_num = int(page_num)
    entries = Entry.objects.all()[ENTRY_PER_PAGE*(page_num-1): ENTRY_PER_PAGE*(page_num)]

    has_next = _has_next_page(page_num)
    has_prev = True if page_num > 1 else False
    next_page_num = page_num+1 if has_next else 1
    prev_page_num = page_num-1 if has_prev else 1
    title = ''首页 - haoblog'' if is_page else ''首页|第二页 - haoblog''
    info = {
            ''title'': title,
            ''entries'': entries,
            ''has_next'': has_next,
            ''has_prev'': has_prev,
            ''page_num'': page_num,
            ''next_page_num'': next_page_num,
            ''prev_page_num'': prev_page_num,
    }
    info.update(_common_info())
    #assert False
    return render_to_response(''index.html'', info)


def _has_next_page(page_num):
    if Entry.objects.count() > ENTRY_PER_PAGE*(page_num):
        return True
    return False


def entry_detail(request, entry_title):
    entries = Entry.objects.filter(_url_title__iexact=entry_title)
    if not entries:
        entries = Entry.objects.filter(pk=entry_title)
    if not entries:
        raise Http404
    info = _common_info()
    info[''entries''] = entries
    if len(entries) == 1:
        info[''title''] = u''%s - haoblog'' % entries[0].title
    else:
        info[''title''] = u''%s - haoblog'' % entry_title
    #assert False
    return render_to_response(''entry_detail.html'', info)


def category_detail(request, category_name, page_num=1):
    category_id = Category.objects.get(name__iexact=category_name).pk
    entries = Entry.objects.filter(catalog=category_id)
    if not entries:
        raise Http404
    total_count = entries.count()
    entries = entries[ENTRY_PER_PAGE*(page_num-1): ENTRY_PER_PAGE*page_num]
    title = u''"%s" 目录下的所有文章 - haoblog'' % category_name
    has_next = total_count > ENTRY_PER_PAGE*page_num
    info = {
            ''title'': title,
            ''entries'': entries,
            ''has_next'': has_next,
            ''has_prev'': page_num > 1,
            ''next_page_num'': page_num+1 if has_next else 1,
            ''prev_page_num'': page_num-1 if page_num > 1 else 1,
    }
    info.update(_common_info())
    return render_to_response(''index.html'', info)


def tag_detail(request, tag_name):
    tag_id = Tag.objects.get(name__iexact=tag_name).pk
    entries = Entry.objects.filter(tags=tag_id)
    if not entries:
        raise Http404
    info = _common_info()
    info[''entries''] = entries
    info[''title''] = u''"%s" 标签的所有文章 - haoblog'' % tag_name
    #assert False
    return render_to_response(''index.html'', info)

def _common_info():
    ''''''取得每个页面通用的所有Category和Tag''''''
    tags = Tag.objects.all()
    categories = Category.objects.all()
    info = {
            ''tags'': tags,
            ''categories'': categories
    }
    return info
',1,'2012-02-07 16:48:36.320807','2012-02-07 16:48:36.320842','2012-02-07 16:47:36');
INSERT INTO "blog_entry" VALUES(7,'Hacker News | So you want to do the SICP','Hacker-News-So-you-are-the-one',1,'# coding=utf8

from datetime import datetime
from django.db import models
from django.utils.encoding import iri_to_uri

# Create your models here.


STATUS_CHOICES = (
    (0, ''Draft''),
    (1, ''Published''),
)

class Tag(models.Model):
    #count = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=20)

    def __unicode__(self):
        return u''%s'' % self.name
    
    @models.permalink
    def get_absolute_url(self):
        #return ''blog/tag/%s'' % self.name
        return (''tag_index'', (), {''tag_name'': self.name})
''''''
    def __init__(self, count, tags):
        if self.tags in Tag.objects.all():
            self.count += 1

    def save(self, *args, **kwargs):
        if self.tag in Tag.objects.all():
            self.count += 1
        super(Tag, self).save(*agrs, **kwargs)''''''


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __unicode__(self):
        return u''%s'' % self.name

    @models.permalink
    def get_absolute_url(self):
        #return ''/blog/category/%s'' % self.name
        return (''category_index'', (), {''category_name'': self.name})


class Entry(models.Model):
    title = models.CharField(max_length=100)
    _url_title = models.CharField(max_length=100, blank=True, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    content = models.TextField()
    author = models.ForeignKey(''auth.User'', related_name=''entries'')
    tags = models.ManyToManyField(Tag)
    catalog = models.ManyToManyField(Category, related_name=''catalogues'')

    time_created = models.DateTimeField(auto_now_add=True, blank=True, editable=False)
    time_modified = models.DateTimeField(auto_now=True, blank=True, null=True)
    time_published = models.DateTimeField(default=datetime.now, blank=False, null=False)

    @property
    def content_preview(self):
        ''''''文章预览，用于首页显示所有文章''''''
        return self.content[ :len(self.content)/4]

    @property
    def url_title(self):
        if self._url_title:
            return self._url_title
        else:
            return self.id

    class Meta:
        ordering = (''-time_published'',)
        #verbose_name_plural = ''Entries''

    def __unicode__(self):
        return u''%s, %s, %s'' % (self.title, self.author, self.time_published)

    @models.permalink
    def get_absolute_url(self):
        ''''''
        return (''entry_date_detail'', (), {
            ''year'': self.time_published.year,
            ''month'': self.time_published.month,
            ''day'': self.time_published.day,
            ''slug'': self.title
        })''''''
        #return (''django.views.generic.list_detail.object_detail'', None, {''object_id'': self.id})
        #return ''blog/%s'' % self.url_title
        return (''entry_detail'', (), {''entry_title'': self.url_title})

''''''
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
        return self.published()[:limit]''''''
',1,'2012-02-07 17:12:05.090508','2012-02-07 19:43:15.878761','2012-02-07 17:11:03');
CREATE INDEX "blog_entry_cc846901" ON "blog_entry" ("author_id");
COMMIT;
BEGIN TRANSACTION;
COMMIT;
BEGIN TRANSACTION;
CREATE TABLE "blog_entry_tags" (
    "id" integer NOT NULL PRIMARY KEY,
    "entry_id" integer NOT NULL,
    "tag_id" integer NOT NULL REFERENCES "blog_tag" ("id"),
    UNIQUE ("entry_id", "tag_id")
);
INSERT INTO "blog_entry_tags" VALUES(1,1,1);
INSERT INTO "blog_entry_tags" VALUES(2,2,1);
INSERT INTO "blog_entry_tags" VALUES(3,2,2);
INSERT INTO "blog_entry_tags" VALUES(4,2,3);
INSERT INTO "blog_entry_tags" VALUES(5,2,4);
INSERT INTO "blog_entry_tags" VALUES(6,3,2);
INSERT INTO "blog_entry_tags" VALUES(7,4,4);
INSERT INTO "blog_entry_tags" VALUES(8,5,3);
INSERT INTO "blog_entry_tags" VALUES(9,6,1);
INSERT INTO "blog_entry_tags" VALUES(10,6,2);
INSERT INTO "blog_entry_tags" VALUES(11,6,3);
INSERT INTO "blog_entry_tags" VALUES(12,6,4);
INSERT INTO "blog_entry_tags" VALUES(13,7,1);
INSERT INTO "blog_entry_tags" VALUES(14,7,2);
INSERT INTO "blog_entry_tags" VALUES(15,7,3);
INSERT INTO "blog_entry_tags" VALUES(16,7,4);
CREATE INDEX "blog_entry_tags_38a62041" ON "blog_entry_tags" ("entry_id");
CREATE INDEX "blog_entry_tags_3747b463" ON "blog_entry_tags" ("tag_id");
COMMIT;
BEGIN TRANSACTION;
CREATE TABLE "blog_tag" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(20) NOT NULL
);
INSERT INTO "blog_tag" VALUES(1,'Python');
INSERT INTO "blog_tag" VALUES(2,'生活');
INSERT INTO "blog_tag" VALUES(3,'IT业界');
INSERT INTO "blog_tag" VALUES(4,'开源');
COMMIT;
BEGIN TRANSACTION;
CREATE TABLE "blog_category" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(20) NOT NULL UNIQUE
);
INSERT INTO "blog_category" VALUES(1,'Java');
INSERT INTO "blog_category" VALUES(2,'Python');
INSERT INTO "blog_category" VALUES(3,'Django');
COMMIT;

#coding=utf8

from django.shortcuts import render_to_response
from django.http import Http404
from haoblog.blog.models import Entry, Tag, Category, Comment
from haoblog.blog.forms import CommentForm

ENTRY_PER_PAGE = 2


def test(request):
    return _render_with_info('templates/test.html', {})

def index(request, page_num=1, is_page=False):
    #assert False
    page_num = int(page_num)
    entries = Entry.objects.all()[ENTRY_PER_PAGE*(page_num-1): ENTRY_PER_PAGE*(page_num)]

    has_next = True if Entry.objects.count() > ENTRY_PER_PAGE*page_num else False
    has_prev = True if page_num > 1 else False
    next_page_num = page_num+1 if has_next else 1
    prev_page_num = page_num-1 if has_prev else 1
    title = u'%s - haoblog' % u'首页' if is_page else u'文章列表'
    info = {
            'title': title,
            'entries': entries,
            'has_next': has_next,
            'has_prev': has_prev,
            'page_num': page_num,
            'next_page_num': next_page_num,
            'prev_page_num': prev_page_num,
            #'nav_url': 'blog_page',
    }
    #assert False
    return _render_with_info('index.html', info)


def entry_detail(request, entry_title):
    entries = Entry.objects.filter(_url_title__iexact=entry_title) # 用url_title搜索
    if not entries:
        entries = Entry.objects.filter(pk=entry_title) # 为空则用“id”搜索
    if not entries:
        raise Http404

    next_entry = Entry.objects.filter(time_published__gt=entries[0].time_published)
    prev_entry = Entry.objects.filter(time_published__lt=entries[0].time_published)

    next_entry = next_entry.order_by('time_published')[0] if next_entry.count()>0 else None
    prev_entry = prev_entry[0] if prev_entry.count()>0 else None
    has_next = True if next_entry else False
    has_prev = True if prev_entry else False
    comment_form = CommentForm(initial={'entry_id': entries[0].id})
    info = {
            'entry': entries[0],
            'title': u'%s - haoblog' % entries[0].title,
            'has_next': has_next,
            'has_prev': has_prev,
            'next_entry': next_entry,
            'prev_entry': prev_entry,
            'comment_form': comment_form,
    }
    #assert False
    return _render_with_info('entry_detail.html', info)


def add_comment(request):
    #assert False
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            e = Entry.objects.get(pk=int(cd['entry_id']))
            new_comment = Comment(
                    email=cd['email'],
                    author=cd['author'],
                    site_url=cd['site_url'],
                    content=cd['content'],
                    entry=e,
                    )
            new_comment.save()
            return entry_detail(request, cd['entry_id'])
    #return _render_with_info('entry_detail.html', info)
    raise Http404


def category_detail(request, category_name, page_num=1):
    category_id = Category.objects.get(name__iexact=category_name).pk
    entries = Entry.objects.filter(catalog=category_id)
    if not entries:
        raise Http404
    total_count = entries.count()
    page_num = int(page_num)
    entries = entries[ENTRY_PER_PAGE*(page_num-1): ENTRY_PER_PAGE*page_num]
    title = u'"%s" 目录下的所有文章 - haoblog' % category_name
    has_next = total_count > ENTRY_PER_PAGE*page_num
    info = {
            'title': title,
            'entries': entries,
            'category_name': category_name,
            'has_next': has_next,
            'has_prev': page_num > 1,
            'next_page_num': page_num+1 if has_next else 1,
            'prev_page_num': page_num-1 if page_num > 1 else 1,
    }
    return _render_with_info('category_detail.html', info)


def tag_detail(request, tag_name, page_num=1):
    tag_id = Tag.objects.get(name__iexact=tag_name).pk
    entries = Entry.objects.filter(tags=tag_id)
    if not entries:
        raise Http404
    total_count = entries.count()
    page_num = int(page_num)
    entries = entries[ENTRY_PER_PAGE*(page_num-1): ENTRY_PER_PAGE*page_num]
    has_next = total_count > ENTRY_PER_PAGE*page_num
    info = {
            'title': u'"%s"标签下的所有文章 - haoblog' % tag_name,
            'entries': entries,
            'tag_name': tag_name,
            'has_next': has_next,
            'has_prev': page_num > 1,
            'next_page_num': page_num+1 if has_next else 1,
            'prev_page_num': page_num-1 if page_num > 1 else 1,
    }
    return _render_with_info('tag_detail.html', info)


def _render_with_info(template_name, extra_info={}):
    '''
    封装render_to_response()方法，将传入的extra_info字典
    合并所有页面通用的Tag和Category，再render到指定的模板template_name
    '''
    tags = Tag.objects.all()
    categories = Category.objects.all()
    info = {
            'tags': tags,
            'categories': categories
    }
    info.update(extra_info)
    return render_to_response(template_name, info)

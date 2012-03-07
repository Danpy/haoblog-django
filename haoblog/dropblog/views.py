#coding=utf8

from django.shortcuts import render_to_response, redirect
from django.http import Http404

from django.contrib.auth.models import User
from haoblog.dropblog.models import Entry, Tag, Category, Comment
from haoblog.dropblog.forms import CommentForm
from haoblog.dropboxapp.models import DropboxUser
from haoblog import userconfig

# 分页每一页的Entry数
ENTRY_PER_PAGE = userconfig.ENTRY_PER_PAGE


def index(request, page_num=1, is_page=False, url_name=None):
    #assert False
    page_num = int(page_num)
    dropbox_user = DropboxUser.objects.get(url_name__iexact=url_name)
    user = User.objects.get(username__iexact=dropbox_user.uid)
    all_entries = Entry.objects.filter(author=user)
    entries = all_entries[ENTRY_PER_PAGE*(page_num-1): ENTRY_PER_PAGE*(page_num)]

    has_next = True if len(all_entries) > ENTRY_PER_PAGE*page_num else False
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
            'url_name': url_name,
    }
    #assert False
    return _render_with_info('dropblog/index.html', info)


def entry_detail(request, entry_title, url_name=None):
    dropbox_user = DropboxUser.objects.get(url_name__iexact=url_name)
    admin_user = User.objects.get(username__iexact=dropbox_user.uid)
    all_entries = Entry.objects.filter(author=admin_user)
    entries = all_entries.filter(_url_title__iexact=entry_title) # 用url_title搜索
    if not entries:
        entries = all_entries.filter(pk=entry_title) # 为空则用“id”搜索
    if not entries:
        raise Http404

    next_entry = all_entries.filter(time_published__gt=entries[0].time_published)
    prev_entry = all_entries.filter(time_published__lt=entries[0].time_published)

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
            'url_name': url_name,
    }
    #assert False
    return _render_with_info('dropblog/entry_detail.html', info)


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
            admin_user = e.author
            du = DropboxUser.objects.get(uid__iexact=admin_user.username)
            #return entry_detail(request, cd['entry_id'], du.url_name)
            #return redirect('entry_detail', entry_title=cd['entry_id'], url_name=du.url_name)
            return redirect('entry_detail', entry_title=e._url_title, url_name=du.url_name)
    #return _render_with_info('entry_detail.html', info)

    raise Http404


def category_detail(request, category_name, page_num=1, url_name=None):
    if not url_name:
        url_name = request.GET['author']
    dropbox_user = DropboxUser.objects.get(url_name__iexact=url_name)
    admin_user = User.objects.get(username__iexact=dropbox_user.uid)
    all_entries = Entry.objects.filter(author=admin_user)

    category_id = Category.objects.get(name__iexact=category_name).pk
    entries = all_entries.filter(catalog=category_id)
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
            'url_name': url_name,
            'tips': u'“%s” 目录下的文章' % category_name,
    }
    #assert False
    return _render_with_info('dropblog/category_detail.html', info)


def tag_detail(request, tag_name, page_num=1, url_name=None):
    if not url_name:
        url_name = request.GET['author']
    dropbox_user = DropboxUser.objects.get(url_name__iexact=url_name)
    admin_user = User.objects.get(username__iexact=dropbox_user.uid)
    all_entries = Entry.objects.filter(author=admin_user)

    tag_id = Tag.objects.get(name__iexact=tag_name).pk
    entries = all_entries.filter(tags=tag_id)
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
            'next_page_num':page_num+1 if has_next else 1,
            'prev_page_num': page_num-1 if page_num > 1 else 1,
            'url_name': url_name,
            'tips': u'“%s” 标签下的文章' % tag_name,
    }
    return _render_with_info('dropblog/tag_detail.html', info)


def _render_with_info(template_name, extra_info={}):
    '''
    封装render_to_response()方法，将传入的extra_info字典
    合并所有页面通用的Tag和Category，再render到指定的模板template_name
    '''
    tags = Tag.objects.all()
    categories = Category.objects.all()
    info = {
            'tags': tags,
            'categories': categories,
            'user_widgets': userconfig.WIDGETS,
            'blog_name': userconfig.blog_name,
    }
    info.update(extra_info)
    return render_to_response(template_name, info)


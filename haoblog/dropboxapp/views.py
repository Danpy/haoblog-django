# coding=utf8

from django.shortcuts import render_to_response, redirect
from django.http import Http404, HttpResponse
from django.template import Context
from django.contrib.auth.models import User
from dropbox import client, session, rest

from haoblog.blog.models import Entry, Tag, Category
from haoblog.dropboxapp.models import DropboxUser
from haoblog.dropboxapp import keys as settings


APP_KEY = settings.APP_KEY
APP_SECRET = settings.APP_SECRET
ACCESS_TYPE = settings.ACCESS_TYPE

def _get_session():
    return session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)


def _get_client(access_token):
    sess = _get_session()
    sess.set_token(access_token.key, access_token.secret)
    return client.DropboxClient(sess)


def oauth_start(request):
    return render_to_response('oauth_start.html', {})


def dropbox_oauth(request):
    '''请求获得request_token并重定向到callbock_url'''
    sess = _get_session()
    request_token = sess.obtain_request_token()
    request.session['request_token'] = request_token
    #callback_url = 'http://127.0.0.1:8000/dropbox/settings/'
    callback_url = 'http://127.0.0.1:8000/dropbox/temp/'
    url = sess.build_authorize_url(request_token, oauth_callback=callback_url)
    return redirect(url)


def test(request):
    return render_to_response('dropblog.html', {})


def dropbox_temp(request):
    return render_to_response('dropbox_settings.html', {})


def check(request, para_name, para_value):
    '''判断blog_name 和 url_name是否已经存在'''
    try:
        if DropboxUser.objects.get(para_name__iexact=para_value):
            return HttpResponse(u'<b style="color:red; font-size:10px;">%s不可用!</b>' % para_value)
    except:
        return HttpResponse(u'<b style="color:#fff; font-size: 10px;">%s可用</b>' % para_value)


def dropbox_settings(request):
    sess = _get_session()
    #if 'oauth_token' in request.GET:
    #    request_token = request.GET['oauth_token']
    #sess.set_request_token(request_token, request_token_secret)
    request_token = request.session['request_token']
    access_token = sess.obtain_access_token(request_token)
    local_client = _get_client(access_token)
    account_info = local_client.account_info()

    try:
        posts_folder_meta = local_client.file_create_folder('/posts')
    except:
        posts_folder_meta = local_client.metadata('/posts')
    app_folder_meta = local_client.metadata('/')

    display_name = account_info['display_name']
    uid = account_info['uid']
    blog_name = request.POST['blog_name']
    url_name = request.POST['url_name']
    user = DropboxUser(
            dropbox_display_name=display_name,
            uid=uid,
            blog_name=blog_name,
            url_name=url_name,
            access_token=access_token.key,
            access_token_secret=access_token.secret,
            app_folder_hash=app_folder_meta['hash'],
            posts_folder_hash=posts_folder_meta['hash']
    )
    user.save()

    #admin_user = UserManager.create_user(user.uid, 'admin.haoblog@gmail.com', '123')
    admin_user = User(username=user.uid, email='admin.haoblog@gmail.com', password='123')
    admin_user.save()

    c = Context({'user': user})
    #return render_to_response('dropbox_settings.html', {'user': user})
    return render_to_response('blog_updates.html', c)
    #return redirect('/dropbox/blog/updates/', user.uid)


def blog_updates(request):
    user_uid = request.POST['uid']
    user = DropboxUser.objects.get(uid=user_uid)
    sess = _get_session()
    sess.set_token(user.access_token, user.access_token_secret)
    local_client = client.DropboxClient(sess)

    c = Context({'user': user})
    try:
        app_folder_meta = local_client.metadata('/', user.app_folder_hash)
        admin_user = User.objects.get(username__iexact=user_uid)
        _process_files(local_client, admin_user)
        return render_to_response('blog_updates.html', c)

    except rest.ErrorResponse:
        if rest.ErrorResponse.status == 304:
            return render_to_response('blog_updates.html', c)


def _process_files(local_client, admin_user):
    posts_folder_meta = local_client.metadata('/posts')
    posts_list = posts_folder_meta['contents']
    for post in posts_list:
        f = local_client.get_file(post['path']).read()
        lines = f.split('\n')
        _process_post(lines, admin_user)
    return redirect('/blog/')


def _process_post(lines, admin_user):
    line_num = 0
    entry = Entry()
    entry.author = admin_user
    entry.save()

    for l in lines:
        if not l.startswith('-'):
            break
        line_num += 1
        kv = l.split(': ')
        prefix = kv[0].strip()[1:]

        if 'Title' == prefix:
            entry.title = kv[1].strip()
        elif 'Url' == prefix:
            entry._url_title = '-'.join(kv[1].strip().split(' '))
        elif 'Date' == prefix:
            entry.time_created = kv[1].strip()
        elif 'Tags' == prefix:
            for t in kv[1].strip().split(' '):
                try:
                    tag = Tag.objects.get(name__iexact=t)
                    entry.tags.add(tag)
                except Tag.DoesNotExist:
                    tag = Tag(name=t)
                    tag.save()
                    entry.tags.add(tag)
        elif 'Categories' == prefix:
            for c in kv[1].strip().split(' '):
                try:
                    category = Category.objects.get(name__iexact=c)
                    entry.catalog.add(category)
                except Category.DoesNotExist:
                    category = Category(name=c)
                    category.save()
                    entry.catalog.add(category)
        elif 'Status' == prefix:
            entry.status = 1 if kv[1].strip() == 'Published' else 0

    content = '\n'.join(lines[line_num: ])
    entry.content = content
    entry.save()

'''
{
    "hash": "6cf4b41fd9e39205db84c07e462ddd01", 
    "bytes": 0, 
    "thumb_exists": false, 
    "path": "/posts", 
    "is_dir": true, 
    "contents": [
        {
            "rev": "d062e7f33", 
            "thumb_exists": false, 
            "path": "/posts/my-first-post.md", 
            "is_dir": false, 
            "icon": "page_white", 
            "bytes": 58, 
            "modified": "Tue, 28 Feb 2012 10:52:50 +0000", 
            "size": "58 bytes", 
            "root": "dropbox", 
            "mime_type": "application/octet-stream", 
            "revision": 13
        }
    ], 
    "icon": "folder", 
    "rev": "a062e7f33", 
    "modified": "Sun, 26 Feb 2012 09:20:28 +0000", 
    "size": "0 bytes", 
    "root": "app_folder", 
    "revision": 10
}
'''

'''
https://www.dropbox.com/login?cont=https%3A//www.dropbox.com/1/oauth/authorize%3Foauth_token%3Dlpr01ku14r94ck5%26oauth_callback%3Dhttp%253A%252F%252Flocalhost%253A8000%252Fcallback
'''

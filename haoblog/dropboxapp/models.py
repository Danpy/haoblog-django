# coding=utf8

from django.db import models


class DropboxUser(models.Model):
    dropbox_display_name = models.CharField(blank=True, null=False, max_length=20)
    uid = models.CharField(blank=False, null=False, max_length=50, unique=True)
    # Dropbox用户oauth授权的时间戳
    account_oauth_date = models.DateTimeField(auto_now_add=True)
    # 授权后由用户自定义，用于展示在blog顶栏
    blog_name = models.CharField(blank=True, null=True, max_length=20)
    # 为每个用户生成的URL后缀
    url_name = models.CharField(blank=False, null=False, max_length=20, unique=True)
    # oauth授权后获取到的access_token_key
    access_token = models.CharField(blank=False, null=False, max_length=20)
    # oauth授权后获取到的access_token_secret
    access_token_secret = models.CharField(blank=False, null=False, max_length=20)
    app_folder_hash = models.CharField(blank=False, null=False, max_length=100)
    posts_folder_hash = models.CharField(blank=False, null=False, max_length=100)

    def __unicode__(self):
        return u'%s, %s, %s, %s' % (self.dropbox_display_name,
                self.uid, self.blog_name, self.url_name)
    
    @models.permalink
    def get_absolute_url(self):
        return ''

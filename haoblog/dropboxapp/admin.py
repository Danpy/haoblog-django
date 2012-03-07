# coding=utf8

from django.contrib import admin
from haoblog.dropboxapp.models import DropboxUser


class DropboxUserAdmin(admin.ModelAdmin):
    list_display = ('dropbox_display_name', 'uid', 'account_oauth_date', 'blog_name', 'url_name', 'id')
    ordering = ('-account_oauth_date',)
    search_fields = ('dropbox_display_name',)
    



admin.site.register(DropboxUser, DropboxUserAdmin)

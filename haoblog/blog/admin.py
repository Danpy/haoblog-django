# coding=utf8

from django.contrib import admin
from haoblog.blog.models import Entry, Tag, Category, Comment

class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'time_published', 'author', '_url_title', 'id')
    ordering = ('-time_published',)
    search_fields = ('title',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'time_published', 'email', 'site_url', 'id', 'entry')
    ordering = ('-time_published',)
    search_fields = ('content',)

admin.site.register(Entry, EntryAdmin)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Comment, CommentAdmin)

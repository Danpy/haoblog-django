# coding=utf8

from django.contrib import admin
from haoblog.blog.models import Entry, Tag, Category

class EntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_published', 'author', '_url_title')
    ordering = ('-time_published',)
    search_fields = ('title',)

admin.site.register(Entry, EntryAdmin)
admin.site.register(Tag)
admin.site.register(Category)

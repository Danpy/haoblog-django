# coding=utf8

from django.contrib import admin
from haoblog.blog.models import Entry, Tag, Category, Comment


class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'time_published', 'author', '_url_title', 'id')
    ordering = ('-time_published',)
    search_fields = ('title',)
    filter_horizontal = ('tags', 'catalog',)

    class Media:
        js = (
                '/static_media/js/tiny_mce/tiny_mce.js',
                '/static_media/js/tiny_mce/textareas.js',
                #'/media/js/tiny_mce/tiny_mce.js',
                #'/media/js/tiny_mce/textareas.js',
        )


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'time_published', 'email', 'site_url', 'id', 'entry')
    ordering = ('-time_published',)
    search_fields = ('content',)

admin.site.register(Entry, EntryAdmin)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Comment, CommentAdmin)

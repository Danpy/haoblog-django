# coding=utf8

from django.contrib import admin
from haoblog.testmodel.models import One, Many


admin.site.register(One)
admin.site.register(Many)

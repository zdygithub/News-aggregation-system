# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from news import models

class NewsDataAdmin(admin.ModelAdmin):
    list_display = ('title','title_original','site_original','url_original',
                    'newstime', 'similar', 'content','keyword')
                    # ,'click','content_html'

class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('username','password','keyword')


admin.site.register(models.NewsData, NewsDataAdmin)
admin.site.register(models.UserInfo, UserInfoAdmin)

# Register your models here.

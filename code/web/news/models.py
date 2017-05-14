# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class NewsData(models.Model):
    title = models.CharField(max_length=200, verbose_name=u'标题')
    title_original  = models.CharField(max_length=200, verbose_name=u'原文标题')
    site_original = models.CharField(max_length=100, verbose_name=u'原文来自')
    url_original = models.CharField(max_length=300, verbose_name=u'原文地址')
    newstime = models.DateTimeField(verbose_name=u'发布时间')
    front_image_url = models.CharField(max_length=300,null=True, blank=True, verbose_name=u'封面图地址')
    click = models.IntegerField(max_length=11, default=0, verbose_name=u'点击量')
    content = models.TextField(null=True, blank=True, verbose_name=u'新闻内容')
    content_html = models.TextField(null=True, blank=True, verbose_name=u'新闻内容html')

    class Meta:
        verbose_name = u'新闻数据'
        verbose_name_plural = verbose_name
        db_table = 'news_data'  # 设置表名
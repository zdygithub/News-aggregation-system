# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class UewsData(models.Model):
    title = models.CharField(max_length=200, verbose_name=u'标题')
    title_original  = models.CharField(max_length=200, verbose_name=u'原文标题')
    site_original = models.CharField(max_length=100, verbose_name=u'原文来自')
    url_original = models.CharField(max_length=300, verbose_name=u'原文地址')
    newstime = models.DateField(verbose_name=u'发布时间')
    content = models.TextField(null=True, blank=True, verbose_name=u'新闻内容')
    content_html = models.TextField(null=True, blank=True, verbose_name=u'新闻内容html')

    class Meta:
        verbose_name = u'新闻数据'
        verbose_name_plural = verbose_name
        db_table = 'uews_data'  # 设置表名
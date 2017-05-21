# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import NewsData


# Create your views here.
def NewsList(request):
    news = NewsData.objects.all().order_by('-id')  # 按id降序排列
    return render(request, 'news_list.html', {'news':news})


def NewsContent(request, n_id=1):
    news =  NewsData.objects.get(id=n_id)
    return render(request, 'news_content.html', {'news':news})
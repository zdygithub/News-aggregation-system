# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import UewsData

# Create your views here.
def UewContent(request):
    uews =  UewsData.objects.filter(id=1)
    for u in uews:
        title = u.title
        title_original = u.title_original
        site_original = u.site_original
        newstime = u.newstime
        url_original = u.url_original
        content_html = u.content_html


    return render(request, 'new_content.html', {
        'title': title,
        'title_original':title_original,
        'site_original':site_original,
        'newstime':newstime,
        'url_original':url_original,
        'content_html': content_html,

    })
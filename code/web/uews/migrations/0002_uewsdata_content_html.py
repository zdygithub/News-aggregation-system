# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-13 11:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uews', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='uewsdata',
            name='content_html',
            field=models.TextField(blank=True, null=True, verbose_name='\u65b0\u95fb\u5185\u5bb9html'),
        ),
    ]

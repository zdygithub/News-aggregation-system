# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-14 03:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_auto_20170513_2302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsdata',
            name='newstime',
            field=models.DateTimeField(verbose_name='\u53d1\u5e03\u65f6\u95f4'),
        ),
        migrations.AlterModelTable(
            name='newsdata',
            table='uews_data',
        ),
    ]
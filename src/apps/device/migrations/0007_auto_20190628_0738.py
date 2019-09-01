# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2019-06-28 07:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0006_auto_20190628_0706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phone',
            name='platform',
            field=models.IntegerField(choices=[(0, 'Android'), (1, 'IOS')], default=1, help_text='手机类型 0 ANDROID， 1 IOS', verbose_name='手机类型 0 ANDROID， 1 IOS'),
        ),
        migrations.AlterField(
            model_name='phone',
            name='status',
            field=models.IntegerField(choices=[(1, 'offline'), (0, 'online'), (2, 'disabled')], default=0, help_text='手机状态', verbose_name='手机状态'),
        ),
    ]

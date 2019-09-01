# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2019-06-29 08:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0006_auto_20190628_0738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task_state',
            field=models.IntegerField(choices=[(2, 'complete'), (3, 'success'), (0, 'wait'), (1, 'start')], default=0, help_text='任务状态', verbose_name='任务状态'),
        ),
    ]

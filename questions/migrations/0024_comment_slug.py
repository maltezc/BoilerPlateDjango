# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-03 15:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0023_remove_comment_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='slug',
            field=models.SlugField(default='', unique=True),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-02 23:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0002_remove_comic_comic_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='comic',
            name='alt_text',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='comic',
            name='comic_page',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]

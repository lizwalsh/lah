# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-08-17 14:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('extras', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fanartgallery',
            name='gallery',
        ),
        migrations.DeleteModel(
            name='FanartGallery',
        ),
    ]

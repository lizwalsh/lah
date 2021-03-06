# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-04-02 20:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0007_auto_20160305_1417'),
    ]

    operations = [
        migrations.AddField(
            model_name='comic',
            name='cid',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='comic',
            name='guest',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='comic',
            name='published',
            field=models.BooleanField(default=False),
        ),
    ]

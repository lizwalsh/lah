# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-04-23 19:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0010_auto_20160423_1502'),
    ]

    operations = [
        migrations.CreateModel(
            name='GuestComic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(blank=True, max_length=100)),
                ('url', models.CharField(blank=True, max_length=200)),
                ('type', models.CharField(choices=[('guest', 'Guest comic'), ('special', 'Special item'), ('art', 'Filler art')], max_length=10)),
                ('ref_comic', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='comics.Comic')),
            ],
        ),
    ]
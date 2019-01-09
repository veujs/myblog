# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2018-12-28 07:10
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('article', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticlePost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(max_length=500)),
                ('body', models.TextField()),
                ('created', models.DateTimeField(default=datetime.datetime(2018, 12, 28, 7, 10, 56, 611144, tzinfo=utc))),
                ('updated', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article', to=settings.AUTH_USER_MODEL)),
                ('column', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='article_column', to='article.ArticleColumn')),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.AlterIndexTogether(
            name='articlepost',
            index_together=set([('id', 'slug')]),
        ),
    ]

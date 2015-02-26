# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FlickrUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_id', models.CharField(max_length=32)),
                ('last_get_faved', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Liking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_faved', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigIntegerField(serialize=False, primary_key=True)),
                ('owner', models.CharField(max_length=32)),
                ('url', models.URLField()),
                ('last_get_faved', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='liking',
            name='photo',
            field=models.ForeignKey(to='app.Photo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='liking',
            name='user',
            field=models.ForeignKey(to='app.FlickrUser'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='flickruser',
            name='favorited',
            field=models.ManyToManyField(to='app.Photo', through='app.Liking'),
            preserve_default=True,
        ),
    ]

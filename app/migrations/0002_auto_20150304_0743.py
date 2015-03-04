# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_review', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('photo', models.ForeignKey(to='app.Photo')),
                ('user', models.ForeignKey(to='app.FlickrUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='flickruser',
            name='reviewed',
            field=models.ManyToManyField(related_name='reviewed', through='app.Review', to='app.Photo'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='flickruser',
            name='favorited',
            field=models.ManyToManyField(related_name='favorited', through='app.Liking', to='app.Photo'),
            preserve_default=True,
        ),
    ]

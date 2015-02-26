# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_photo'),
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
                ('photo', models.ForeignKey(to='app.Photo')),
                ('user', models.ForeignKey(to='app.FlickrUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='flickruser',
            name='favorited',
            field=models.ManyToManyField(to='app.Photo', through='app.Liking'),
            preserve_default=True,
        ),
    ]

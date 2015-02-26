# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flickruser',
            name='favorited',
        ),
        migrations.RemoveField(
            model_name='liking',
            name='photo',
        ),
        migrations.RemoveField(
            model_name='liking',
            name='user',
        ),
        migrations.DeleteModel(
            name='FlickrUser',
        ),
        migrations.DeleteModel(
            name='Liking',
        ),
        migrations.DeleteModel(
            name='Photo',
        ),
    ]

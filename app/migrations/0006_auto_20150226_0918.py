# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_remove_photo_last_get_faved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='url',
            field=models.URLField(null=True),
            preserve_default=True,
        ),
    ]

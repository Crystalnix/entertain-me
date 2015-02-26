# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20150226_0918'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='last_get_faved',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]

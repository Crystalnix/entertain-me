# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20150226_0850'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='last_get_faved',
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Weight',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weight', models.FloatField(default=0)),
                ('against', models.ForeignKey(related_name='against_weight', to='app.FlickrUser')),
                ('to', models.ForeignKey(related_name='to_weight', to='app.FlickrUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20150108_2234'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalproduct',
            name='number_of_api_calls',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='number_of_api_calls',
            field=models.PositiveIntegerField(default=0),
            preserve_default=True,
        ),
    ]

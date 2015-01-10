# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20150110_1042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalproduct',
            name='image',
            field=models.URLField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.URLField(null=True, blank=True),
        ),
    ]

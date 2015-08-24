# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pola', '0006_auto_20150823_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='query',
            name='client',
            field=models.CharField(default=None, max_length=40, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='client',
            field=models.CharField(default=None, max_length=40, null=True, blank=True),
        ),
        migrations.DeleteModel(
            name='Client',
        ),
    ]

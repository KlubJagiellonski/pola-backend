# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0004_auto_20151018_1214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='verified',
            field=models.BooleanField(default=False, verbose_name='Dane zweryfikowane'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0011_auto_20151128_2152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='common_name',
            field=models.CharField(db_index=True, max_length=128, verbose_name='Nazwa dla u\u017cytkownika', blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='official_name',
            field=models.CharField(db_index=True, max_length=128, null=True, verbose_name='Nazwa rejestrowa', blank=True),
        ),
    ]

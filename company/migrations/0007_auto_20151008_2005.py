# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0006_auto_20151008_1902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='plBrand_notes',
            field=models.TextField(null=True, verbose_name='Notes about brand', blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='plCapital_notes',
            field=models.TextField(null=True, verbose_name='Notes about share of Polish capital', blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='plRnD_notes',
            field=models.TextField(null=True, verbose_name='Notes about R&D center', blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='plTaxes_notes',
            field=models.TextField(null=True, verbose_name='Notes about payment of taxes', blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='plWorkers_notes',
            field=models.TextField(null=True, verbose_name='Notes about workers', blank=True),
        ),
    ]

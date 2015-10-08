# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import company.models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0005_auto_20150823_1316'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'verbose_name': 'Company', 'verbose_name_plural': 'Companies'},
        ),
        migrations.AddField(
            model_name='company',
            name='official_name',
            field=models.CharField(max_length=64, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='company',
            name='plBrand',
            field=company.models.IntegerRangeField(null=True, verbose_name='Information about brand', blank=True),
        ),
        migrations.AddField(
            model_name='company',
            name='plBrand_notes',
            field=models.TextField(null=True, verbose_name='Notes about brand'),
        ),
        migrations.AddField(
            model_name='company',
            name='plRnD',
            field=company.models.IntegerRangeField(null=True, verbose_name='Information about R&D center', blank=True),
        ),
        migrations.AddField(
            model_name='company',
            name='plRnD_notes',
            field=models.TextField(null=True, verbose_name='Notes about R&D center'),
        ),
        migrations.AddField(
            model_name='company',
            name='plTaxes',
            field=company.models.IntegerRangeField(null=True, verbose_name='Payment of taxes and information about registration', blank=True),
        ),
        migrations.AddField(
            model_name='company',
            name='plTaxes_notes',
            field=models.TextField(null=True, verbose_name='Notes about payment of taxes'),
        ),
        migrations.AddField(
            model_name='company',
            name='plWorkers',
            field=company.models.IntegerRangeField(null=True, verbose_name='Information about workers', blank=True),
        ),
        migrations.AddField(
            model_name='company',
            name='plWorkers_notes',
            field=models.TextField(null=True, verbose_name='Notes about workers'),
        ),
        migrations.AddField(
            model_name='company',
            name='verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='company',
            name='address',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(max_length=64, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='nip',
            field=models.CharField(db_index=True, max_length=10, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='plCapital',
            field=company.models.IntegerRangeField(null=True, verbose_name='Percentage share of Polish capital', blank=True),
        ),
    ]

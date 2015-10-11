# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0007_auto_20151008_2005'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='common_name',
            field=models.CharField(max_length=128, verbose_name=b'Common company name', blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(db_index=True, max_length=128, null=True, verbose_name=b'Name as retrieved from produkty_w_sieci API', blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='nip',
            field=models.CharField(db_index=True, max_length=10, null=True, verbose_name=b"Company's NIP#", blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='official_name',
            field=models.CharField(max_length=128, null=True, verbose_name=b'Official company name', blank=True),
        ),
    ]

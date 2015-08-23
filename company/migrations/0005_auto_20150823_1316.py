# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import company.models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0004_auto_20150821_2043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='plCapital',
            field=company.models.IntegerRangeField(null=True, verbose_name='Percentage share of Polish capital'),
        ),
    ]

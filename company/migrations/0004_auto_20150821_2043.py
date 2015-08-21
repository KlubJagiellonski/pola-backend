# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import company.models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_auto_20150816_0251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='plCapital',
            field=company.models.IntegerRangeField(verbose_name='Percentage share of Polish capital'),
        ),
    ]

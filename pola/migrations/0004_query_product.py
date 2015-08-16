# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
        ('pola', '0003_auto_20150812_0511'),
    ]

    operations = [
        migrations.AddField(
            model_name='query',
            name='product',
            field=models.ForeignKey(default=1, to='product.Product'),
            preserve_default=False,
        ),
    ]

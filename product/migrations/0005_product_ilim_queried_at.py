# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_auto_20151029_0811'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='ilim_queried_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]

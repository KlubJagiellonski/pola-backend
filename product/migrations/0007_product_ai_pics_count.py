# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_product_query_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='ai_pics_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]

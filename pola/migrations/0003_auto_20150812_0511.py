# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pola', '0002_auto_20150812_0259'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='company',
        ),
        migrations.AlterField(
            model_name='report',
            name='barcode',
            field=models.ForeignKey(to='product.Product'),
        ),
        migrations.DeleteModel(
            name='Company',
        ),
        migrations.DeleteModel(
            name='Product',
        ),
    ]

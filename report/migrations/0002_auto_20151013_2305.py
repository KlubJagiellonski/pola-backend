# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='product',
            field=models.ForeignKey(to='product.Product', null=True, on_delete=models.CASCADE),
        ),
    ]

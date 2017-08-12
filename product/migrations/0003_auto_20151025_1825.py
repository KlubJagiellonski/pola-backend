# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_product_created_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Produkt', 'verbose_name_plural': 'Produkty'},
        ),
        migrations.AlterField(
            model_name='product',
            name='code',
            field=models.CharField(max_length=20, verbose_name=b'Kod', db_index=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='company',
            field=models.ForeignKey(verbose_name=b'Producent', blank=True, to='company.Company', null=True, on_delete=models.CASCADE),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Nazwa'),
        ),
    ]

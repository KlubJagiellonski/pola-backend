# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_auto_20150823_1319'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('client', models.CharField(default=None, max_length=40, null=True, blank=True)),
                ('desciption', models.TextField()),
                ('product', models.ForeignKey(to='product.Product')),
            ],
        ),
    ]

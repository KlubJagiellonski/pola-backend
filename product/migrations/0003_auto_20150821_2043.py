# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20150813_0150'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='description_of_change',
        ),
        migrations.RemoveField(
            model_name='product',
            name='event_desc',
        ),
        migrations.AlterField(
            model_name='product',
            name='company',
            field=models.ForeignKey(blank=True, to='company.Company', null=True),
        ),
    ]

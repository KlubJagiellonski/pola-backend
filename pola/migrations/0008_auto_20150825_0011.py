# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pola', '0007_auto_20150824_2257'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='product',
        ),
        migrations.DeleteModel(
            name='Report',
        ),
    ]

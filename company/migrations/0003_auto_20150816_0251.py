# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_auto_20150816_0247'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='adres',
            new_name='address',
        ),
    ]

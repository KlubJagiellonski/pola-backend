# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pola', '0005_client_token'),
    ]

    operations = [
        migrations.RenameField(
            model_name='report',
            old_name='barcode',
            new_name='product',
        ),
    ]

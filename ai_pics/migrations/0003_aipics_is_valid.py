# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ai_pics', '0002_aiattachment_file_no'),
    ]

    operations = [
        migrations.AddField(
            model_name='aipics',
            name='is_valid',
            field=models.NullBooleanField(),
        ),
    ]
